import os
from question import Question
import argparse
import json_fix # this import is needed for def __json__(self) although not used
import matplotlib.pyplot as plt
import numpy as np

def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="Evaluation of the generated questions")
    # path to explainability generated json file directory
    parser.add_argument("-d", "--data", type=str, help="Path to the evaluated questions", 
                        default="evaluation/criterias/explainability")
    # path to output directory
    parser.add_argument("-o", "--output", type=str, help="Path to the output directory", default="evaluation/criterias/explainability")
    args = parser.parse_args()
    
    models: dict[str, tuple[list[Question], list[Question]]] = {}
    # read in json files
    for file in os.listdir(args.data):
        # only read json files
        if file.endswith(".json"):
            # if file contains question not explained
            if(file.endswith("_not_explained.json")):
                # remove _not_explained.json to get model name
                name = file[:-19]
                # if model name not in models, add model name and questions not explained
                if(name not in models):
                    models[name] = ([], Question.read_json(os.path.join(args.data, file)))
                # otherwise add questions not explained to model
                else:
                    models[name] = (models[name][0],Question.read_json(os.path.join(args.data, file)))
            # if file ends with _explained.json
            else:
                # remove _explained.json to get model name
                name = file[:-15]
                # if model name not in models, add model name and questions explained
                if name not in models:
                    models[name] = (Question.read_json(os.path.join(args.data, file)), [])
                # otherwise add questions explained to model
                else:
                    models[name] = (Question.read_json(os.path.join(args.data, file)), models[name][1])
    
    explained = []
    not_explained = []
    # for each model, get number of explained and not explained questions
    for model in models.keys():
        explained.append(len(models[model][0]))
        not_explained.append(len(models[model][1]))
    # create stacked bars dataset
    explained_plot = {
        "Erklärt": np.array(explained),
        "Nicht Erklärt": np.array(not_explained),
    }
    
    # figure of size 20, 10
    fig = plt.figure(figsize=(20, 10))
    # subplots() to get axis object
    axis = fig.subplots()
    # create bottom array for stacked bars
    bottom = np.zeros(len(models.keys()))
    # and colors backwards
    colors = ["silver", "green"]
    model_names = list(models.keys())
    # for each label and data in explained_plot
    for labels, data in explained_plot.items():
        # create bars
        bars = axis.bar(model_names, data, width=0.5, label=labels, bottom=bottom, color=colors.pop())
        # set bar labels
        axis.bar_label(bars)
        # and stack next bars on top
        bottom += data
    axis.legend()
    # set y-axis legend
    axis.set_ylabel("Anzahl der Antworten")
    # set title with padding, ad bar_labels might overlap
    axis.set_title("Anzahl der Antworten, die erklärt wurden", pad=15)
    # and save figure
    fig.savefig(os.path.join(args.output, "explained.png"))

if __name__ == "__main__":
    main()