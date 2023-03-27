import os, sys
import time
import datetime
import torch
import torch._tensor
from transformers import GPT2Tokenizer, GPT2LMHeadModel, get_linear_schedule_with_warmup
import numpy as np
from torch.utils.data import Dataset, DataLoader

print(f"Running from working directory {os.getcwd()}")

# this defines the input file
GPT_MODEL = "gpt2"
INPUT_FILE="bb_konrad"

# as I have read, large batch sizes lead to memory problems
BATCH_SIZE = 2
# as loss does not decrease, I don't see the point in more epochs
EPOCHS = 5
# standard learning rate, behaviour does not change with 5e-4, 3e-5
LEARNING_RATE = 3e-4
WARMUP_STEPS = 5000
# maxmium sequencel length in gpt2 is apparently 768 tokens
# each line will transformed into a tensor and extended with padding tokens
# until this maximum sequence length is reached
MAX_SEQ_LEN = 768

# seed for torch to get same results with same settings
SEED=42
# output between training batches to see progress
SAMPLE_EVERY=100

# Device is set to cpu for local and CUDA if available
DEVICE = "cpu"
if torch.cuda.is_available():
    DEVICE = "cuda"
    print("Using CUDA Device")
else:
    print("Using CPU Device")

print("loading models...")
# the default code also defines "bos_token", adding this does not change the result
tokenizer = GPT2Tokenizer.from_pretrained(GPT_MODEL, pad_token='<|pad|>', eos_token='<|endoftext|>')
# gpt2-medium model
model: GPT2LMHeadModel = GPT2LMHeadModel.from_pretrained(GPT_MODEL).to(DEVICE)
# since we added pad-token, we need to resize the model
model.resize_token_embeddings(len(tokenizer))

torch.manual_seed(SEED)

class GPT2DataSet(Dataset):
    def __init__(self, book_dataset_path = 'books/'):
        super().__init__()
        # read in the book
        book_path = os.path.join(book_dataset_path, INPUT_FILE+".txt")
        self.input_ids = []
        self.attn_masks = []
        self.end_of_sentence_token = tokenizer.eos_token
        with open(book_path, encoding="UTF-8") as reader:
            lines = reader.readlines()
            # for each line create a tensor
            for line in lines:
                # if that line is not empty
                if len(line.strip()) > 0:
                    # append the eos token to the line
                    line_str = f"{line.strip()}{self.end_of_sentence_token}"
                    # this will create input ids and attention mask, filled up until MAX_SEQ_LEN with padding tokens
                    encodings_dict = tokenizer(line_str, truncation=True, max_length = MAX_SEQ_LEN, padding="max_length")
                    # create pytorch tensors
                    self.input_ids.append(torch.tensor(encodings_dict['input_ids']).to(DEVICE))
                    self.attn_masks.append(torch.tensor(encodings_dict['attention_mask']).to(DEVICE))
    def __len__(self):
        return len(self.input_ids)
    def __getitem__(self, index):
        return self.input_ids[index], self.attn_masks[index]


def format_time(elapsed):
    return str(datetime.timedelta(seconds=int(round((elapsed)))))

print("Reading in data...")
dataset = GPT2DataSet()
text_loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=False)

# total number of steps to perform
total_steps = len(text_loader)*EPOCHS

# using the huggingface AdamW optimizer does not change the results
optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=WARMUP_STEPS, num_training_steps= total_steps)

np.random.seed(SEED)
# for total training time
total_t0 = time.time()
total_train_loss = 0
# output folder for the model
models_folder = "models"

# start training model
model.train()
for epoch in range(EPOCHS):
    print("")
    print(f'======== Epoch {epoch+1} / {EPOCHS} ========')
    print('Training...')
    # start time of each epoch
    t0 = time.time()
    
    # for reach batch
    for step, batch in enumerate(text_loader):
        # set labels to input_ids
        input_tensor = batch[0]
        labels = batch[0]
        # __get_item()__ returns input_ids and attention_mask
        masks = batch[1]
        
        # I have seen code that zero_grads the model after each step
        model.zero_grad()
        # generate outputs from model
        outputs = model(input_tensor, attention_mask = masks, token_type_ids=None)
        # get the loss of the model
        loss, logits = outputs[:2]
        batch_loss = loss.mean()
        total_train_loss += batch_loss
        # propagate backwards, step optimizer and scheduler
        batch_loss.backward()
        optimizer.step()
        scheduler.step()
        # output between training for progress tracking
        if step % SAMPLE_EVERY == 0 and not step == 0:
            elapsed = format_time(time.time() - t0)
            print(f'  Batch {step:>5,}  of  {len(text_loader):>5,}. Loss: {batch_loss:>5,}.   Elapsed: {elapsed}.')
    # calculate avg training loss per step
    avg_train_loss = total_train_loss / len(text_loader)
    training_time = format_time(time.time() - t0)
    print("")
    print("  Average training loss: {0:.2f}".format(avg_train_loss))
    print(f"  Training epoch took: {training_time}")
    sys.stdout.flush()

# training finished, save model
print("")
print("Training complete!")
print(f"Total training took {format_time(time.time()-total_t0)} (h:mm:ss)")      
    
torch.save(model.state_dict(), os.path.join(models_folder, f"{GPT_MODEL}_{INPUT_FILE}.pt"))
    