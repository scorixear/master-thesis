# source https://huggingface.co/docs/transformers/main/main_classes/deepspeed#main-deepspeed-resources

import os
from transformers import TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments
from transformers import LlamaForCausalLM, LlamaTokenizer
from transformers.deepspeed import HfDeepSpeedConfig
import deepspeed # cannot be installed on windows, release by microsoft, cannot be installed by windows - wtf
import torch


os.environ["TOKENIZERS_PARALLELISM"] = "false"  # To avoid warnings about parallelism in tokenizers
local_rank = int(os.getenv("LOCAL_RANK", "0")) # get the local rank and world size from slurm env variables
world_size = int(os.getenv("WORLD_SIZE", "1"))
torch.cuda.set_device(local_rank) # set the device to the local rank
deepspeed.init_distributed() # and initialise deepspeed


train_batch_size = 1 * world_size

ds_config = {
    "fp16": {
        # enabled if trainer args are enabled
        "enabled": "auto",
        # figure out values here!!!
        "loss_scale": 0,
        "loss_scale_window": 1000,
        "initial_scale_power": 16,
        "hysteresis": 2,
        "min_loss_scale": 1
    },

    "optimizer": {
        # check if correct optimizer is used
        "type": "AdamW",
        "params": {
            # configured by trainer args
            "lr": "auto",
            "betas": "auto",
            "eps": "auto",
            "weight_decay": "auto"
        }
    },

    "scheduler": { # possibly no warmup here
        "type": "WarmupLR",
        # otherwise configured by trainer args
        "params": {
            "warmup_min_lr": "auto",
            "warmup_max_lr": "auto",
            "warmup_num_steps": "auto"
        }
    },
    # stage 2 for best performance
    "zero_optimization": {
        "stage": 2,
        # possibly no offloading to cpu (not sure)
        "offload_optimizer": {
            "device": "cpu",
            # what ever this is
            "pin_memory": True
        },
        # CHECK THE VALUES HERE
        "allgather_partitions": True,
        # this was calculated from model_hidden_size
        # so maybe not fixed value
        "allgather_bucket_size": 2e8,
        "overlap_comm": True,
        "reduce_scatter": True,
        # this was calculated from model_hidden_size
        "reduce_bucket_size": 2e8,
        # what is this?
        "contiguous_gradients": True,
        # as by the paper
        "gradient_clipping": 1.0,
    },
    # CHECK THE VALUES HERE
    "steps_per_print": 2000,
    # no idea what this is
    "train_batch_size": train_batch_size,
    "train_micro_batch_size_per_gpu": 1,
    # what ever this is
    "wall_clock_breakdown": False
}

# initialize deepspeed config. MUST BE DONE BEFORE MODEL INITIALIZATION.
dschf = HfDeepSpeedConfig(ds_config)  # keep this object alive
# get the converted weights of the model
model = LlamaForCausalLM.from_pretrained("../models/converted_llama_model/7b_model")

# initialise Deepspeed ZeRO and store only the engine object
ds_engine = deepspeed.initialize(model=model, config_params=ds_config)[0]
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
    deepspeed = dschf,
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
