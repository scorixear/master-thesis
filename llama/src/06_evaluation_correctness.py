import os
import argparse

import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
import pandas as pd

from helper.question import Question, QuestionSource, QuestionType
from helper.model_helper import get_model_key, get_model_name
from helper.heatmap import ModelHeatMap, show_heatmap
from helper.plot_helper import PlotParams


def main():
    # parse arguments
    parser = argparse.ArgumentParser(
        description="Evaluation of the generated questions"
    )
    # path to evaluated questions json file
    parser.add_argument(
        "-d",
        "--data",
        type=str,
        help="Path to the evaluated questions",
        default="evaluation/input",
    )
    # path to output directory
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Path to the output directory",
        default="evaluation/criterias/correctness",
    )
    parser.add_argument(
        "-s", "--skip", action="store_true", help="Skip recalculation of statistics"
    )
    args = parser.parse_args()

    if not args.skip:
        df, heatmap_data = calculate_correctness(args)
    else:
        df = pd.read_csv(args.output + "/evaluation.csv")
        heatmap_data = ModelHeatMap.read_json(args.output + "/heatmap.json")

    heatmap_data.reorder("gpt4", -1)

    # get model names for plots
    model_names = df["Model"].tolist()

    # bar plots with correct, wrong and unanswered questions
    num_correct = np.array(df["Num_Correct"].tolist())
    num_wrong = np.array(df["Num_Wrong"].tolist())
    num_unanswered = np.array(df["Num_Unanswered"].tolist())
    show_answer_bars(
        num_correct,
        num_wrong,
        num_unanswered,
        model_names,
        "Richtig, Falsch und Unbeantwortete Fragen",
        args.output + "/answers_total.png",
    )
    show_heatmap(
        heatmap_data.get_makrof1_heatmap_total_by_model(),
        "Fragequelle",
        "Fragetyp",
        "Makro F1",
        args.output + "/makrof1_total_model_heat.png",
    )
    for model in model_names:
        show_heatmap(
            heatmap_data.get_heatmap_by_model(model, "makrof1"),
            "Fragequelle",
            "Fragetyp",
            f"Makro F1 ({model})",
            args.output + f"/makrof1_{model}_heat.png",
        )

    show_heatmap(
        heatmap_data.get_makrof1_heatmap_total_by_type(),
        "Fragequelle",
        "Modell",
        "Makro F1",
        args.output + "/makrof1_total_type_heat.png",
    )
    for q_type in QuestionType:
        num_correct = np.array(df[f"Num_Correct_{q_type}"].tolist())
        num_wrong = np.array(df[f"Num_Wrong_{q_type}"].tolist())
        num_unanswered = np.array(df[f"Num_Unanswered_{q_type}"].tolist())
        show_answer_bars(
            num_correct,
            num_wrong,
            num_unanswered,
            model_names,
            f"Richtig, Falsch und Unbeantwortete Fragen ({q_type})",
            args.output + f"/answers_{q_type}.png",
        )
        show_heatmap(
            heatmap_data.get_heatmap_by_type(q_type, "makrof1"),
            "Fragequelle",
            "Modell",
            f"Makro F1 ({q_type})",
            args.output + f"/makrof1_{q_type}_heat.png",
        )
    show_heatmap(
        heatmap_data.get_makrof1_heatmap_total_by_source(),
        "Fragetyp",
        "Modell",
        "Makro F1",
        args.output + "/makrof1_total_source_heat.png",
    )
    for source in QuestionSource:
        num_correct = np.array(df[f"Num_Correct_{source}"].tolist())
        num_wrong = np.array(df[f"Num_Wrong_{source}"].tolist())
        num_unanswered = np.array(df[f"Num_Unanswered_{source}"].tolist())
        show_answer_bars(
            num_correct,
            num_wrong,
            num_unanswered,
            model_names,
            f"Richtig, Falsch und Unbeantwortete Fragen ({source})",
            args.output + f"/answers_{source}.png",
        )
        show_heatmap(
            heatmap_data.get_heatmap_by_source(source, "makrof1"),
            "Fragetyp",
            "Modell",
            f"Makro F1 ({source})",
            args.output + f"/makrof1_{source}_heat.png",
        )
    # bar plots with macro f1 scores

    show_makrof1_bars(
        df["MacroF1"].tolist(),
        model_names,
        "Makro F1",
        args.output + "/makro_total.png",
    )
    for q_type in QuestionType:
        show_makrof1_bars(
            df[f"MacroF1_{q_type}"].tolist(),
            model_names,
            f"Makro F1 ({q_type})",
            args.output + f"/makro_{q_type}.png",
        )
    for source in QuestionSource:
        show_makrof1_bars(
            df[f"MacroF1_{source}"].tolist(),
            model_names,
            f"Makro F1 ({source})",
            args.output + f"/makro_{source}.png",
        )


def calculate_correctness(args):
    # read in evaluated questions
    unsorted_models: dict[str, list[Question]] = {}
    for file in os.listdir(args.data):
        # only read json files
        if file.endswith(".json"):
            # remove .json to get model name
            name = get_model_name(file[:-5])
            unsorted_models[name] = Question.read_json(os.path.join(args.data, file))
    model_names = sorted(unsorted_models.keys(), key=get_model_key)
    models: list[list[Question]] = [unsorted_models[name] for name in model_names]

    heatmap_data: ModelHeatMap = ModelHeatMap()
    for model in model_names:
        for q_type in QuestionType:
            for source in QuestionSource:
                heatmap_data.set_value(model, q_type, source, "correct", 0)
                heatmap_data.set_value(model, q_type, source, "wrong", 0)
                heatmap_data.set_value(model, q_type, source, "unanswered", 0)
                heatmap_data.set_value(model, q_type, source, "makrof1", 0)
                heatmap_data.set_value(model, q_type, source, "f1", [])

    # initialize pandas dataframe
    dataframe_columns = [
        "Model",
        "Num_Correct",
        "Num_Wrong",
        "Num_Unanswered",
        "Num_Questions",
        "MacroF1",
    ]
    dataframe_columns.extend([f"Num_Correct_{qtype}" for qtype in QuestionType])
    dataframe_columns.extend([f"Num_Wrong_{qtype}" for qtype in QuestionType])
    dataframe_columns.extend([f"Num_Unanswered_{qtype}" for qtype in QuestionType])
    dataframe_columns.extend([f"Num_Questions_{qtype}" for qtype in QuestionType])
    dataframe_columns.extend([f"MacroF1_{qtype}" for qtype in QuestionType])
    dataframe_columns.extend([f"Num_Correct_{source}" for source in QuestionSource])
    dataframe_columns.extend([f"Num_Wrong_{source}" for source in QuestionSource])
    dataframe_columns.extend([f"Num_Unanswered_{source}" for source in QuestionSource])
    dataframe_columns.extend([f"Num_Questions_{source}" for source in QuestionSource])
    dataframe_columns.extend([f"MacroF1_{source}" for source in QuestionSource])
    df = DataFrame(columns=dataframe_columns)
    # for each model
    for index, model in enumerate(models):
        # get model name
        name = model_names[index]
        # initialize counters
        num_correct = 0
        num_wrong = 0
        num_unanswered = 0
        type_num_correct: dict[QuestionType, int] = {}
        type_num_wrong: dict[QuestionType, int] = {}
        type_num_unanswered: dict[QuestionType, int] = {}
        source_num_correct: dict[QuestionSource, int] = {}
        source_num_wrong: dict[QuestionSource, int] = {}
        source_num_unanswered: dict[QuestionSource, int] = {}
        # initialize f1 scores
        f1_scores = []
        type_f1_scores: dict[QuestionType, list[float]] = {}
        source_f1_scores: dict[QuestionSource, list[float]] = {}
        for q_type in QuestionType:
            type_f1_scores[q_type] = []
            type_num_correct[q_type] = 0
            type_num_wrong[q_type] = 0
            type_num_unanswered[q_type] = 0
        for source in QuestionSource:
            source_f1_scores[source] = []
            source_num_correct[source] = 0
            source_num_wrong[source] = 0
            source_num_unanswered[source] = 0
        # for each question of one model evaluation
        for question in model:
            # get correct answers (C)
            correct: float = question.points
            # get expected correct answers (G)
            true: float = question.num_answers
            # get total answers (S)
            total: float = question.total_answers
            # if total or true are 0, we cannot divide by 0
            # therefor f1 is 0
            # as the model gave 0 answers
            if total == 0 or true == 0:
                f1: float = 0
            else:
                # calculate precision
                prec = correct / total
                # and recall
                recall = correct / true
                # if both are 0, f1 is 0
                if prec + recall == 0:
                    f1 = 0
                # else calculate f1
                else:
                    f1 = 2 * (prec * recall) / (prec + recall)
            # and append to f1 scores
            f1_scores.append(f1)
            type_f1_scores[QuestionType(question.type)].append(f1)  # type: ignore
            source_f1_scores[QuestionSource(question.source)].append(f1)  # type: ignore
            heatmap_data.append_value(name, question.type, question.source, "f1", f1)
            # increase counters depending on question type
            # and if question was answered correctly, wrong or not at all
            if question.answered == 0:
                num_unanswered += 1
                type_num_unanswered[QuestionType(question.type)] += 1  # type: ignore
                source_num_unanswered[QuestionSource(question.source)] += 1  # type: ignore
                heatmap_data.update_value(
                    name, question.type, question.source, "unanswered", 1
                )
            elif question.answered == 1:
                num_wrong += 1
                type_num_wrong[QuestionType(question.type)] += 1  # type: ignore
                source_num_wrong[QuestionSource(question.source)] += 1  # type: ignore
                heatmap_data.update_value(
                    name, question.type, question.source, "wrong", 1
                )
            elif question.answered == 2:
                num_correct += 1
                type_num_correct[QuestionType(question.type)] += 1  # type: ignore
                source_num_correct[QuestionSource(question.source)] += 1  # type: ignore
                heatmap_data.update_value(
                    name, question.type, question.source, "correct", 1
                )

        # calcualte macro f1 scores
        macro_f1 = sum(f1_scores) / len(f1_scores)
        type_macro_f1: dict[QuestionType, float] = {}
        source_macro_f1: dict[QuestionSource, float] = {}
        for q_type in QuestionType:
            type_macro_f1[q_type] = sum(type_f1_scores[q_type]) / len(
                type_f1_scores[q_type]
            )
            for source in QuestionSource:
                type_f1: list[int] = heatmap_data.get_value(
                    name, q_type, source, "f1"
                )  # type: ignore
                type_makro_f1 = sum(type_f1) / len(type_f1)
                heatmap_data.set_value(name, q_type, source, "makrof1", type_makro_f1)
        for source in QuestionSource:
            source_macro_f1[source] = sum(source_f1_scores[source]) / len(
                source_f1_scores[source]
            )

        # and the total amount of questions per type
        questions = num_correct + num_wrong + num_unanswered
        type_questions: dict[QuestionType, int] = {}
        source_questions: dict[QuestionSource, int] = {}
        for q_type in QuestionType:
            type_questions[q_type] = (
                type_num_correct[q_type]
                + type_num_wrong[q_type]
                + type_num_unanswered[q_type]
            )
        for source in QuestionSource:
            source_questions[source] = (
                source_num_correct[source]
                + source_num_wrong[source]
                + source_num_unanswered[source]
            )

        # add to dataframe
        final_results = [
            name,
            num_correct,
            num_wrong,
            num_unanswered,
            questions,
            macro_f1,
        ]
        final_results.extend([type_num_correct[type] for type in QuestionType])
        final_results.extend([type_num_wrong[type] for type in QuestionType])
        final_results.extend([type_num_unanswered[type] for type in QuestionType])
        final_results.extend([type_questions[type] for type in QuestionType])
        final_results.extend([type_macro_f1[type] for type in QuestionType])
        final_results.extend([source_num_correct[source] for source in QuestionSource])
        final_results.extend([source_num_wrong[source] for source in QuestionSource])
        final_results.extend(
            [source_num_unanswered[source] for source in QuestionSource]
        )
        final_results.extend([source_questions[source] for source in QuestionSource])
        final_results.extend([source_macro_f1[source] for source in QuestionSource])
        df.loc[len(df)] = final_results  # type: ignore

    # save data to csv
    df.to_csv(args.output + "/evaluation.csv", index=False)
    heatmap_data.save_json(args.output + "/heatmap.json")
    return df, heatmap_data


def show_answer_bars(correct, wrong, unanswered, names, title, file_name):
    # create figure of 20, 10 size
    fig = plt.figure(figsize=PlotParams.fig_size)
    # subplots() to get axis object
    axis = fig.subplots()
    # create stacked bars dataset
    answers = {"Korrekt": correct, "Falsch": wrong, "Unbeantwortet": unanswered}
    # create bottom array with 0
    bottom = np.zeros(len(names))
    # and define colors (backwards because of stacking)
    colors = ["silver", "lightcoral", "green"]
    # for each label in answers dataset
    for labels, answer in answers.items():
        # create the bars for each model
        bars = axis.bar(
            names, answer, width=0.8, label=labels, bottom=bottom, color=colors.pop()
        )
        # stack next bars on top
        bottom += answer
        # enable labeling of bars
        axis.bar_label(bars, fontsize=PlotParams.font_size)
    x_ticks = axis.get_xticks()
    axis.set_xticks(x_ticks, labels=names, rotation=45, fontsize=PlotParams.font_size)
    axis.tick_params(axis="y", labelsize=PlotParams.font_size)
    # add legend
    axis.legend(loc=(1.01, 0.78), fontsize=PlotParams.font_size)
    axis.set_xlabel("Modell", fontsize=PlotParams.font_size)
    # y axis legend
    axis.set_ylabel("Anzahl der Fragen", fontsize=PlotParams.font_size)
    # title with padding because bar labels might overlap
    axis.set_title(
        title, pad=PlotParams.title_padding, fontsize=PlotParams.title_font_size
    )
    # save figure
    fig.tight_layout()
    fig.savefig(file_name)


def show_makrof1_bars(f1, names, title, file_name):
    # create figure of size 20, 10
    fig = plt.figure(figsize=PlotParams.fig_size)
    # subplots to get axis object
    axis = fig.subplots()
    # create bars
    f1 = [round(x, 2) for x in f1]
    bars = axis.bar(names, f1, width=0.8)
    x_ticks = axis.get_xticks()
    axis.set_xticks(x_ticks, labels=names, rotation=45, fontsize=PlotParams.font_size)
    axis.tick_params(axis="y", labelsize=PlotParams.font_size)
    # label bars
    axis.bar_label(bars, fontsize=PlotParams.font_size)
    axis.set_xlabel("Modell", fontsize=PlotParams.font_size)
    # set y axis label
    axis.set_ylabel("Makro F1", fontsize=PlotParams.font_size)
    # set title and padding as bar labels might overlap
    axis.set_title(
        title, pad=PlotParams.title_padding, fontsize=PlotParams.title_font_size
    )
    # and save the figure
    fig.tight_layout()
    fig.savefig(file_name)


if __name__ == "__main__":
    main()
