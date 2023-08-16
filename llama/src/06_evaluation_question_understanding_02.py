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
    single_understood = []
    single_not_understood = []
    multi_understood = []
    multi_not_understood = []
    transfer_understood = []
    transfer_not_understood = []
    # for each model, get number of understood and not understood questions
    for (name, (understood_q, not_understood_q)) in models.items():
        understood.append(len(understood_q))
        not_understood.append(len(not_understood_q))
        (single_u, multi_u, transfer_u) = count_type_questions(understood_q)
        (single_n, multi_n, transfer_n) = count_type_questions(not_understood_q)
        single_understood.append(single_u)
        single_not_understood.append(single_n)
        multi_understood.append(multi_u)
        multi_not_understood.append(multi_n)
        transfer_understood.append(transfer_u)
        transfer_not_understood.append(transfer_n)
    
    create_plot(list(models.keys()), understood, not_understood, "Verstandene Fragen", os.path.join(args.output, "understood.png"))
    create_plot(list(models.keys()), single_understood, single_not_understood, "Verstandene Einzel-Fakt Fragen", os.path.join(args.output, "understood_single.png"))
    create_plot(list(models.keys()), multi_understood, multi_not_understood, "Verstandene Multi-Fakten Fragen", os.path.join(args.output, "understood_multi.png"))
    create_plot(list(models.keys()), transfer_understood, transfer_not_understood, "Verstandene Transferfragen", os.path.join(args.output, "understood_transfer.png"))

def create_plot(model_names: list[str], understood: list[int], not_understood: list[int], title: str, file_path: str):
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
    bottom = np.zeros(len(model_names))
    # colors of stacked bars in reverse order
    colors = ["silver", "green"]
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
    axis.set_title(title, pad=15)
    # and save the figure
    fig.savefig(file_path)

def count_type_questions(questions: list[Question]) -> tuple[int, int, int]:
    single = 0
    multi = 0
    transfer = 0
    for question in questions:
        if question.type == "single":
            single += 1
        elif question.type == "multi":
            multi += 1
        elif question.type == "transfer":
            transfer += 1
    return (single, multi, transfer)

if __name__ == "__main__":
    main()