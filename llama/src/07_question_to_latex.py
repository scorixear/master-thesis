import argparse
import json

def replace_special_chars(text: str):
    return text.replace("&", "\\&").replace("^","\\^").replace("%","\\%").replace("$","\\$").replace("#","\\#").replace("_","\\_").replace("{","\\{").replace("}","\\}").replace("~","\\~").replace("<","\\textless").replace(">","\\textgreater").replace("|","\\textbar")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default="data/single_questions.json")
    parser.add_argument('--output', type=str, default="data/single_questions.tex")
    args = parser.parse_args()
    
    # load in question json file
    data = json.load(open(args.input, "r"))
    output_lines = []
    # for each question
    for question in data:
        # replace special characters
        # and append to output
        original = replace_special_chars(question['question'])
        output_lines.append(f"Frage & {original} \\\\")
        transformed = replace_special_chars(question['transformed'])
        output_lines.append(f"Umformuliert & {transformed} \\\\")
        context = replace_special_chars(question['context'])
        if context != "":
            output_lines.append(f"Kontext & {context} \\\\")
        true_answer = replace_special_chars(question['true_answer'])
        output_lines.append(f"Antwort & {true_answer} \\\\")
        source = replace_special_chars(question['source'])
        output_lines.append(f"Quelle & {source} \\\\")
        num_answers = question['num_answers']
        output_lines.append(f"Anz. Antw. & {num_answers} \\\\")
        
        
        output_lines.append("\\midrule")
    # then write to output file
    with open(args.output, 'w') as f:
        f.write("\n".join(output_lines))
if __name__ == '__main__':
    main()