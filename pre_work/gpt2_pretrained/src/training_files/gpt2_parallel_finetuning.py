import os
import sys
import time
import datetime
import argparse
import torch
import torch._tensor
from transformers import GPT2Tokenizer, GPT2LMHeadModel, get_linear_schedule_with_warmup
import numpy as np
from torch.utils.data import Dataset, DataLoader
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

print(f"Running from working directory {os.getcwd()}")

GPT_MODEL = "gpt2"
INPUT_FILE="bb_konrad"

BATCH_SIZE = 2
EPOCHS = 5
LEARNING_RATE = 3e-4
WARMUP_STEPS = 5000
MAX_SEQ_LEN = 768

SEED=42
SAMPLE_EVERY=100

DEVICE = "cpu"
if torch.cuda.is_available():
    DEVICE = "cuda"
    print("Using CUDA Device")
else:
    print("Using CPU Device")

def format_time(elapsed):
    return str(datetime.timedelta(seconds=int(round((elapsed)))))

def main(rank):
    os.environ['RANK'] = str(rank)
    dist.init_process_group(backend='nccl', init_method='env://')
    torch.cuda.set_device(rank)

    print("loading models...")
    tokenizer = GPT2Tokenizer.from_pretrained(GPT_MODEL, pad_token='<|pad|>', eos_token='<|endoftext|>')
    model: GPT2LMHeadModel = GPT2LMHeadModel.from_pretrained(GPT_MODEL).to(DEVICE)
    model.resize_token_embeddings(len(tokenizer))

    torch.manual_seed(SEED)

    class GPT2DataSet(Dataset):
        def __init__(self, book_dataset_path = 'books/'):
            super().__init__()

            book_path = os.path.join(book_dataset_path, INPUT_FILE+".txt")
            self.input_ids = []
            self.attn_masks = []
            self.end_of_text_token = tokenizer.eos_token
            with open(book_path, encoding="UTF-8") as reader:
               lines = reader.readlines()
               for line in lines:
                   if len(line.strip()) > 0:
                       line_str = f"{line.strip()}{self.end_of_text_token}"
                       encodings_dict = tokenizer(line_str, truncation=True, max_length = MAX_SEQ_LEN, padding="max_length")

                       self.input_ids.append(torch.tensor(encodings_dict['input_ids']).to(DEVICE))
                       self.attn_masks.append(torch.tensor(encodings_dict['attention_mask']).to(DEVICE))
        def __len__(self):
            return len(self.input_ids)
        def __getitem__(self, index):
            return self.input_ids[index], self.attn_masks[index]

    print("Reading in data...")
    dataset = GPT2DataSet()
    text_loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=False)


    total_steps = len(text_loader)*EPOCHS
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=WARMUP_STEPS, num_training_steps= total_steps)

    np.random.seed(SEED)

    total_t0 = time.time()
    total_train_loss = 0


    models_folder = "models"
    model = DDP(model, device_ids=[rank])
    

    model.train()
    for epoch in range(EPOCHS):
        print("")
        print(f'======== Epoch {epoch+1} / {EPOCHS} ========')
        print('Training...')
        t0 = time.time()

        for step, batch in enumerate(text_loader):
            input_tensor = batch[0]
            masks = batch[1]
            model.zero_grad()

            outputs = model(input_tensor, attention_mask = masks, token_type_ids=None)
            batch_loss = torch.mean((outputs - input_tensor)**2)
            total_train_loss += batch_loss
            batch_loss.backward()
            optimizer.step()
            scheduler.step()
            if step % SAMPLE_EVERY == 0 and not step == 0:
                elapsed = format_time(time.time() - t0)
                print(f'  Batch {step:>5,}  of  {len(text_loader):>5,}. Loss: {batch_loss:>5,}.   Elapsed: {elapsed}.')

        avg_train_loss = total_train_loss / len(text_loader)
        training_time = format_time(time.time() - t0)
        print("")
        print("  Average training loss: {0:.2f}".format(avg_train_loss))
        print(f"  Training epoch took: {training_time}")
        sys.stdout.flush()

    print("")
    print("Training complete!")
    print(f"Total training took {format_time(time.time()-total_t0)} (h:mm:ss)")      
    if(rank==0):
        torch.save(model.state_dict(), os.path.join(models_folder, f"{GPT_MODEL}_{INPUT_FILE}.pt"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rank', type=int, default=0)
    args = parser.parse_args()
    
    main(args.rank)