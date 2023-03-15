from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
import torch
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-cased-distilled-squad')
model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-cased-distilled-squad')

with open('books/bb_small.txt', encoding="UTF-8") as reader:
  context = reader.read()

while True:
  question = input("Q:")
  inputs = tokenizer(question, context, return_tensors="pt")
  with torch.no_grad():
      outputs = model(**inputs)
      start_logits, end_logits = outputs.start_logits, outputs.end_logits
      start_position = torch.argmax(start_logits, dim=1).item()
      end_position = torch.argmax(end_logits, dim=1).item()
      answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][start_position:end_position+1]))
  
      print(answer)