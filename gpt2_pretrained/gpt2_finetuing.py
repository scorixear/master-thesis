import torch
import torch_directml
from transformers import GPT2Tokenizer, GPT2LMHeadModel, AdamW, get_linear_schedule_with_warmup
import numpy as np
from torch.utils.data import Dataset, DataLoader
import os
import logging
import warnings

logging.getLogger().setLevel(logging.CRITICAL)
warnings.filterwarnings('ignore')

device = "cpu"
if torch.cuda.is_available():
    device = 'cuda'
device = torch_directml.device()

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')
model = model.to(device)

class BookDataset(Dataset):
    def __init__(self, book_dataset_path = 'books/', book_filename="bb_small.txt"):
         super().__init__()
         
         book_path = os.path.join(book_dataset_path, book_filename)
         self.text_list = []
         self.end_of_text_token = "<|endoftext|>"
         with open(book_path, encoding="UTF-8") as reader:
             lines = reader.readlines()
             x= 0
             for line in lines:
                 if len(line.strip()) > 0:
                     line_str = f"INPUT: {line.strip()}{self.end_of_text_token}"
                     self.text_list.append(line_str)
    def __len__(self):
        return len(self.text_list)
    def __getitem__(self, index):
        return self.text_list[index]
    
dataset = BookDataset()
text_loader = DataLoader(dataset, batch_size=1, shuffle=False)


BATCH_SIZE = 16
EPOCHS = 5
LEARNING_RATE = 3e-5
WARMUP_STEPS = 5000
MAX_SEQ_LEN = 1024

model.train()
optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=WARMUP_STEPS, num_training_steps= -1)
proc_seq_count = 0
sum_loss = 0
batch_count = 0

tmp_text_tens = None
models_folder = "models"

for epoch in range(EPOCHS):
    print(f"EPOCH {epoch} started"+'='*30)
    for idx, line in enumerate(text_loader):
        text_tens = torch.tensor(tokenizer.encode(line[0])).unsqueeze(0).to(device)
        
        if text_tens.size()[1] > MAX_SEQ_LEN:
            continue
        
        if not torch.is_tensor(tmp_text_tens):
            tmp_text_tens = text_tens
            continue
        else:
            if tmp_text_tens.size()[1] + text_tens.size()[1] > MAX_SEQ_LEN:
                work_text_tens = tmp_text_tens
                tmp_text_tens = text_tens
            else:
                tmp_text_tens = torch.cat([tmp_text_tens, text_tens[:,1:]], dim=1)
                continue
        outputs = model(work_text_tens, labels=work_text_tens)
        loss, logits = outputs[:2]
        loss.backward()
        sum_loss = sum_loss + loss.detach().data
        
        proc_seq_count = proc_seq_count + 1
        if proc_seq_count == BATCH_SIZE:
            proc_seq_count = 0
            batch_count += 1
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()
            model.zero_grad()
        if batch_count == 100:
            print(f"sum loss {sum_loss}")
            batch_count = 0
            sum_loss = 0
torch.save(model.state_dict(), os.path.join(models_folder, f"gpt2_text_{EPOCHS}.pt"))
    