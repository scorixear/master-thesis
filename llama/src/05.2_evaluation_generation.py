import json
from os import system, name
import json_fix
import argparse


class Question:
    def __init__(self, question, transformed, generated, true_answer, num_answers, q_type, source, context, true_input, answered, points):
        self.question = question
        self.transformed = transformed
        self.generated = generated
        self.true_answer = true_answer
        self.num_answers = num_answers
        self.type = q_type
        self.source = source
        self.context = context
        self.true_input = true_input
        self.answered = answered
        self.points: int = points
        self.total_answers = 0
    def __json__(self):
        return self.__dict__

def main():
    parser = argparse.ArgumentParser(description="Evaluation of the generated questions")
    parser.add_argument("-d", "--data", type=str, help="Path to the evaluated questions", 
                        default="output/evaluated.json")
    parser.add_argument("-o", "--output", type=str, help="Path to the output file", default="output/evaluated.json")
    args = parser.parse_args()
    input_file = args.data
    with open(input_file, "r", encoding="utf-8") as json_file:
        evaluated_questions = json.load(json_file)
        
    print("=====================================================================================================")
    print("2nd Evaluation of the generated questions")
    print("=====================================================================================================")
    print("You are given a question, a context, the generated answer, the true answer and the amount of expected answers.\nPlease input how many answers are given in general.\nIt is not important if the answers are correct or not.")
    print(f"Loaded {len(evaluated_questions)} questions")
    print("=====================================================================================================")
    input("Press Enter to continue...")
    questions = []
    for index, item in enumerate(evaluated_questions):
        clear()
        print(f"Question {index+1}/{len(evaluated_questions)}")
        question = item["question"]
        transformed = item["transformed"]
        generated = item["generated"]
        true_answer = item["true_answer"]
        num_answers = item["num_answers"]
        q_type = item["type"]
        source= item["source"]
        context= item["context"]
        true_input= item["true_input"]
        answered= item["answered"]
        points= item["points"]
        
        current_question = Question(question, transformed, generated, true_answer, num_answers, q_type, source, context, true_input, answered, points)
        questions.append(current_question)
        
        if(answered == 0):
            current_question.total_answers = 0
            continue
        print("=====================================================================================================")
        print(f"Question:\n{transformed}")
        print("=====================================================================================================")
        print(f"Context:\n{context}")
        print("=====================================================================================================")
        print(f"True Answer:\n{true_answer}")
        print("=====================================================================================================")
        print(f"Number of Answers:\n{num_answers}")
        print("=====================================================================================================")
        print(f"Generated Answer:\n{generated}")
        print("=====================================================================================================")
        while True:
            total_answers = input("How many answers are given in general?\n")
            total_answers = int(total_answers) if total_answers.isdecimal() else None
            if total_answers is not None:
                if total_answers < 0:
                    print("Please enter a positive number")
                    continue
                current_question.total_answers = total_answers
                break
            else:
                print("Please enter a number")
                continue
        print("=====================================================================================================")
    save_questions(questions, args.output)
def save_questions(questions, output_file):
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(questions, json_file, indent=4, ensure_ascii=False)

def clear():
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")

if __name__ == "__main__":
    main()
    

        
        
        