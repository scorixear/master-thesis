# https://reyfarhan.com/posts/easy-gpt2-finetuning-huggingface/
import os
import time
import datetime
import random

import pandas as pd
import seaborn as sns
import numpy as np

import matplotlib.pyplot as plt
import torch
import torch._tensor
import torch_directml
from torch.utils.data import Dataset, DataLoader, random_split, SequentialSampler

from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config
from transformers import get_linear_schedule_with_warmup

import nltk
nltk.download('punkt')

SEED = 42
OUTPUT_DIR = "./models/rey_farhan_winter.pt"
INPUT_DIR = 'books'
INPUT_FILE = 'bb_winter.txt'

EPOCHS = 5
LEARNING_RATE = 5e-4
WARMUP_STEPS = 1e2
EPSILON = 1e-8
MAX_SEQ_LENGTH = 768
BATCH_SIZE = 16

SAMPLE_EVERY = 100

torch.manual_seed(SEED)

# Creating Training Set


with open(os.path.join(INPUT_DIR, INPUT_FILE), "r", encoding='UTF-8') as reader:
    lines = reader.readlines()

doc_lenghts = []
for line in lines:
    tokens = nltk.word_tokenize(line)
    doc_lenghts.append(len(tokens))
doc_lenghts = np.array(doc_lenghts)
sns.displot(doc_lenghts)
plt.show()

print('Max Token Length:', len(doc_lenghts[doc_lenghts > MAX_SEQ_LENGTH])/len(doc_lenghts))
print('Average Token Length', np.average(doc_lenghts))


# GPT2 Tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2', bos_token='<|startoftext|>', eos_token='<|endoftext|>', pad_token='<|pad|>') # gpt2-medium

print("The max model length is {} for this model, although the actual embedding size for GPT small is 768".format(tokenizer.model_max_length))
print("The beginning of sequence token {} token has the id {}".format(tokenizer.convert_ids_to_tokens(tokenizer.bos_token_id), tokenizer.bos_token_id))
print("The end of sequence token {} has the id {}".format(tokenizer.convert_ids_to_tokens(tokenizer.eos_token_id), tokenizer.eos_token_id))
print("The padding token {} has the id {}".format(tokenizer.convert_ids_to_tokens(tokenizer.pad_token_id), tokenizer.pad_token_id))

# PyTorch Dataset & DataLoaders

batch_size = 2
device = torch_directml.device()

class GPT2Dataset(Dataset):
    def __init__(self, txt_list: list[str], tokenizer, gpt2_type="gpt2", max_length=MAX_SEQ_LENGTH):
        self.tokenizer = tokenizer
        self.input_ids = []
        self.attn_masks = []
        
        for txt in txt_list:
            encoded_input_ids = tokenizer.encode('<|startoftext|>' + txt.strip() + '<|endoftext|>', add_special_tokens=True)
            
            self.input_ids.append(torch.tensor(encoded_input_ids))
            #self.attn_masks.append(torch.tensor(encodings_dict['attention_mask']))
    def __len__(self):
        return len(self.input_ids)
    
    def __getitem__(self, index):
        return self.input_ids[index]#, self.attn_masks[index]

dataset = GPT2Dataset(lines, tokenizer)

# split into training and validation sets
train_size = int(0.9*len(dataset))
val_size = len(dataset) - train_size

train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

print('{:>5,} training samples'.format(train_size))
print('{:>5,} validation samples'.format(val_size))

# Create DataLoaders for training and validation
# normally done in random order, here sequential
train_dataloader =  DataLoader(train_dataset, batch_size=1, shuffle=False)

validation_dataloader = DataLoader(val_dataset, sampler=SequentialSampler(val_dataset), batch_size=batch_size)

# Fine Tuning

configuration = GPT2Config.from_pretrained('gpt2', output_hidden_states=False)
model = GPT2LMHeadModel.from_pretrained('gpt2', config=configuration)


# resize embeddings to fit the bos_token etc.
model.resize_token_embeddings(len(tokenizer))

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)



#optimizer = AdamW(model.parameters(), lr=learning_rate, eps=epsilon)
optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE, eps=EPSILON)
total_steps = len(train_dataloader)*EPOCHS
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=WARMUP_STEPS, num_training_steps=total_steps)

def format_time(elapsed):
    return str(datetime.timedelta(seconds=int(round(elapsed))))

total_t0 = time.time()
training_stats = []
model = model.to(device)
proc_seq_count = 0

def pack_tensor(new_tensor, packed_tensor,):
    if packed_tensor is None:
        return new_tensor, True, None
    if new_tensor.size()[1] + packed_tensor.size()[1] > MAX_SEQ_LENGTH:
        return packed_tensor, False, new_tensor
    else:
        packed_tensor = torch.cat([new_tensor, packed_tensor[:,1:]],dim=1)
        return packed_tensor, True, None

# training
model.train()
for epoch_i in range(EPOCHS):
    print("")
    print('======== Epoch {:} / {:} ========'.format(epoch_i+1, EPOCHS))
    print('Training...')
    
    t0 = time.time()
    total_train_loss = 0
    b_input_ids = None
    for step, batch in enumerate(train_dataloader):
        (b_input_ids, carry_on, remainder) = pack_tensor(batch, b_input_ids)
        if carry_on and step != len(train_dataloader)-1:
            continue
        #b_masks = batch[1].to(device)
        b_input_ids = b_input_ids.to(device)
        b_labels = b_input_ids.to(device)
        
        outputs = model(
            b_input_ids, 
            labels=b_labels, 
            #attention_mask = b_masks, 
            token_type_ids=None)
        loss = outputs[0]
        batch_loss = loss.item()
        total_train_loss += batch_loss
        loss.backward()
        
        proc_seq_count += 1
        
        if proc_seq_count == BATCH_SIZE:
            proc_seq_count = 0
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()
            model.zero_grad()
        
        if step%SAMPLE_EVERY == 0 and not step == 0:
            elapsed = format_time(time.time() - t0)
            print('  Batch {:>5,} of {:>5,}. Loss {:>5,}. Elapsed: {:}'.format(step, len(train_dataloader), batch_loss, elapsed))
            
            #model.eval()
            
            #sample_outputs = model.generate(
            #  bos_token_id=random.randint(1,30000),
            #  do_sample=True,
            #  top_k = 50,
            #  max_length = 200,
            #  top_p=0.95,
            #  num_return_sequences=1
            #)
            #for i, sample_output in enumerate(sample_outputs):
            #  print("{}: {}".format(i, tokenizer.decode(sample_output, skip_special_tokens=True)))
            
            #model.train()
        #optimizer.step()
        #scheduler.step()
        #optimizer.zero_grad()
        #model.zero_grad()
      
    avg_train_loss = total_train_loss / len(train_dataloader)
    training_time = format_time(time.time() - t0)
    
    print("")
    print("  Average training loss: {0:.2f}".format(avg_train_loss))
    print("  Training epoch took: {:}".format(training_time))
    
    ### validation
    #print("")
    #print("Running Validation...")
    #
    #t0 = time.time()
    #
    #model.eval()
    #total_eval_loss = 0
    #nb_eval_steps = 0
    #
    ## evaluate data for one eopch
    #for batch in validation_dataloader:
    #    b_input_ids = batch[0].to(device)
    #    b_labels = batch[0].to(device)
    #    #b_masks = batch[1].to(device)
    #    
    #    with torch.no_grad():
    #        outputs = model(
    #            b_input_ids, 
    #            #attention_mask = b_masks, 
    #            labels = b_labels)
    #        loss = outputs[0]
    #      
    #    batch_loss = loss.item()
    #    total_eval_loss += batch_loss
    #avg_val_loss = total_eval_loss / len(validation_dataloader)
    #validation_time = format_time(time.time() - t0)
    #
    #print("  Validation Loss: {0:.2f}".format(avg_val_loss))
    #print("  Validation took: {:}".format(validation_time))
    #
    ## Record all statistics from this epoch
    training_stats.append(
        {
            'epoch': epoch_i+1,
            'Training Loss': avg_train_loss,
            #'Valid. Loss': avg_val_loss,
            'Training Time': training_time,
            #'Validation Time': validation_time
        }
    )

print("")
print("Training complete!")
print("total training took {:} (h:mm:ss)".format(format_time(time.time() - total_t0)))


# Summary of Training process
pd.set_option('display.precision', 2)
df_stats = pd.DataFrame(data=training_stats)
df_stats = df_stats.set_index('epoch')

print(df_stats)

sns.set(style='darkgrid')
sns.set(font_scale=1.5)
plt.rcParams["figure.figsize"] = (12,6)
plt.plot(df_stats['Training Loss'], 'b-o', label='Training')
#äplt.plot(df_stats['Valid. Loss'], 'g-o', label='Validation')

plt.title('Training & Validation Loss')
plt.xlabel('Epoch')
plt.ylabel("Loss")
plt.legend()
plt.xticks([1,2,3,4])
plt.show()


# Display Model Info
params = list(model.named_parameters())
print('The GPT-2 model has {:} different named parameters.\n'.format(len(params)))
print('==== Embedding Layer ====\n')
 
for p in params[0:2]:
    print("{:<55} {:>12}".format(p[0], str(tuple(p[1].size()))))
print("\n==== First Transformer ====\n")
for p in params[2:14]:
    print("{:<55} {:>12}".format(p[0], str(tuple(p[1].size()))))
print("\n==== Output Layer ====\n")
for p in params[-2:]:
    print("{:<55} {:>12}".format(p[0], str(tuple(p[1].size()))))

# Saving Model



#if not os.path.exists(OUTPUT_DIR):
#    os.makedirs(OUTPUT_DIR)
print("Saving model to %s" % OUTPUT_DIR)

#model_to_save = model.module if hasattr(model, 'module') else model
#model_to_save.save_pretrained(OUTPUT_DIR)
#tokenizer.save_pretrained(OUTPUT_DIR)

torch.save(model.state_dict(), OUTPUT_DIR)