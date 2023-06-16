# source https://huggingface.co/docs/transformers/main/main_classes/deepspeed#main-deepspeed-resources

from transformers import TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments
from transformers import LlamaForCausalLM, LlamaTokenizer, LlamaConfig
from transformers.deepspeed import HfDeepSpeedConfig
import deepspeed
import os
import torch


os.environ["TOKENIZERS_PARALLELISM"] = "false"  # To avoid warnings about parallelism in tokenizers
local_rank = int(os.getenv("LOCAL_RANK", "0"))
world_size = int(os.getenv("WORLD_SIZE", "1"))
torch.cuda.set_device(local_rank)
deepspeed.init_distributed()

config = LlamaConfig.from_pretrained("../models/converted_llama_model/7b_model")

model_hidden_size = config.d_model

train_batch_size = 1 * world_size

ds_config = {
    "fp16": {
        "enabled": False
    },
    "bf16": {
        "enabled": False
    },
    "zero_optimization": {
        "stage": 3,
        "offload_param": {
            "device": "cpu",
            "pin_memory": True
        },
        "overlap_comm": True,
        "contiguous_gradients": True,
        "reduce_bucket_size": model_hidden_size * model_hidden_size,
        "stage3_prefetch_bucket_size": 0.9 * model_hidden_size * model_hidden_size,
        "stage3_param_persistence_threshold": 10 * model_hidden_size
    },
    "steps_per_print": 2000,
    "train_batch_size": train_batch_size,
    "train_micro_batch_size_per_gpu": 1,
    "wall_clock_breakdown": False
}

dschf = HfDeepSpeedConfig(ds_config)  # keep this object alive
model = LlamaForCausalLM.from_pretrained("../models/converted_llama_model/7b_model")

# initialise Deepspeed ZeRO and store only the engine object
ds_engine = deepspeed.initialize(model=model, config_params=ds_config)[0]
ds_engine.module.train()


text_in = "The quick brown fox jumps over the lazy dog"
tokenizer = LlamaTokenizer.from_pretrained("../models/converted_llama_model/7b_model")
inputs = tokenizer.encode(text_in, return_tensors="pt").to(device=local_rank)


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
)

trainer = Trainer(
    model=ds_engine,
    args=training_args,
    train_dataset=train_data,
    data_collator=data_collator,
    deepspeed = dschf,
)
trainer.train()

trainer.save_model("models/traied_llama_model/7b_konrad.pt")