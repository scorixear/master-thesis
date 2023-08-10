import json
from os import system, name
import json_fix  # this import is needed for def __json__(self) although not used
import argparse


class Question:
    """Represent one question and their data
    """
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
    # parse arguments
    parser = argparse.ArgumentParser(description="Evaluation of the generated questions")
    # path to evaluated question json file
    parser.add_argument("-d", "--data", type=str, help="Path to the evaluated questions", 
                        default="output/evaluated.json")
    # path to json output file
    parser.add_argument("-o", "--output", type=str, help="Path to the output file", default="output/evaluated.json")
    args = parser.parse_args()
    # read in evaluated questions
    input_file = args.data
    with open(input_file, "r", encoding="utf-8") as json_file:
        evaluated_questions = json.load(json_file)
    # print starting screen
    print("=====================================================================================================")
    print("2nd Evaluation of the generated questions")
    print("=====================================================================================================")
    print("You are given a question, a context, the generated answer, the true answer and the amount of expected answers.\nPlease input how many answers are given in general.\nIt is not important if the answers are correct or not.")
    print(f"Loaded {len(evaluated_questions)} questions")
    print("=====================================================================================================")
    input("Press Enter to continue...")
    questions = []
    # for each question
    for index, item in enumerate(evaluated_questions):
        # clear the screen
        clear()
        # print progess
        print(f"Question {index+1}/{len(evaluated_questions)}")
        # extract question data
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
        
        # create question object
        current_question = Question(question, transformed, generated, true_answer, num_answers, q_type, source, context, true_input, answered, points)
        questions.append(current_question)
        
        # if the question could not be answered by model, skip it
        if(answered == 0):
            current_question.total_answers = 0
            continue
        # print question data
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
            # get total amount of answers contained in generated answer
            total_answers = input("How many answers are given in general?\n")
            # try parsing int
            total_answers = int(total_answers) if total_answers.isdecimal() else None
            # if total_answers is int
            if total_answers is not None:
                # but below 0, get again
                if total_answers < 0:
                    print("Please enter a positive number")
                    continue
                # otherwise set
                current_question.total_answers = total_answers
                break
            # if total_answers is not int, get again
            else:
                print("Please enter a number")
                continue
        print("=====================================================================================================")
    # and save the questions
    save_questions(questions, args.output)
def save_questions(questions, output_file):
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(questions, json_file, indent=4, ensure_ascii=False)

def clear():
    """Clears terminal screen
    """
    # for windows
    if name == "nt":
        _ = system("cls")
    # for mac, linux
    else:
        _ = system("clear")

if __name__ == "__main__":
    main()
    

        
        
        