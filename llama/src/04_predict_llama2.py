import json
import sys
import logging

import pandas as pd
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

logger = logging.getLogger(__name__)

def main():
    # setup logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    
    transformers.utils.logging.set_verbosity_info()
    
    log_level = logging.INFO
    logger.setLevel(log_level)
    transformers.utils.logging.set_verbosity(log_level)
    transformers.utils.logging.enable_default_handler()
    transformers.utils.logging.enable_explicit_format()

    #single_question_dataset = pd.read_csv("data/single_questions.csv")
    #multi_question_dataset = pd.read_csv("data/multi_questions.csv")
    #transfer_question_dataset = pd.read_csv("data/transfer_questions.csv")
    
    single_question_dataset = read_json("data/single_questions.json")
    multi_question_dataset = read_json("data/multi_questions.json")
    transfer_question_dataset = read_json("data/transfer_questions.json")
    
    dataframe = pd.DataFrame(columns=["Question", "Transformed", "Generated", "True_Answer", "Num_Answers", "Type", "Source", "Context", "True_Input"])
    
    model_dir = "./trained/7B"
    
    model = AutoModelForCausalLM.from_pretrained(model_dir)
    model = model.to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    
    tokenizer.pad_token_id = 0
    tokenizer.bos_token_id = 1
    tokenizer.eos_token_id = 2
    
    generate_for_single_csv(tokenizer, model, single_question_dataset, "single", dataframe)
    generate_for_single_csv(tokenizer, model, multi_question_dataset, "multi", dataframe)
    generate_for_single_csv(tokenizer, model, transfer_question_dataset, "transfer", dataframe)
    
    dataframe.to_csv("output/generated.csv", index=False)

def read_json(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(columns=["Fragen", "Umformuliert", "Antworten", "Anzahl_Antworten", "Quelle", "Kontext"])
    for item in data:
        df.loc[len(df)] = [item["Fragen"], item["Umformuliert"], item["Antworten"], item["Anzahl_Antworten"], item["Quelle"], item["Kontext"]]
    return df

def generate_for_single_csv(tokenizer: transformers.PreTrainedTokenizer | transformers.PreTrainedTokenizerFast, model, csv_df: pd.DataFrame, csv_type: str, output_df: pd.DataFrame):
    for index, row in csv_df.iterrows():
        print(f"{index}/{len(csv_df)} Questions")
        print(f"Generation {index}/{len(csv_df)}")
        question = row["Fragen"]
        transformed_question = row["Umformuliert"]
        true_answer = row["Antworten"]
        num_answers = row["Anzahl_Antworten"]
        source = row["Quelle"]
        context = row["Kontext"]
        
        if context != "":
            prompt = f"Instruction: You are given a question and a context. Answer the question to your best knowledge.\nQuestion: {transformed_question}\nContext: {context}\nAnswer: "
        else:
            prompt = f"Instruction: You are given a question. Answer the question to your best knowledge.\nQuestion: {transformed_question}\nAnswer: "
        
        print(prompt)
        inputs = tokenizer(prompt, return_tensors="pt")
        inputs = inputs.to(device)
        output = model.generate(inputs.input_ids, temperature=0.9, max_new_tokens=512)
        generated = tokenizer.batch_decode(output, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        generated = generated[len(prompt):]
        print(f"Generated: {generated}")
        output_df.loc[len(output_df)] = [question, transformed_question, generated, true_answer, num_answers, csv_type, source, context, prompt]

if __name__ == "__main__":
    main()
