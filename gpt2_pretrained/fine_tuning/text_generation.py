import torch
import torch._tensor
import torch_directml
from transformers import GPT2Tokenizer, GPT2LMHeadModel, GPT2Config
import numpy as np
import os
import logging
import warnings

logging.getLogger().setLevel(logging.CRITICAL)
warnings.filterwarnings('ignore')


def choose_from_top(probs, n=5):
    ind = np.argpartition(probs, -n)[-n:]
    top_prob = probs[ind]
    top_prob = top_prob / np.sum(top_prob) # Normalize
    choice = np.random.choice(n, 1, p = top_prob)
    token_id = ind[choice][0]
    return int(token_id)


device = "cpu"
if torch.cuda.is_available():
    print("Using CUDA Device")
    device = 'cuda'
elif torch_directml.is_available():
    print("Using DIRECTML Device")
    device = torch_directml.device()
else:
    print("Using CPU Device")

print("loading models...")
models_folder = "."
model_path = os.path.join(models_folder, "gpt2_bb_konrad.pt")

model = GPT2LMHeadModel.from_pretrained('gpt2')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2', pad_token='<|pad|>', eos_token='<|endoftext|>')
model.resize_token_embeddings(len(tokenizer))
model = model.to(device)

model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

model.eval()
with torch.no_grad():
  while True:
    generation_finished = False
    input_text = input("Q: ")
    cur_ids = torch.tensor(tokenizer.encode(input_text, add_special_tokens=False)).unsqueeze(0).to(device)
    for i in range(100):
      outputs = model(cur_ids, labels = cur_ids)
      loss, logits = outputs[:2]
      softmax_logits = torch.softmax(logits[0,-1], dim=0)
      if i < 3:
        n = 20
      else:
        n = 3
      next_token_id = choose_from_top(softmax_logits.to('cpu').numpy(), n=n)
      cur_ids = torch.cat([cur_ids, torch.ones((1,1)).long().to(device)*next_token_id], dim=1)
      if next_token_id in tokenizer.encode('<|endoftext|>'):
        generation_finished = True
        break
    
    output_list = list(cur_ids.squeeze().to('cpu').numpy())
    output_text = tokenizer.decode(output_list, skip_special_tokens=True)
      
    print(f"A: {output_text}")