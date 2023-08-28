import os
import argparse
import matplotlib.pyplot as plt
import numpy as np

from helper.model_helper import get_model_key, get_model_name
from helper.heatmap import ModelHeatMap, show_heatmap
from helper.question import Question, QuestionSource, QuestionType
from helper.plot_helper import PlotParams

def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="Evaluation of the generated questions")
    # path to explainability generated json file directory
    parser.add_argument("-d", "--data", type=str, help="Path to the evaluated questions",
                        default="evaluation/criterias/explainability")
    # path to output directory
    parser.add_argument("-o", "--output", type=str, help="Path to the output directory",
                        default="evaluation/criterias/explainability")
    args = parser.parse_args()
    unsorted_models: dict[str, tuple[list[Question], list[Question]]] = {}
    models: dict[str, tuple[list[Question], list[Question]]] = {}
    # read in json files
    for file in os.listdir(args.data):
        # only read json files
        if file.endswith(".json"):
            name = get_model_name(file[:-5])
            # if file contains question not explained
            if file.endswith("_not_explained.json"):
                # if model name not in models, add model name and questions not explained
                if name not in unsorted_models:
                    unsorted_models[name] = ([], Question.read_json(os.path.join(args.data, file)))
                # otherwise add questions not explained to model
                else:
                    unsorted_models[name] = (unsorted_models[name][0],
                                             Question.read_json(os.path.join(args.data, file)))
            # if file ends with _explained.json
            else:
                # if model name not in models, add model name and questions explained
                if name not in unsorted_models:
                    unsorted_models[name] = (Question.read_json(os.path.join(args.data, file)), [])
                # otherwise add questions explained to model
                else:
                    unsorted_models[name] = (Question.read_json(os.path.join(args.data, file)),
                                             unsorted_models[name][1])
    # sort models by key
    for key in sorted(unsorted_models.keys(), key=get_model_key):
        models[key] = unsorted_models[key]

    heatmap = ModelHeatMap()
    explained: list[tuple[int, int]] = []
    type_explained: dict[QuestionType, list[tuple[int, int]]] = {}
    for q_type in QuestionType:
        type_explained[q_type] = []
    source_explained: dict[QuestionSource, list[tuple[int, int]]] = {}
    for source in QuestionSource:
        source_explained[source] = []

    # for each model, get number of explained and not explained questions
    for (name, (explained_q, not_explained_q)) in models.items():
        explained.append((len(explained_q), len(not_explained_q)))
        (type_exp, source_exp) = count_questions(explained_q)
        (type_not_exp, source_not_exp) = count_questions(not_explained_q)
        for q_type in QuestionType:
            type_explained[q_type].append((type_exp[q_type], type_not_exp[q_type]))
        for source in QuestionSource:
            source_explained[source].append((source_exp[source], source_not_exp[source]))
        for question in explained_q:
            heatmap.update_value(name, question.type, question.source, "explained", 1)
        for question in not_explained_q:
            heatmap.update_value(name, question.type, question.source, "not_explained", 1)
        for q_type in QuestionType:
            for source in QuestionSource:
                explained_h = heatmap.get_value(name, str(q_type), str(source), "explained")
                if explained_h is None:
                    explained_h = 0
                not_explained_h = heatmap.get_value(name, str(q_type), str(source), "not_explained")
                if not_explained_h is None:
                    not_explained_h = 0
                if explained_h + not_explained_h == 0:
                    avg = 0
                else:
                    avg = explained_h / (explained_h + not_explained_h)
                heatmap.set_value(name, str(q_type), str(source), "avg", avg)
    heatmap.reorder("gpt4", -1)


    create_plot(list(models.keys()), [data[0] for data in explained],
                [data[1] for data in explained], "Anzahl der Fragen, die erklärt wurden",
                os.path.join(args.output, "explained.png"))
    show_heatmap(heatmap.get_avgvalue_heatmap_total_by_model("avg"),
                 "Fragequelle", "Fragetyp", "Durchschnittliche Erklärbarkeit der Fragen",
                 os.path.join(args.output, "explainability_total_model.png"))
    for model in models:
        show_heatmap(heatmap.get_heatmap_by_model(model, "avg"),
                     "Fragequelle", "Fragetyp",
                     f"Durchschnittliche Erklärbarkeit der Fragen für {model}",
                     os.path.join(args.output, f"explainability_{model}.png"))
    show_heatmap(heatmap.get_avgvalue_heatmap_total_by_type("avg"),
                 "Fragequelle", "Modell", "Durchschnittliche Erklärbarkeit der Fragen",
                 os.path.join(args.output, "explainability_total_type.png"))
    for q_type in QuestionType:
        create_plot(list(models.keys()), [data[0] for data in type_explained[q_type]],
                    [data[1] for data in type_explained[q_type]],
                    f"Anzahl der {q_type} Fragen, die erklärt wurden",
                    os.path.join(args.output, f"explained_{q_type}.png"))
        show_heatmap(heatmap.get_heatmap_by_type(str(q_type), "avg"),
                     "Fragequelle", "Modell",
                     f"Durchschnittliche Erklärbarkeit der {q_type} Fragen",
                     os.path.join(args.output, f"avg_{q_type}.png"))
    show_heatmap(heatmap.get_avgvalue_heatmap_total_by_source("avg"),
                 "Fragetyp", "Modell", "Durchschnittliche Erklärbarkeit der Fragen",
                 os.path.join(args.output, "explainability_total_source.png"))
    for source in QuestionSource:
        create_plot(list(models.keys()), [data[0] for data in source_explained[source]],
                    [data[1] for data in source_explained[source]],
                    f"Anzahl der {source} Fragen, die erklärt wurden",
                    os.path.join(args.output, f"explained_{source}.png"))
        show_heatmap(heatmap.get_heatmap_by_source(str(source), "avg"),
                     "Fragetyp", "Modell", f"Durchschnittliche Erklärbarkeit der {source} Fragen",
                     os.path.join(args.output, f"explainability_{source}.png"))

def create_plot(model_names: list[str], explained: list[int],
                not_explained: list[int], title: str, file_path: str):

    # create stacked bars dataset
    explained_plot = {
        "Erklärt": np.array(explained),
        "Nicht Erklärt": np.array(not_explained),
    }

    # figure of size 20, 10
    fig = plt.figure(figsize=PlotParams.fig_size)
    # subplots() to get axis object
    axis = fig.subplots()
    # create bottom array for stacked bars
    bottom = np.zeros(len(model_names))
    # and colors backwards
    colors = ["silver", "green"]
    # for each label and data in explained_plot
    for labels, data in explained_plot.items():
        # create bars
        bars = axis.bar(model_names, data, width=0.5, label=labels, bottom=bottom,
                        color=colors.pop())
        # set bar labels
        axis.bar_label(bars, fontsize=PlotParams.font_size)
        # and stack next bars on top
        bottom += data
    x_ticks = axis.get_xticks()
    axis.set_xticks(x_ticks, labels=model_names, rotation=45, fontsize=PlotParams.font_size)
    axis.tick_params(axis="y", labelsize=PlotParams.font_size)
    axis.legend(fontsize=PlotParams.font_size)
    axis.set_xlabel("Modell", fontsize=PlotParams.font_size)
    # set y-axis legend
    axis.set_ylabel("Anzahl der Antworten", fontsize=PlotParams.font_size)
    # set title with padding, ad bar_labels might overlap
    axis.set_title(title, pad=PlotParams.title_padding, fontsize=PlotParams.title_font_size)
    fig.tight_layout()
    # and save figure
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
