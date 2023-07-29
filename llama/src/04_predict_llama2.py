import sys
import logging

import pandas as pd
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer

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
    
    single_question_dataset = pd.read_csv("data/single_questions.csv")
    multi_question_dataset = pd.read_csv("data/multi_questions.csv")
    transfer_question_dataset = pd.read_csv("data/transfer_questions.csv")
    
    dataframe = pd.DataFrame(columns=["Question", "Transformed", "Generated_1", "Generated_2", "Generated_3", "True_Answer", "Num_Answers", "Type", "Source", "Context", "True_Input"])
    
    model_dir = "./trained/7B"
    
    model = AutoModelForCausalLM.from_pretrained(model_dir)
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    
    tokenizer.pad_token_id = 0
    tokenizer.bos_token_id = 1
    tokenizer.eos_token_id = 2
    
    generate_for_single_csv(tokenizer, model, single_question_dataset, "single", dataframe)
    generate_for_single_csv(tokenizer, model, multi_question_dataset, "multi", dataframe)
    generate_for_single_csv(tokenizer, model, transfer_question_dataset, "transfer", dataframe)
    
    dataframe.to_csv("output/generated.csv", index=False)
    
def generate_for_single_csv(tokenizer: transformers.PreTrainedTokenizer | transformers.PreTrainedTokenizerFast, model, csv_df: pd.DataFrame, csv_type: str, output_df: pd.DataFrame):
    for index, row in csv_df.iterrows():
        print(f"Generation {index}/{len(csv_df)}")
        question = row["Fragen"]
        transformed_question = row["Umformuliert"]
        true_answer = row["Antworten"]
        num_answers = row["Anzahl_Antworten"]
        source = row["Quelle"]
        context = row["Kontext"]
        
        if context != "":
            input = f"Instruction: You are given a question and a context. Answer the question to your best knowledge.\nQuestion: {question}\nContext: {context}\nAnswer: "
        else:
            input = f"Instruction: You are given a question. Answer the question to your best knowledge.\nQuestion: {question}\nAnswer: "
        
        input_ids = tokenizer.encode(input, return_tensors="pt")
        output = model.generate(input=input_ids, temperature=0.9, max_new_tokens=512)
        generated_1 = tokenizer.decode(output[0])
        
        output = model.generate(input=input_ids, temperature=0.9, max_new_tokens=512)
        generated_2 = tokenizer.decode(output[0])
        
        output = model.generate(input=input_ids, temperature=0.9, max_new_tokens=512)
        generated_3 = tokenizer.decode(output[0])
        
        output_df.loc[len(output_df)] = [question, transformed_question, generated_1, generated_2, generated_3, true_answer, num_answers, csv_type, source, context, input]


        
        
        
        
    