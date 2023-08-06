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
                        default="evaluation/criterias/explainability")
    parser.add_argument("-o", "--output", type=str, help="Path to the output file", default="evaluation/criterias/explainability")
    args = parser.parse_args()
    
    models: dict[str, tuple[list[Question], list[Question]]] = {}
    
    for file in os.listdir(args.data):
        if file.endswith(".json"):
            if(file.endswith("_non_explained.json")):
                name = file[:-19]
                if(name not in models):
                    models[name] = ([], Question.read_json(os.path.join(args.data, file)))
                else:
                    models[name] = (models[name][0],Question.read_json(os.path.join(args.data, file)))
            else:
                name = file[:-15]
                if name not in models:
                    models[name] = (Question.read_json(os.path.join(args.data, file)), [])
                else:
                    models[name] = (Question.read_json(os.path.join(args.data, file)), models[name][0])
    
    explained = []
    non_explained = []
    
    for model in models.keys():
        explained.append(len(models[model][0]))
        non_explained.append(len(models[model][1]))
    explained_plot = {
        "Nicht Erklärt": np.array(non_explained),
        "Erklärt": np.array(explained),
    }
    
    fig = plt.figure(figsize=(20, 10))
    axis = fig.subplots()
    bottom = np.array([0] * len(models.keys()))
    colors = ["green", "grey"]
    model_names = list(models.keys())
    for boolean, answer in explained_plot.items():
        axis.bar(model_names, answer, width=0.5, label=boolean, bottom=bottom, color=colors.pop())
        bottom += answer
    axis.legend()
    axis.set_title("Anzahl der Antworten, die erklärt wurden")
    fig.savefig(os.path.join(args.output, "explained.png"))

if __name__ == "__main__":
    main()