# https://reyfarhan.com/posts/easy-gpt2-finetuning-huggingface/
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config
import torch
import torch_directml
import random
import os

device = torch.device('cpu')

input_dir = "./models/rey_farhan_winter/"
model_path ="./models/gpt2_winter_5.pt"
#model = GPT2LMHeadModel.from_pretrained(input_dir)
#tokenizer = GPT2Tokenizer.from_pretrained(input_dir)
model = GPT2LMHeadModel.from_pretrained('gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model.load_state_dict(torch.load(model_path))
model = model.to(device)

model.eval()

while True:
    input_text = input("Q: ")
    #input_text = "<|startoftext|>"+input_text.strip()
    
    generated = torch.tensor(tokenizer.encode(input_text)).unsqueeze(0)
    generated = generated.to(device)
    
    print(generated)
    
    sample_outputs = model.generate(
      generated,
      #bos_token_id=random.randint(1,30000),
      do_sample=True,
      top_k=50,
      max_length=300,
      top_p=0.95,
      num_return_sequences=3
    )
    for i, sample_output in enumerate(sample_outputs):
      print("{}:{}\n\n".format(i, tokenizer.decode(sample_output, skip_special_tokens=True)))