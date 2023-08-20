import os
from question import Question
import argparse
import json_fix # this import is needed for def __json__(self) although not used
import matplotlib.pyplot as plt
import numpy as np
from model_helper import get_model_key, get_model_name

def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="Evaluation of the generated questions")
    # path to explainability generated json file directory
    parser.add_argument("-d", "--data", type=str, help="Path to the evaluated questions", 
                        default="evaluation/criterias/explainability")
    # path to output directory
    parser.add_argument("-o", "--output", type=str, help="Path to the output directory", default="evaluation/criterias/explainability")
    args = parser.parse_args()
    unsorted_models: dict[str, tuple[list[Question], list[Question]]] = {}
    models: dict[str, tuple[list[Question], list[Question]]] = {}
    # read in json files
    for file in os.listdir(args.data):
        # only read json files
        if file.endswith(".json"):
            name = get_model_name(file[:-5])
            # if file contains question not explained
            if(file.endswith("_not_explained.json")):
                # if model name not in models, add model name and questions not explained
                if(name not in unsorted_models):
                    unsorted_models[name] = ([], Question.read_json(os.path.join(args.data, file)))
                # otherwise add questions not explained to model
                else:
                    unsorted_models[name] = (unsorted_models[name][0],Question.read_json(os.path.join(args.data, file)))
            # if file ends with _explained.json
            else:
                # if model name not in models, add model name and questions explained
                if name not in unsorted_models:
                    unsorted_models[name] = (Question.read_json(os.path.join(args.data, file)), [])
                # otherwise add questions explained to model
                else:
                    unsorted_models[name] = (Question.read_json(os.path.join(args.data, file)), unsorted_models[name][1])
    # sort models by key
    for key in sorted(unsorted_models.keys(), key=get_model_key):
        models[key] = unsorted_models[key]
    
    explained = []
    not_explained = []
    
    single_not_explained = []
    single_explained = []
    multi_not_explained = []
    multi_explained = []
    transfer_not_explained = []
    transfer_explained = []
    
    # for each model, get number of explained and not explained questions
    for (name, (explained_q, not_explained_q)) in models.items():
        explained.append(len(explained_q))
        not_explained.append(len(not_explained_q))
        (single_exp, multi_exp, transfer_exp) = count_type_questions(explained_q)
        (single_not_exp, multi_not_exp, transfer_not_exp) = count_type_questions(not_explained_q)
        single_not_explained.append(single_not_exp)
        single_explained.append(single_exp)
        multi_not_explained.append(multi_not_exp)
        multi_explained.append(multi_exp)
        transfer_not_explained.append(transfer_not_exp)
        transfer_explained.append(transfer_exp)
    
    create_plot(list(models.keys()), explained, not_explained, "Anzahl der Fragen, die erklärt wurden", os.path.join(args.output, "explained.png"))
    create_plot(list(models.keys()), single_explained, single_not_explained, "Anzahl der Einzel-Fakt Fragen, die erklärt wurden", os.path.join(args.output, "explained_single.png"))
    create_plot(list(models.keys()), multi_explained, multi_not_explained, "Anzahl der Multi-Fakten Fragen, die erklärt wurden", os.path.join(args.output, "explained_multi.png"))
    create_plot(list(models.keys()), transfer_explained, transfer_not_explained, "Anzahl der Transferfragen, die erklärt wurden", os.path.join(args.output, "explained_transfer.png"))

def create_plot(model_names: list[str], explained: list[int], not_explained: list[int], title: str, file_path: str):
 
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
    bottom = np.zeros(len(model_names))
    # and colors backwards
    colors = ["silver", "green"]
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
    axis.set_title(title, pad=15)
    # and save figure
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