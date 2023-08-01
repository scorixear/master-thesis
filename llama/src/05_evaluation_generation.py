import json
import json_fix
import enum
import sys

# import only system from os
from os import system, name

class AnswerType(enum.Enum):
    Not_Answered = 0
    Wrong_Answer = 1
    Correct_Answer = 2
    def __json__(self):
        return self.value


class Question:
    def __init__(self, question, transformed, generated, true_answer, num_answers, q_type, source, context, true_input):
        self.question = question
        self.transformed = transformed
        self.generated = generated
        self.true_answer = true_answer
        self.num_answers = num_answers
        self.type = q_type
        self.source = source
        self.context = context
        self.true_input = true_input
        self.answered = AnswerType.Not_Answered
        self.points: int = 0
    def __json__(self):
        return self.__dict__

def main():
    input_file = "output/generated.json"
    if len(sys.argv) > 2:
        if sys.argv[1] == "--data":
            input_file = sys.argv[2]
    with open(input_file, "r", encoding="utf-8") as json_file:
        generated_questions = json.load(json_file)
    
    print("=====================================================================================================")
    print("Evaluation of the generated questions")
    print("=====================================================================================================")
    print(" You are given a question, a context, the generated answer and the true answer.\n Compare the generated answer to the true answer.\n First you will be asked if the generated answer is in correlation to the question. Input 0 if no, 1 if yes.\n If you said 1 you will be asked if the answer is correct and how much.\n Each question has a number of answer associated. Input the number of correct answers / facts the generated answer contains.")
    print(f"Loaded {len(generated_questions)} questions")
    print("=====================================================================================================")
    input("Press Enter to continue...")
    questions = []
    for index, item in enumerate(generated_questions):
        clear()
        print(f"Question {index+1}/{len(generated_questions)}")
        question = item["Question"]
        transformed = item["Transformed"]
        generated = item["Generated"]
        true_answer = item["True_Answer"]
        number_of_answers = item["Num_Answers"]
        q_type = item["Type"]
        source = item["Source"]
        context = item["Context"]
        true_input = item["True_Input"]
        
        current_question = Question(question, transformed, generated, true_answer, number_of_answers, q_type, source, context, true_input)
        questions.append(current_question)
        print("=====================================================================================================")
        print(f"Question:\n{transformed}")
        print("=====================================================================================================")
        print(f"Context:\n{context}")
        print("=====================================================================================================")
        print(f"True Answer:\n{true_answer}")
        print("=====================================================================================================")
        print(f"Number of Answers:\n{number_of_answers}")
        print("=====================================================================================================")
        print(f"Generated Answer:\n{generated}")
        print("=====================================================================================================")
        
        in_correlation = input("Is this answer in correlation to the question? (Type 0 for no, 1 for yes)\n")
        if in_correlation != "1":
            current_question.answered = AnswerType.Not_Answered
            current_question.points = 0
            continue
        while True:
            points_str = input(f"How many points would you give this answer? (0 = wrong answered, 1-{number_of_answers} points possible)\n")
            if points_str == "0":
                current_question.answered = AnswerType.Wrong_Answer
                current_question.points = 0
                break
            points = int(points_str) if points_str.isdecimal() else None
            if points is not None:
                if points > number_of_answers:
                    print(f"Please input a number between 0 and {number_of_answers}")
                    continue
                current_question.answered = AnswerType.Correct_Answer
                current_question.points = points
                break
            else:
                print("Please input a number")
                continue
        print("=====================================================================================================\n\n")
    save_questions(questions)
def save_questions(questions):
    with open("output/evaluated.json", "w", encoding="utf-8") as json_file:
        json.dump(questions, json_file, indent=4, ensure_ascii=False)
        
        

 
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