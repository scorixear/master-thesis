import argparse
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default="data/single_questions.json")
    parser.add_argument('--output', type=str, default="data/single_questions.tex")
    args = parser.parse_args()
    
    data = json.load(open(args.input, "r"))
    output_lines = []
    for question in data:
        original = question['question']
        transformed = question['transformed']
        true_answer = question['true_answer']
        num_answers = question['num_answers']
        source = question['source']
        context = question['context']
        
        if context == "":
            context = "-"
        output_lines.append(f"{original} & {source} & {num_answers} & {transformed} & {context} & {true_answer} \\\\")
    with open(args.output, 'w', encoding="UTF-8") as f:
        f.write("\n".join(output_lines))
if __name__ == '__main__':
    main()