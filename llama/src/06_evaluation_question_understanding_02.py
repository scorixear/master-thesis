import json
import os
from question import Question
import argparse
import json_fix
import matplotlib.pyplot as plt
import numpy as np

def main():
    parser = argparse.ArgumentParser(description="Evaluation of the generated questions")
    parser.add_argument("-d", "--data", type=str, help="Path to the evaluated questions", 
                        default="evaluation/criterias/question_understanding")
    parser.add_argument("-o", "--output", type=str, help="Path to the output file", default="evaluation/criterias/question_understanding")
    args = parser.parse_args()
    
    models: dict[str, tuple[list[Question], list[Question]]] = {}
    
    for file in os.listdir(args.data):
        if file.endswith(".json"):
            if(file.endswith("_not_understood.json")):
                name = file[:-20]
                if(name not in models):
                    models[name] = ([], Question.read_json(os.path.join(args.data, file)))
                else:
                    models[name] = (models[name][0],Question.read_json(os.path.join(args.data, file)))
            else:
                name = file[:-16]
                if name not in models:
                    models[name] = (Question.read_json(os.path.join(args.data, file)), [])
                else:
                    models[name] = (Question.read_json(os.path.join(args.data, file)), models[name][1])
    
    understood = []
    not_understood = []
    
    for model in models.keys():
        understood.append(len(models[model][0]))
        not_understood.append(len(models[model][1]))
    understood_plot = {
        "Nicht Verstanden": np.array(not_understood),
        "Verstamdem": np.array(understood),
    }
    
    fig = plt.figure(figsize=(20, 10))
    axis = fig.subplots()
    bottom = np.array([0] * len(models.keys()))
    colors = ["green", "grey"]
    model_names = list(models.keys())
    for boolean, answer in understood_plot.items():
        bars = axis.bar(model_names, answer, width=0.5, label=boolean, bottom=bottom, color=colors.pop())
        axis.bar_label(bars)
        bottom += answer
    axis.legend()
    axis.set_title("Anzahl der Fragen, die verstanden wurden")
    fig.savefig(os.path.join(args.output, "understood.png"))

if __name__ == "__main__":
    main()