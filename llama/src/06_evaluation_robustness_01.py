import argparse
import os
import json

from helper.question import Question, QuestionType

def main():
    parser = argparse.ArgumentParser(description="Generation of Spelling Questions")
    parser.add_argument("-e", "--evaluated", type=str, default="output/evaluated_1e.json",
                        help="Path to the evaluated questions")
    parser.add_argument("-s", "--source", type=str, default="data/spelling.json",
                        help="Path to the misspelled questions")
    parser.add_argument("-o", "--output", type=str, default="data/",
                        help="Path to the output directory")
    parser.add_argument("-n", "--name", type=str, default="llama2_1e",
                        help="Name of the model")
    args = parser.parse_args()

    evaluated_questions = Question.read_json(args.evaluated)
    source_questions_list = Question.read_json(args.source)
    source_questions: dict[str, Question] = { }
    for question in source_questions_list:
        source_questions[question.question] = question
    output_questions: dict[QuestionType, list[Question]] = {}
    for q_type in QuestionType:
        output_questions[q_type] = []
    for question in evaluated_questions:
        if question.answered == 2:
            if(question.question in source_questions):
                output_questions[QuestionType(question.type)].append( # type: ignore
                    source_questions[question.question])
    for q_type in QuestionType:
        with open(os.path.join(args.output, f"{q_type}_questions_spelling_{args.name}.json"),
                  "w", encoding="UTF-8") as f:
            json.dump(output_questions[q_type], f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
