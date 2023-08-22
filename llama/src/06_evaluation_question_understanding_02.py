import os
from question import Question, QuestionType, QuestionSource
import argparse
import matplotlib.pyplot as plt
import numpy as np

from model_helper import get_model_key, get_model_name

def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="Evaluation of the generated questions")
    # path to question understanding generated json file directory
    parser.add_argument("-d", "--data", type=str, help="Path to the evaluated questions", 
                        default="evaluation/criterias/question_understanding")
    # path to output directory
    parser.add_argument("-o", "--output", type=str, help="Path to the output directory", default="evaluation/criterias/question_understanding")
    args = parser.parse_args()
    
    unsorted_models: dict[str, tuple[list[Question], list[Question]]] = {}
    models: dict[str, tuple[list[Question], list[Question]]] = {}
    # for each file in data directory
    for file in os.listdir(args.data):
        # only read json files
        if file.endswith(".json"):
            name = get_model_name(file[:-5])
            # if file contains question not understood
            if(file.endswith("_not_understood.json")):
                # if model name not in models, add model name and questions not understood
                if(name not in unsorted_models):
                    unsorted_models[name] = ([], Question.read_json(os.path.join(args.data, file)))
                # otherwise add questions not understood to model
                else:
                    unsorted_models[name] = (unsorted_models[name][0],Question.read_json(os.path.join(args.data, file)))
            # if file ends with _understood.json
            else:
                # if model name not in models, add model name and questions understood
                if name not in unsorted_models:
                    unsorted_models[name] = (Question.read_json(os.path.join(args.data, file)), [])
                # otherwise add questions understood to model
                else:
                    unsorted_models[name] = (Question.read_json(os.path.join(args.data, file)), unsorted_models[name][1])
    for key in sorted(unsorted_models.keys(), key=get_model_key):
        models[key] = unsorted_models[key]
    
    understood: list[tuple[int, int]] = []
    type_understood: dict[QuestionType, list[tuple[int, int]]] = {}
    source_understood: dict[QuestionSource, list[tuple[int, int]]] = {}
    
    for type in QuestionType:
        type_understood[type] = []
    for source in QuestionSource:
        source_understood[source] = []

    # for each model, get number of understood and not understood questions
    for (name, (understood_q, not_understood_q)) in models.items():
        understood.append((len(understood_q), len(not_understood_q)))
        (type_u, source_u) = count_questions(understood_q)
        (type_n, source_n) = count_questions(not_understood_q)
        for type in QuestionType:
            type_understood[type].append((type_u[type], type_n[type]))
        for source in QuestionSource:
            source_understood[source].append((source_u[source], source_n[source]))
    
    create_plot(list(models.keys()), [data[0] for data in understood], [data[1] for data in understood], "Verstandene Fragen", os.path.join(args.output, "understood.png"))
    for type in QuestionType:
        create_plot(list(models.keys()), [data[0] for data in type_understood[type]], [data[1] for data in type_understood[type]], f"Verstandene Fragen ({type.value})", os.path.join(args.output, f"understood_{type.value}.png"))
    for source in QuestionSource:
        create_plot(list(models.keys()), [data[0] for data in source_understood[source]], [data[1] for data in source_understood[source]], f"Verstandene Fragen ({source.value})", os.path.join(args.output, f"understood_{source.value}.png"))

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

def count_questions(questions: list[Question]) -> tuple[dict[QuestionType, int], dict[QuestionSource, int]]:
    results: tuple[dict[QuestionType, int], dict[QuestionSource, int]] = ({}, {})
    for question in questions:
        if QuestionType(question.type) not in results[0]:
            results[0][QuestionType(question.type)] = 1
        else:
            results[0][QuestionType(question.type)] += 1
        if QuestionSource(question.source) not in results[1]:
            results[1][QuestionSource(question.source)] = 1
        else:
            results[1][QuestionSource(question.source)] += 1
    for type in QuestionType:
        if type not in results[0]:
            results[0][type] = 0
    for source in QuestionSource:
        if source not in results[1]:
            results[1][source] = 0
    return results

if __name__ == "__main__":
    main()