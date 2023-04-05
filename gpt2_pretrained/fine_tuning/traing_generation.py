from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the saved model
model_path = "models/trainer_konrad.pt"
model = AutoModelForCausalLM.from_pretrained(model_path)

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# Generate some text
while True:
  prompt = input("Q: ")
  input_ids = tokenizer.encode(prompt, return_tensors='pt')
  output = model.generate(input_ids, max_length=100, do_sample=True)
  generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

  print(generated_text)
