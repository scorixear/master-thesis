# source https://huggingface.co/docs/transformers/main/main_classes/deepspeed#main-deepspeed-resources
"""

Execute with:
srun -- jobid $SLURM_JOBID bash -c `python -m torch.distributed.run --nproc_per_node=GPUS_PER_NODE --nnodes $SLURM_NNODES --node_rank $SLURM_PROCID --master_addr $MASTER_ADDR --master_port $MASTER_PORT 03_train_llama.py
"""
import os
import argparse
import inspect
import logging
from typing import Tuple

import torch
import numpy as np
import deepspeed # cannot be installed on windows, release by microsoft, cannot be installed by windows - wtf

from transformers import TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments
from transformers import LlamaForCausalLM, LlamaTokenizer, GenerationMixin
from transformers.modeling_outputs import CausalLMOutputWithPast

os.environ["TOKENIZERS_PARALLELISM"] = "false"  # To avoid warnings about parallelism in tokenizers

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

MAX_LENGTH = int(10000) # Hardcoded max length to avoid infinite loop

def set_seed(args):
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if args.n_gpu > 0:
        torch.cuda.manual_seed_all(args.seed)

#
# Functions to prepare models' input
#


def adjust_length_to_model(length, max_sequence_length):
    if length < 0 and max_sequence_length > 0:
        length = max_sequence_length
    elif 0 < max_sequence_length < length:
        length = max_sequence_length  # No generation bigger than model size
    elif length < 0:
        length = MAX_LENGTH
    return length

def sparse_model_config(model_config):
    embedding_size = None
    if hasattr(model_config, "hidden_size"):
        embedding_size = model_config.hidden_size
    elif hasattr(model_config, "n_embed"):
        embedding_size = model_config.n_embed
    elif hasattr(model_config,  "n_embd"):
        embedding_size = model_config.n_embd
    
    num_head = None
    if hasattr(model_config, "num_attention_heads"):
        num_head = model_config.num_attention_heads
    elif hasattr(model_config,  "n_head"):
        num_head = model_config.n_head
    
    if embedding_size is None or num_head is None or num_head == 0:
        raise ValueError("Could not find embedding size or number of heads")
    
    num_embeddings_size_per_head = int(embedding_size / num_head)
    if hasattr(model_config, "n_layer"):
        num_layer = model_config.n_layer
    elif hasattr(model_config, "num_hidden_layers"):
        num_layer = model_config.num_hidden_layers
    else:
        raise ValueError("Could not find number of layers in model configuration")
    return num_layer, num_head, num_embeddings_size_per_head

def generate_past_key_values(model, batch_size, seq_len):
    num_block_layers, num_attention_heads, num_embedding_size_per_head = sparse_model_config(model.config)
    past_key_values = tuple(
        (
            torch.empty(batch_size, num_attention_heads, seq_len, num_embedding_size_per_head)
            .to(model.dtype)
            .to(model.device),
            torch.empty(batch_size, num_attention_heads, seq_len, num_embedding_size_per_head)
            .to(model.dtype)
            .to(model.device),
        )
        for _ in range(num_block_layers)
    )
    return past_key_values
    

def prepare_jit_inputs(inputs, model, tokenizer):
    batch_size = len(inputs)
    dummy_input = tokenizer.batch_encode_plus(inputs, return_tensors="pt")
    dummy_input = dummy_input.to(model.device)
    if model.config.use_cache:
        dummy_input["past_key_values"] = generate_past_key_values(model, batch_size, 1)
    dummy_input["attention_mask"] = torch.cat(
        [
            torch.zeros(dummy_input["attention_mask"].shape[0], 1)
            .to(dummy_input["attention_mask"].dtype)
            .to(model.device),
            dummy_input["attention_mask"],
        ],
        -1,
    )
    return dummy_input

class _ModelFallbackWrapper(GenerationMixin):
    __slots__ = ("_optimized", "_default")

    def __init__(self, optimized, default):
        self._optimized = optimized
        self._default = default

    def __call__(self, *args, **kwargs):
        if kwargs["past_key_values"] is None and self._default.config.use_cache:
            kwargs["past_key_values"] = generate_past_key_values(self._default, kwargs["input_ids"].shape[0], 0)
        kwargs.pop("position_ids", None)
        for k in list(kwargs.keys()):
            if kwargs[k] is None or isinstance(kwargs[k], bool):
                kwargs.pop(k)
        outputs = self._optimized(**kwargs)
        lm_logits = outputs[0]
        past_key_values = outputs[1]
        fixed_output = CausalLMOutputWithPast(
            loss=None,
            logits=lm_logits,
            past_key_values=past_key_values,
            hidden_states=None,
            attentions=None,
        )
        return fixed_output

    def __getattr__(self, item):
        return getattr(self._default, item)

    def prepare_inputs_for_generation(
        self, input_ids, past_key_values=None, inputs_embeds=None, use_cache=None, **kwargs
    ):
        return self._default.prepare_inputs_for_generation(
            input_ids, past_key_values=past_key_values, inputs_embeds=inputs_embeds, use_cache=use_cache, **kwargs
        )

    def _reorder_cache(
        self, past_key_values: Tuple[Tuple[torch.Tensor]], beam_idx: torch.Tensor
    ) -> Tuple[Tuple[torch.Tensor]]:
        """
        This function is used to re-order the `past_key_values` cache if [`~PretrainedModel.beam_search`] or
        [`~PretrainedModel.beam_sample`] is called. This is required to match `past_key_values` with the correct
        beam_idx at every generation step.
        """
        return self._default._reorder_cache(past_key_values, beam_idx)




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_path",
        default=None,
        type=str,
        required=True,
        help="Path to pretrained model"
    )
    
    parser.add_argument("--prompt", type=str, default="")
    parser.add_argument("--length", type=int, default=20)
    parser.add_argument("--stop_token", type=str, default=None, help="Token at which text generation is stopped")
    
    parser.add_argument(
        "--temperature",
        type=float,
        default=1.0,
        help="temperature of 1.0 has no effect, lower tend toward greedy sampling",
    )
    parser.add_argument(
        "--repetition_penalty",
        type=float,
        default=1.0,
        help="primarily useful for CTRL model; in that case, use 1.2",
    )
    parser.add_argument("--k", type=int, default=0, help="k for top-k sampling")
    parser.add_argument("--p", type=float, default=0.9, help="p for nucleus sampling")
    parser.add_argument("--prefix", type=str, default="", help="Text added prior to input.")
    parser.add_argument("--seed", type=int, default=42, help="random seed for initialization")
    parser.add_argument("--no_cuda", action="store_true", help="Avoid using CUDA when available")
    parser.add_argument("--num_return_sequences", type=int, default=1, help="The number of samples to generate.")
    parser.add_argument(
        "--fp16",
        action="store_true",
        help="Whether to use 16-bit (mixed) precision (through NVIDIA apex) instead of 32-bit",
    )
    parser.add_argument("--jit", action="store_true", help="Whether to use torch.jit.trace to speed up generation")
    
    args = parser.parse_args()
    
    args.device = torch.device("cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu")
    args.n_gpu = 0 if args.no_cuda else torch.cuda.device_count()
    logger.warning(f"device: {args.device}, n_gpu: {args.n_gpu}, 16-bits training: {args.fp16}")
    set_seed(args)
    
    tokenizer = LlamaTokenizer.from_pretrained(args.model_path)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = LlamaForCausalLM.from_pretrained(args.model_path)
    model.to(args.device)
    if args.fp16:
        model.half()
    max_seq_length = getattr(model.config,  "max_position_embeddings", 0)
    args.length = adjust_length_to_model(args.length, max_sequence_length=max_seq_length)
    logger.info(args)
    
    prompt_text = args.prompt if args.prompt else input("Model prompt >>> ")
    
    prefix = args.prefix if args.prefix else args.padding_text
    encoded_prompt = tokenizer.encode(prefix + prompt_text, add_special_tokens=False, return_tensors="pt")
    encoded_prompt = encoded_prompt.to(args.device)
    
    if encoded_prompt.size()[-1] == 0:
        input_ids = None
    else:
        input_ids = encoded_prompt

    if args.jit:
        jit_input_texts = ["enable jit"]
        jit_inputs = prepare_jit_inputs(jit_input_texts, model, tokenizer)
        torch._C._jit_set_texpr_fuser_enabled(False)
        model.config.return_dict = False
        if hasattr(model, "forward"):
            sig = inspect.signature(model.forward)
        else:
            sig = inspect.signature(model.__call__)
        jit_inputs = tuple(jit_inputs[key] for key in sig.parameters if jit_inputs.get(key, None) is not None)
        traced_model = torch.jit.trace(model, jit_inputs, strict=False)
        traced_model = torch.jit.freeze(traced_model.eval())
        traced_model(*jit_inputs)
        traced_model(*jit_inputs)

        model = _ModelFallbackWrapper(traced_model, model)
    output_sequences = model.generate(
        input_ids=input_ids,
        max_length=args.length + len(encoded_prompt[0]),
        temperature=args.temperature,
        top_k=args.k,
        top_p=args.p,
        repetition_penalty=args.repetition_penalty,
        do_sample=True,
        num_return_sequences=args.num_return_sequences,
    )
     # Remove the batch dimension when returning multiple sequences
    if len(output_sequences.shape) > 2:
        output_sequences.squeeze_()
    
    generated_sequences = []

    for generated_sequence_idx, generated_sequence in enumerate(output_sequences):
        print(f"=== GENERATED SEQUENCE {generated_sequence_idx + 1} ===")
        generated_sequence = generated_sequence.tolist()

        # Decode text
        text = tokenizer.decode(generated_sequence, clean_up_tokenization_spaces=True)

        # Remove all text after the stop token
        text = text[: text.find(args.stop_token) if args.stop_token else None]

        # Add the prompt at the beginning of the sequence. Remove the excess text that was used for pre-processing
        total_sequence = (
            prompt_text + text[len(tokenizer.decode(encoded_prompt[0], clean_up_tokenization_spaces=True)) :]
        )

        generated_sequences.append(total_sequence)
        print(total_sequence)

    return generated_sequences
    

if __name__ == "__main__":
    main()
  
ds_config_path = "ds_config.json"

local_rank = int(os.getenv("LOCAL_RANK", "0")) # get the local rank and world size from slurm env variables
world_size = int(os.getenv("WORLD_SIZE", "1"))
torch.cuda.set_device(local_rank) # set the device to the local rank
deepspeed.init_distributed() # and initialise deepspeed


train_batch_size = 1 * world_size

# get the converted weights of the model
model = LlamaForCausalLM.from_pretrained("../models/converted_llama_model/7b_model")

# initialise Deepspeed ZeRO and store only the engine object
ds_engine = deepspeed.initialize(model=model, config_params=ds_config_path)[0]
# set model to train mode
ds_engine.module.train()

# Load the tokenizer from convereted weights
tokenizer = LlamaTokenizer.from_pretrained("../models/converted_llama_model/7b_model")

# Prepare the training data as a TextDataset
train_data = TextDataset(tokenizer=tokenizer, file_path="books/bb_konrad.txt", block_size=128)

# Define a data collator to batch the training data
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

training_args = TrainingArguments(
    output_dir="output",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=16,
    save_steps=1000,
    save_total_limit=2,
    deepspeed = ds_config_path,
    # a lot more arguments to be set here
    # see deepseed config
)
# Initialise the trainer
trainer = Trainer(
    model=ds_engine,
    args=training_args,
    train_dataset=train_data,
    data_collator=data_collator,
)

# Train the model and hope for the best
trainer.train()

# if you get here, you are lucky
# save the model
trainer.save_model("models/trained_llama_model/7b_konrad.pt")
