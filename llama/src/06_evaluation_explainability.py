import json
import os
# import only system from os
from os import system, name
from question import Question
import argparse
import json_fix
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description="Evaluation of the generated questions")
    parser.add_argument("-d", "--data", type=str, help="Path to the evaluated questions", 
                        default="evaluation/input/llama2_0e.json")
    parser.add_argument("-o", "--output", type=str, help="Path to the output file", default="evaluation/criterias/explainability/llama2_0e")
    args = parser.parse_args()
    
    model_name = args.data.split("/")[-1][:-5]
    model = Question.read_json(args.data)
    
    print("=====================================================================================================")
    print("Evaluation of the generated questions - Explainability")
    print("=====================================================================================================")
    print(" You are given a question, a context, the generated answer and the true answer.\n The answers generated are correct to some extent. Decide if the provided answer contains an explaination.\n Input 1 if the answer contains an explaination, 0 otherwise.")
    print(f"Loaded {len(model)} Questions")
    print(f"Model: {model_name}")
    print("=====================================================================================================")
    input("Press Enter to continue...")
    
    clear()
    explained = []
    non_explained = []
    for q_i, question in enumerate(model):
        if(question.answered != 2):
            continue
        print("=======================================")
        print(f"Question {q_i+1}/{len(model)}")
        print(question.transformed)
        print("=======================================")
        print("Context")
        print(question.context)
        print("=======================================")
        print("True Answer")
        print(question.true_answer)
        print("=======================================")
        print("Generated Answer")
        print(question.generated)
        print("=======================================")
        explaination = input("Explanation? (1/0)\n")
        if explaination == "0":
            non_explained.append(question)
        else:
            explained.append(question)
        clear()
    
    json.dump(explained, open(f"{args.output}_explained.json", "w", encoding="utf-8"), indent=4, ensure_ascii=False)
    json.dump(non_explained, open(f"{args.output}_non_explained.json", "w", encoding="utf-8"), indent=4, ensure_ascii=False)
    
    
        
# define our clear function
def clear():
 
    # for windows
    if name == 'nt':
        _ = system('cls')
 
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

if __name__ == "__main__":
    main()