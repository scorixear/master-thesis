import os
import argparse
import matplotlib.pyplot as plt
import numpy as np

from helper.model_helper import get_model_key, get_model_name
from helper.heatmap import ModelHeatMap, show_heatmap
from helper.question import Question, QuestionType, QuestionSource
from helper.plot_helper import PlotParams

def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="Evaluation of the generated questions")
    # path to question understanding generated json file directory
    parser.add_argument("-d", "--data", type=str, help="Path to the evaluated questions",
                        default="evaluation/criterias/question_understanding")
    # path to output directory
    parser.add_argument("-o", "--output", type=str, help="Path to the output directory",
                        default="evaluation/criterias/question_understanding")
    args = parser.parse_args()

    unsorted_models: dict[str, tuple[list[Question], list[Question]]] = {}
    models: dict[str, tuple[list[Question], list[Question]]] = {}
    # for each file in data directory
    for file in os.listdir(args.data):
        # only read json files
        if file.endswith(".json"):
            name = get_model_name(file[:-5])
            # if file contains question not understood
            if file.endswith("_not_understood.json"):
                # if model name not in models, add model name and questions not understood
                if name not in unsorted_models:
                    unsorted_models[name] = ([], Question.read_json(os.path.join(args.data, file)))
                # otherwise add questions not understood to model
                else:
                    unsorted_models[name] = (unsorted_models[name][0],
                                             Question.read_json(os.path.join(args.data, file)))
            # if file ends with _understood.json
            else:
                # if model name not in models, add model name and questions understood
                if name not in unsorted_models:
                    unsorted_models[name] = (Question.read_json(os.path.join(args.data, file)), [])
                # otherwise add questions understood to model
                else:
                    unsorted_models[name] = (Question.read_json(os.path.join(args.data, file)),
                                             unsorted_models[name][1])
    for key in sorted(unsorted_models.keys(), key=get_model_key):
        models[key] = unsorted_models[key]

    heatmap = ModelHeatMap()
    understood: list[tuple[int, int]] = []
    type_understood: dict[QuestionType, list[tuple[int, int]]] = {}
    source_understood: dict[QuestionSource, list[tuple[int, int]]] = {}

    for q_type in QuestionType:
        type_understood[q_type] = []
    for source in QuestionSource:
        source_understood[source] = []

    # for each model, get number of understood and not understood questions
    for (name, (understood_q, not_understood_q)) in models.items():
        understood.append((len(understood_q), len(not_understood_q)))
        (type_u, source_u) = count_questions(understood_q)
        (type_n, source_n) = count_questions(not_understood_q)
        for q_type in QuestionType:
            type_understood[q_type].append((type_u[q_type], type_n[q_type]))
        for source in QuestionSource:
            source_understood[source].append((source_u[source], source_n[source]))
        for question in understood_q:
            heatmap.update_value(name, question.type, question.source, "understood", 1)
        for question in not_understood_q:
            heatmap.update_value(name, question.type, question.source, "not_understood", 1)
        for q_type in QuestionType:
            for source in QuestionSource:
                understood_h = heatmap.get_value(name, str(q_type), str(source), "understood")
                if understood_h is None:
                    understood_h = 0
                not_understood_h = heatmap.get_value(name, str(q_type),
                                                     str(source), "not_understood")
                if not_understood_h is None:
                    not_understood_h = 0
                if understood_h + not_understood_h == 0:
                    avg = 0
                else:
                    avg = understood_h / (understood_h + not_understood_h)
                heatmap.set_value(name, str(q_type), str(source), "avg", avg)
    heatmap.reorder("gpt4", -1)


    create_plot(list(models.keys()), [data[0] for data in understood],
                [data[1] for data in understood], "Verstandene Fragen",
                os.path.join(args.output, "understood.png"))
    show_heatmap(heatmap.get_avgvalue_heatmap_total_by_model("avg"),
                 "Fragequelle", "Fragetyp", "Durschnittlich Verstande Fragen",
                 os.path.join(args.output, "question_understanding_total_model.png"))
    for model in models:
        show_heatmap(heatmap.get_heatmap_by_model(model, "avg"),
                     "Fragequelle", "Fragetyp", f"Durschnittlich Verstande Fragen ({model})",
                     os.path.join(args.output, f"question_understanding_{model}.png"))
    show_heatmap(heatmap.get_avgvalue_heatmap_total_by_type("avg"),
                 "Fragequelle", "Modell", "Durschnittlich Verstande Fragen",
                 os.path.join(args.output, "question_understanding_total_type.png"))
    for q_type in QuestionType:
        create_plot(list(models.keys()), [data[0] for data in type_understood[q_type]],
                    [data[1] for data in type_understood[q_type]],
                    f"Verstandene Fragen ({q_type.value})",
                    os.path.join(args.output, f"understood_{q_type.value}.png"))
        show_heatmap(heatmap.get_heatmap_by_type(str(q_type), "avg"),
                     "Fragequelle", "Modell", f"Durschnittlich Verstande Fragen ({q_type.value})",
                     os.path.join(args.output, f"question_understanding_{q_type}.png"))
    show_heatmap(heatmap.get_avgvalue_heatmap_total_by_source("avg"),
                 "Fragetyp", "Modell", "Durschnittlich Verstande Fragen",
                 os.path.join(args.output, "question_understanding_total_source.png"))
    for source in QuestionSource:
        create_plot(list(models.keys()), [data[0] for data in source_understood[source]],
                    [data[1] for data in source_understood[source]],
                    f"Verstandene Fragen ({source.value})",
                    os.path.join(args.output, f"understood_{source.value}.png"))
        show_heatmap(heatmap.get_heatmap_by_source(str(source), "avg"),
                     "Fragetyp", "Modell", f"Durschnittlich Verstande Fragen ({source.value})",
                     os.path.join(args.output, f"question_understanding_{source}.png"))

def create_plot(model_names: list[str], understood: list[int],
                not_understood: list[int], title: str, file_path: str):
    # create dataset for stacked bars
    understood_plot = {
        "Verstanden": np.array(understood),
        "Nicht Verstanden": np.array(not_understood),
    }
    # create figure of size 20, 10
    fig = plt.figure(figsize=PlotParams.fig_size)
    # subplots() to get axis object
    axis = fig.subplots()
    # bottom array for stacked bars
    bottom = np.zeros(len(model_names))
    # colors of stacked bars in reverse order
    colors = ["silver", "green"]
    # for each label and data in dataset
    for labels, data in understood_plot.items():
        # plot bars
        bars = axis.bar(model_names, data, width=0.5, label=labels, bottom=bottom,
                        color=colors.pop())
        # set bar labels
        axis.bar_label(bars, fontsize=PlotParams.font_size)
        # and stack next bar on top
        bottom += data
    x_ticks = axis.get_xticks()
    axis.set_xticks(x_ticks, labels=model_names, rotation=45, fontsize=PlotParams.font_size)
    axis.tick_params(axis="y", labelsize=PlotParams.font_size)
    axis.legend(loc=(1.01, 0.85), fontsize=PlotParams.font_size)
    axis.set_xlabel("Modell", fontsize=PlotParams.font_size)
    # set y-axis legend
    axis.set_ylabel("Anzahl der Fragen", fontsize=PlotParams.font_size)
    # set title and  padding as bar labels might overlap
    axis.set_title(title, pad=PlotParams.title_padding, fontsize=PlotParams.title_font_size)
    fig.tight_layout()
    # and save the figure
    fig.savefig(file_path)

def count_questions(questions: list[Question]) \
    -> tuple[dict[QuestionType, int], dict[QuestionSource, int]]:
    results: tuple[dict[QuestionType, int], dict[QuestionSource, int]] = ({}, {})
    for question in questions:
        if QuestionType(question.type) not in results[0]:
            results[0][QuestionType(question.type)] = 1 # type: ignore
        else:
            results[0][QuestionType(question.type)] += 1 # type: ignore
        if QuestionSource(question.source) not in results[1]:
            results[1][QuestionSource(question.source)] = 1 # type: ignore
        else:
            results[1][QuestionSource(question.source)] += 1 # type: ignore
    for q_type in QuestionType:
        if q_type not in results[0]:
            results[0][q_type] = 0
    for source in QuestionSource:
        if source not in results[1]:
            results[1][source] = 0
    return results

if __name__ == "__main__":
    main()
