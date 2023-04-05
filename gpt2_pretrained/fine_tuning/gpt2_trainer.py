from transformers import AutoTokenizer, AutoModelForCausalLM, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

# Instantiate a pre-trained GPT-2 model
model_name = "gpt2"
model = AutoModelForCausalLM.from_pretrained(model_name)

# Instantiate a tokenizer to convert text to tokens
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Prepare the training data as a TextDataset
train_data = TextDataset(tokenizer=tokenizer, file_path="books/bb_konrad.txt", block_size=128)

# Define a data collator to batch the training data
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Define the training arguments
training_args = TrainingArguments(
    output_dir="output",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=16,
    save_steps=1000,
    save_total_limit=2,
)

# Instantiate a Trainer object and train the model
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_data,
    data_collator=data_collator,
    gpus=1,
)
trainer.train()

# Evaluate the trained model on a validation dataset
#eval_data = TextDataset(tokenizer=tokenizer, file_path="path/to/eval.txt", block_size=128)
#trainer.evaluate(eval_data)

# Save the trained model to disk
trainer.save_model("models/trainer_konrad.pt")
