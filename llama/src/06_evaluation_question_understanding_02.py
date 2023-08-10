import os
from question import Question
import argparse
import json_fix # this import is needed for def __json__(self) although not used
import matplotlib.pyplot as plt
import numpy as np

def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="Evaluation of the generated questions")
    # path to question understanding generated json file directory
    parser.add_argument("-d", "--data", type=str, help="Path to the evaluated questions", 
                        default="evaluation/criterias/question_understanding")
    # path to output directory
    parser.add_argument("-o", "--output", type=str, help="Path to the output directory", default="evaluation/criterias/question_understanding")
    args = parser.parse_args()
    
    
    models: dict[str, tuple[list[Question], list[Question]]] = {}
    # for each file in data directory
    for file in os.listdir(args.data):
        # only read json files
        if file.endswith(".json"):
            # if file contains question not understood
            if(file.endswith("_not_understood.json")):
                # remove _not_understood.json to get model name
                name = file[:-20]
                # if model name not in models, add model name and questions not understood
                if(name not in models):
                    models[name] = ([], Question.read_json(os.path.join(args.data, file)))
                # otherwise add questions not understood to model
                else:
                    models[name] = (models[name][0],Question.read_json(os.path.join(args.data, file)))
            # if file ends with _understood.json
            else:
                # remove _understood.json to get model name
                name = file[:-16]
                # if model name not in models, add model name and questions understood
                if name not in models:
                    models[name] = (Question.read_json(os.path.join(args.data, file)), [])
                # otherwise add questions understood to model
                else:
                    models[name] = (Question.read_json(os.path.join(args.data, file)), models[name][1])
    
    understood = []
    not_understood = []
    # for each model, get number of understood and not understood questions
    for model in models.keys():
        understood.append(len(models[model][0]))
        not_understood.append(len(models[model][1]))
    # create dataset for stacked bars
    understood_plot = {
        "Verstanden": np.array(understood),
        "Nicht Verstanden": np.array(not_understood),
    }
    # create figure of size 20, 10
    fig = plt.figure(figsize=(20, 10))
    # subplots() to get axis object
    axis = fig.subplots()
    # bottom array for stacked bars
    bottom = np.zeros(len(models.keys()))
    # colors of stacked bars in reverse order
    colors = ["silver", "green"]
    model_names = list(models.keys())
    # for each label and data in dataset
    for labels, data in understood_plot.items():
        # plot bars
        bars = axis.bar(model_names, data, width=0.5, label=labels, bottom=bottom, color=colors.pop())
        # set bar labels
        axis.bar_label(bars)
        # and stack next bar on top
        bottom += data
    axis.legend()
    # set y-axis legend
    axis.set_ylabel("Anzahl der Fragen")
    # set title and  padding as bar labels might overlap
    axis.set_title("Anzahl der Fragen, die verstanden wurden", pad=15)
    # and save the figure
    fig.savefig(os.path.join(args.output, "understood.png"))

if __name__ == "__main__":
    main()