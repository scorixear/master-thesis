import json
from os import system, name
from question import Question
import argparse
import json_fix # this import is needed for def __json__(self) although not used

def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="Evaluation of the generated questions")
    # path to evaluated question json file
    parser.add_argument("-d", "--data", type=str, help="Path to the evaluated questions", 
                        default="evaluation/input/llama2_0e.json")
    # path to json output file (only start of the name, _explained.json and _not_explained.json will be added)
    parser.add_argument("-o", "--output", type=str, help="Path to the output file", default="evaluation/criterias/explainability/llama2_0e")
    args = parser.parse_args()
    
    # get model name
    model_name = args.data.split("/")[-1][:-5]
    # and read in evaluated questions
    model = Question.read_json(args.data)
    
    # print prompt for user
    print("=====================================================================================================")
    print("Evaluation of the generated questions - Explainability")
    print("=====================================================================================================")
    print(" You are given a question, a context, the generated answer and the true answer.\n The answers generated are correct to some extent. Decide if the provided answer contains an explaination.\n Input 1 if the answer contains an explaination, 0 otherwise.")
    print(f"Loaded {len(model)} Questions")
    print(f"Model: {model_name}")
    print("=====================================================================================================")
    input("Press Enter to continue...")
    
    # clear the screen
    clear()
    explained = []
    non_explained = []
    # for each question
    for q_i, question in enumerate(model):
        # we only look at correctly answered questions
        if(question.answered != 2):
            continue
        # print progess and question data
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
        # let the user decide if the answer contains an explaination
        explaination = input("Explanation? (1/0)\n")
        if explaination == "0":
            non_explained.append(question)
        else:
            explained.append(question)
        clear()
    # and save the results
    with open(f"{args.output}_explained.json", "w", encoding="utf-8") as f:
        json.dump(explained, f, indent=4, ensure_ascii=False)
    with  open (f"{args.output}_not_explained.json", "w", encoding="utf-8") as f:
        json.dump(non_explained, f, indent=4, ensure_ascii=False)
    
def clear():
    """Clears terminal screen
    """
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

if __name__ == "__main__":
    main()