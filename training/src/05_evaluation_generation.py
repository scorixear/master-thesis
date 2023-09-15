import json
import json_fix  # this import is needed for def __json__(self) although not used
import enum
import argparse

# import only system from os
from os import system, name


class AnswerType(enum.Enum):
    """Represents type of Answer the model gave

    Args:
        enum (int): The type of answer

    Returns:
        int: 0 = Not_Answered, 1 = Wrong_Answer, 2 = Correct_Answer
    """

    Not_Answered = 0
    Wrong_Answer = 1
    Correct_Answer = 2

    def __json__(self):
        return self.value


class Question:
    """Represent one question and their data"""

    def __init__(
        self,
        question,
        transformed,
        generated,
        true_answer,
        num_answers,
        q_type,
        source,
        context,
        true_input,
    ):
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
    # parse arguments
    parser = argparse.ArgumentParser(
        description="Evaluation of the generated questions"
    )
    # path to generated question json file
    parser.add_argument(
        "-d",
        "--data",
        type=str,
        help="Path to the generated questions",
        default="output/generated.json",
    )
    # path to json output file
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Path to the output file",
        default="output/evaluated.json",
    )
    args = parser.parse_args()
    # read in generated questions
    input_file = args.data
    with open(input_file, "r", encoding="utf-8") as json_file:
        generated_questions = json.load(json_file)

    # prompt for user
    print(
        "====================================================================================================="
    )
    print("Evaluation of the generated questions")
    print(
        "====================================================================================================="
    )
    print(
        " You are given a question, a context, the generated answer and the true answer.\n Compare the generated answer to the true answer.\n First you will be asked if the generated answer is in correlation to the question. Input 0 if no, 1 if yes.\n If you said 1 you will be asked if the answer is correct and how much.\n Each question has a number of answer associated. Input the number of correct answers / facts the generated answer contains."
    )
    print(f"Loaded {len(generated_questions)} questions")
    print(
        "====================================================================================================="
    )
    input("Press Enter to continue...")

    questions = []
    # for each question
    for index, item in enumerate(generated_questions):
        # clear the screen
        clear()
        # print progess
        print(f"Question {index+1}/{len(generated_questions)}")
        # extract question data
        question = item["question"]
        transformed = item["transformed"]
        generated = item["generated"]
        true_answer = item["true_answer"]
        number_of_answers = item["num_answers"]
        q_type = item["type"]
        source = item["source"]
        context = item["context"]
        true_input = item["true_input"]

        # create question object
        current_question = Question(
            question,
            transformed,
            generated,
            true_answer,
            number_of_answers,
            q_type,
            source,
            context,
            true_input,
        )
        questions.append(current_question)
        # print question data
        print(
            "====================================================================================================="
        )
        print(f"Question:\n{transformed}")
        print(
            "====================================================================================================="
        )
        print(f"Context:\n{context}")
        print(
            "====================================================================================================="
        )
        print(f"True Answer:\n{true_answer}")
        print(
            "====================================================================================================="
        )
        print(f"Number of Answers:\n{number_of_answers}")
        print(
            "====================================================================================================="
        )
        print(f"Generated Answer:\n{generated}")
        print(
            "====================================================================================================="
        )
        # ask if answer is correlated to question
        in_correlation = input(
            "Is this answer in correlation to the question? (Type 0 for no, 1 for yes)\n"
        )
        # if not correlated, set answer type to not answered and points to 0
        if in_correlation != "1":
            current_question.answered = AnswerType.Not_Answered
            current_question.points = 0
            continue
        # if correlated
        while True:
            # ask for points
            points_str = input(
                f"How many points would you give this answer? (0 = wrong answered, 1-{number_of_answers} points possible)\n"
            )
            # if 0 points, set answer type to wrong answer and points to 0
            if points_str == "0":
                current_question.answered = AnswerType.Wrong_Answer
                current_question.points = 0
                break
            # try parsing points to int
            points = int(points_str) if points_str.isdecimal() else None
            # if point are int
            if points is not None:
                # if points are not in range of 0 - number of answers, ask again
                if points > number_of_answers:
                    print(f"Please input a number between 0 and {number_of_answers}")
                    continue
                # else set answer type to correct answer and points to points
                current_question.answered = AnswerType.Correct_Answer
                current_question.points = points
                break
            # if points are not int, ask again
            else:
                print("Please input a number")
                continue
        print(
            "=====================================================================================================\n\n"
        )
    # save the questions
    save_questions(questions, args.output)


def save_questions(questions, output_file):
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(questions, json_file, indent=4, ensure_ascii=False)


def clear():
    """Clears terminal screen"""
    # for windows
    if name == "nt":
        _ = system("cls")
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system("clear")


if __name__ == "__main__":
    main()
