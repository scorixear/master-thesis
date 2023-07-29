import os
from peft.tuners.lora import LoraConfig
from peft.mapping import get_peft_model
from peft.utils.other import prepare_model_for_kbit_training
#from peft.utils.other import prepare_model_for_int8_training
from transformers import  AutoModelForCausalLM, LlamaTokenizer, BitsAndBytesConfig
# from transformers import AutoTokenizer, AutoConfig
import torch
#import torch.nn as nn
import transformers
from datasets import load_dataset
import huggingface_hub
#import bitsandbytes as bnb
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


model_name = "meta-llama/Llama-2-7b-hf"
token = "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"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

huggingface_hub.login(token=token) 

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_8bit=True,
    device_map="auto"
)

print(f"Setting special tokens for LLaMA model {model_name}...")

model.config.pad_token_id=0
model.config.bos_token_id=1
model.config.eos_token_id=2

print(f"Loaded model {model_name}")
tokenizer = LlamaTokenizer.from_pretrained(model_name)
print(f"Setting special tokens for LLaMA tokenizer {model_name}...")
tokenizer.pad_token_id=0
tokenizer.bos_token_id=1
tokenizer.eos_token_id=2
tokenizer.padding_side = "left"

print(f"Loaded tokenizer {model_name}")

def print_trainable_parameters(model):
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
    print(
        f"trainable params: {trainable_params} || all params: {all_param} || trainable%: {100 * trainable_params / all_param}"
    )
    

config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, config)
print_trainable_parameters(model)

data_files = {}
dataset_args = {}
data_files["train"] =  "./input/health_information_systems_epub.md"
extension = "text"
dataset_args["keep_linebreaks"] = True

raw_dataset = load_dataset(
    extension,
    data_files=data_files,
    **dataset_args
)

column_names = list(raw_dataset["train"].features)
text_column_name = "text" if "text" in column_names else column_names[0]

def tokenizer_function(examples):
    return tokenizer(examples[text_column_name])
tokenized_datasets = raw_dataset.map(
    tokenizer_function,
    batched=True,
    num_proc=1,
    remove_columns=column_names,
    load_from_cache_file=True,
    desc="Running tokenizer on dataset"
)
block_size = min(1024, tokenizer.model_max_length)

def group_texts(examples):
    concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
    total_length = len(concatenated_examples[list(examples.keys())[0]])
    total_length = (total_length // block_size) * block_size
    result = {
        k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
        for k, t in concatenated_examples.items()
    }
    result["labels"] = result["input_ids"].copy()
    return result
lm_datasets = tokenized_datasets.map(
    group_texts,
    batched=True,
    num_proc=1,
    load_from_cache_file=True,
    desc=f"Grouping texts in chunks of {block_size} tokens"
)
train_dataset = lm_datasets["train"]

trainer = transformers.Trainer(
    model=model,
    train_dataset=train_dataset,
    args=transformers.TrainingArguments(
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        warmup_steps=50,
        # max_steps=200
        learning_rate=2e-4,
        fp16=True,
        logging_steps=1,
        num_train_epochs=3,
        output_dir="./trained/7B-lora-3"
    ),
    data_collator=transformers.DataCollatorForLanguageModeling(tokenizer, mlm=False)
)




print(f"Setting special tokens for LLaMA model {model_name}...")
model.config.pad_token_id = 0
model.config.bos_token_id = 1
model.config.eos_token_id = 2

print("Setting tokenizer tokens")
tokenizer.pad_token_id = 0
tokenizer.bos_token_id = 1
tokenizer.eos_token_id = 2

model.config.use_cache = False
train_result = trainer.train()
trainer.save_model()

metrics = train_result.metrics
metrics["train_samples"] = len(train_dataset)
        
trainer.log_metrics("train", metrics)
trainer.save_metrics("train", metrics)
trainer.save_state()