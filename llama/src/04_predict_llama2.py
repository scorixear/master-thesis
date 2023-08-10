import json
import sys
import logging
import argparse

import pandas as pd
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# use CUDA / GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# init logger
logger = logging.getLogger(__name__)

def main():
    # parse arguments
    parser = argparse.ArgumentParser()
    # for trained model as files
    parser.add_argument("-m", "--model-dir", type=str, default="./trained/7B", help="Path to the model directory")
    # file path for generated answers 
    parser.add_argument("-o", "--output-path", type=str, default="./output/generated.csv", help="Path to the output file")
    
    args = parser.parse_args()
    # setup logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    
    # set logging verbosity to info
    transformers.utils.logging.set_verbosity_info()
    
    log_level = logging.INFO
    logger.setLevel(log_level)
    transformers.utils.logging.set_verbosity(log_level)
    transformers.utils.logging.enable_default_handler()
    transformers.utils.logging.enable_explicit_format()
    
    # read in questions from json files
    single_question_dataset = read_json("data/single_questions.json")
    multi_question_dataset = read_json("data/multi_questions.json")
    transfer_question_dataset = read_json("data/transfer_questions.json")
    
    # setup datafram for output
    dataframe = pd.DataFrame(columns=["question", "transformed", "generated", "true_answer", "num_answers", "type", "source", "context", "true_input"])
    
    model_dir = args.model_dir
    output_file = args.output_path
    
    print("Loading Model from", model_dir)
    print("Saving output to", output_file)
    
    # load in model and port to device
    model = AutoModelForCausalLM.from_pretrained(model_dir)
    model = model.to(device)
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    
    # introduce special tokens
    tokenizer.pad_token_id = 0
    tokenizer.bos_token_id = 1
    tokenizer.eos_token_id = 2
    
    # generate answers per question file
    generate_for_single_csv(tokenizer, model, single_question_dataset, "single", dataframe)
    generate_for_single_csv(tokenizer, model, multi_question_dataset, "multi", dataframe)
    generate_for_single_csv(tokenizer, model, transfer_question_dataset, "transfer", dataframe)
    
    # and save the results
    dataframe.to_csv(output_file, index=False)

def read_json(file):
    # reas in json file
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    # and dump into dataframe
    df = pd.DataFrame(columns=["question", "transformed", "true_answer", "num_answers", "source", "context"])
    for item in data:
        df.loc[len(df)] = [item["question"], item["transformed"], item["true_answer"], item["num_answers"], item["source"], item["context"]]
    return df

def generate_for_single_csv(tokenizer: transformers.PreTrainedTokenizer | transformers.PreTrainedTokenizerFast, model, csv_df: pd.DataFrame, csv_type: str, output_df: pd.DataFrame):
    # for each question in the question file
    for index, row in csv_df.iterrows():
        # log progress
        print(f"{index}/{len(csv_df)} Questions")
        print(f"Generation {index}/{len(csv_df)}")
        # extract question data
        question = row["question"]
        transformed_question = row["transformed"]
        true_answer = row["true_answer"]
        num_answers = row["num_answers"]
        source = row["source"]
        context = row["context"]
        
        # generate prompt depending on whether context is given
        if context != "":
            prompt = f"Instruction: You are given a question and a context. Answer the question to your best knowledge.\nQuestion: {transformed_question}\nContext: {context}\nAnswer: "
        else:
            prompt = f"Instruction: You are given a question. Answer the question to your best knowledge.\nQuestion: {transformed_question}\nAnswer: "
        
        print(prompt)
        # tokenize the prompt and port to device
        inputs = tokenizer(prompt, return_tensors="pt")
        inputs = inputs.to(device)
        # generate answers, temperature is doing nothing here?
        output = model.generate(inputs.input_ids, temperature=0.9, max_new_tokens=512)
        # decode the output
        generated = tokenizer.batch_decode(output, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        generated = generated[len(prompt):]
        print(f"Generated: {generated}")
        # and save to dataframe
        output_df.loc[len(output_df)] = [question, transformed_question, generated, true_answer, num_answers, csv_type, source, context, prompt]

if __name__ == "__main__":
    main()
