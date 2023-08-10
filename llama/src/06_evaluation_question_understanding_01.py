from os import system, name
from question import Question
import argparse
import json_fix # this import is needed for def __json__(self) although not used
import json


def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="Evaluation of the generated questions")
    # path to evaluated question json file
    parser.add_argument("-d", "--data", type=str, help="Path to the evaluated questions",
                        default="evaluation/input/llama2_0e.json")
    # path to json output file, _understood.json and _not_understood.json will be appended
    parser.add_argument("-o", "--output", type=str, help="Path to the output file", default="evaluation/criterias/question_understanding/llama2_0e")
    args = parser.parse_args()
    
    # get model name
    model_name = args.data.split("/")[-1][:-5]
    # and read in evaluated questions
    model = Question.read_json(args.data)
    
    # print user prompt
    print("=====================================================================================================")
    print("Evaluation of the generated questions - Question Understanding")
    print("=====================================================================================================")
    print(" You are given a question, a context, the generated answer and the true answer.\n The answers are wrong or correct. Decide if the model understood the question.\n Input 1 if the question is understood, 0 otherwise.")
    print(f"Loaded {len(model)} Questions")
    print(f"Model: {model_name}")
    print("=====================================================================================================")
    input("Press Enter to continue...")
    
    # clear the screen
    clear()
    understood = []
    not_understood = []
    # fpr each question
    for q_i, question in enumerate(model):
        # we skip unanswered questions
        if question.answered == 0:
            not_understood.append(question)
            continue
        # print progress and question data
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
        # let the user decide if the question is understood by the model
        understood_answer = input("Understood? (1/0)\n")
        if understood_answer == "0":
            not_understood.append(question)
        else:
            understood.append(question)
        clear()
    # and save the file
    with open(f"{args.output}_understood.json", "w", encoding="utf-8") as f:
        json.dump(understood, f, indent=4, ensure_ascii=False)
    with open (f"{args.output}_not_understood.json", "w", encoding="utf-8") as f:
        json.dump(not_understood, f, indent=4, ensure_ascii=False)

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