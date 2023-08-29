import os
import argparse
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
import pandas as pd

from helper.question import Question, QuestionType, QuestionSource
from helper.model_helper import get_model_key, get_model_name
from helper.plot_helper import PlotParams


def main():
    # parse arguments
    parser = argparse.ArgumentParser(
        description="Evaluation of the generated questions"
    )
    # path to evaluated questions json file directory
    parser.add_argument(
        "-d",
        "--data",
        type=str,
        help="Path to the evaluated questions",
        default="evaluation/spelling",
    )
    # path to correctness evaluation csv file
    parser.add_argument(
        "-e",
        "--eval",
        type=str,
        help="Path to the evaluation file",
        default="evaluation/criterias/correctness/evaluation.csv",
    )
    # path to output directory
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Path to the output directory",
        default="evaluation/criterias/robustness",
    )
    parser.add_argument(
        "-s", "--skip", action="store_true", help="Skip calculation of correctness"
    )
    args = parser.parse_args()

    if not args.skip:
        df = calculate_correctness(args)
    else:
        df = pd.read_csv(args.output + "/evaluation.csv")

    # read in correctness evaluation
    evaluated = pd.read_csv(args.eval)
    model_names = df["Model"].tolist()

    # create bar plots for correct, wrong and unanswered questions
    num_correct = np.array(df["Num_Correct"].tolist())
    num_wrong = np.array(df["Num_Wrong"].tolist())
    num_unanswered = np.array(df["Num_Unanswered"].tolist())
    show_answer_bars(
        num_correct,
        num_wrong,
        num_unanswered,
        model_names,
        "Richtig, Falsch und Unbeantwortete Fragen - Robustheit",
        args.output + "/answers_total.png",
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
            f"Richtig, Falsch und Unbeantwortete Fragen ({q_type}) - Robustheit",
            args.output + f"/answers_{q_type}.png",
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
            f"Richtig, Falsch und Unbeantwortete Fragen ({source}) - Robustheit",
            args.output + f"/answers_{source}.png",
        )

    # create bar plots for macro f1 scores
    show_makrof1_bars(
        df["MacroF1"].tolist(),
        model_names,
        "Makro F1 - Robustheit",
        args.output + "/makro_total.png",
    )
    for q_type in QuestionType:
        show_makrof1_bars(
            df[f"MacroF1_{q_type}"].tolist(),
            model_names,
            f"Makro F1 ({q_type}) - Robustheit",
            args.output + f"/makro_{q_type}.png",
        )
    for source in QuestionSource:
        show_makrof1_bars(
            df[f"MacroF1_{source}"].tolist(),
            model_names,
            f"Makro F1 ({source}) - Robustheit",
            args.output + f"/makro_{source}.png",
        )

    # extract data from correctness evaluation
    makro_eval = evaluated["MacroF1"].tolist()
    show_comparison_bars(
        df["MacroF1"].tolist(),
        makro_eval,
        model_names,
        "Makro F1 Vergleich - Robustheit",
        args.output + "/makro_comparison.png",
    )

    for q_type in QuestionType:
        macro_eval = evaluated[f"MacroF1_{q_type}"].tolist()
        show_comparison_bars(
            df[f"MacroF1_{q_type}"].tolist(),
            macro_eval,
            model_names,
            f"Makro F1 Vergleich ({q_type}) - Robustheit",
            args.output + f"/makro_{q_type}_comparison.png",
        )
    for source in QuestionSource:
        macro_eval = evaluated[f"MacroF1_{source}"].tolist()
        show_comparison_bars(
            df[f"MacroF1_{source}"].tolist(),
            macro_eval,
            model_names,
            f"Makro F1 Vergleich ({source}) - Robustheit",
            args.output + f"/makro_{source}_comparison.png",
        )


def calculate_correctness(args):
    unsorted_models: dict[str, list[Question]] = {}
    # read in all json files in directory
    for file in os.listdir(args.data):
        # only read json files
        if file.endswith(".json"):
            name = get_model_name(file[:-5])
            unsorted_models[name] = Question.read_json(os.path.join(args.data, file))
    # remove .json to get model name
    model_names = sorted(unsorted_models.keys(), key=get_model_key)
    models: list[list[Question]] = [unsorted_models[name] for name in model_names]

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
        # get name
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

        # for each question
        for question in model:
            # number of correct answers (C)
            correct: float = question.points
            # number of true answers (G)
            true: float = question.num_answers
            # number of total answers given (S)
            total: float = question.total_answers
            # if total or true is 0, the model either answered nothing
            # or the question is invalid
            if total == 0 or true == 0:
                f1: float = 0
            else:
                # calcualte precision
                prec = correct / total
                # calculate recall
                recall = correct / true
                # if both are 0, f1 is 0
                if prec + recall == 0:
                    f1: float = 0
                # else calculate f1 score
                else:
                    f1: float = 2 * (prec * recall) / (prec + recall)
            # and append
            f1_scores.append(f1)
            type_f1_scores[QuestionType(question.type)].append(f1)  # type: ignore
            source_f1_scores[QuestionSource(question.source)].append(f1)  # type: ignore
            # count correct, wrong and unanswered questions
            # for each question type
            if question.answered == 0:
                num_unanswered += 1
                type_num_unanswered[QuestionType(question.type)] += 1  # type: ignore
                source_num_unanswered[QuestionSource(question.source)] += 1  # type: ignore
            elif question.answered == 1:
                num_wrong += 1
                type_num_wrong[QuestionType(question.type)] += 1  # type: ignore
                source_num_wrong[QuestionSource(question.source)] += 1  # type: ignore
            elif question.answered == 2:
                num_correct += 1
                type_num_correct[QuestionType(question.type)] += 1  # type: ignore
                source_num_correct[QuestionSource(question.source)] += 1  # type: ignore

        # calculate macro f1 scores
        # but include max number of question answered
        # as they are counted as f1 = 0 in correctness
        # this represents the correct macro f1 score
        macro_f1 = sum(f1_scores) / 95

        type_macro_f1: dict[QuestionType, float] = {
            QuestionType.Single: sum(type_f1_scores[QuestionType.Single]) / 34,  # type: ignore
            QuestionType.Multi: sum(type_f1_scores[QuestionType.Multi]) / 38,  # type: ignore
            QuestionType.Transfer: sum(type_f1_scores[QuestionType.Transfer]) / 23,  # type: ignore
        }
        source_macro_f1: dict[QuestionSource, float] = {
            QuestionSource.Book: sum(source_f1_scores[QuestionSource.Book]) / 33,  # type: ignore
            QuestionSource.IS_2022_07_18: sum(
                source_f1_scores[QuestionSource.IS_2022_07_18]
            )
            / 9,  # type: ignore
            QuestionSource.IS_2022_09_27: sum(
                source_f1_scores[QuestionSource.IS_2022_09_27]
            )
            / 31,  # type: ignore
            QuestionSource.A_2021: sum(source_f1_scores[QuestionSource.A_2021]) / 22,  # type: ignore
        }

        # and calculate total number of questions
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

        # append to dataframe
        df.loc[len(df)] = final_results  # type: ignore
    # save dataframe
    df.to_csv(args.output + "/evaluation.csv", index=False)
    return df


def show_answer_bars(correct, wrong, unanswered, names, title, file_name):
    # create figure of size 20, 10
    fig = plt.figure(figsize=PlotParams.fig_size)
    # subplots() to get axis object
    axis = fig.subplots()
    # create stacked bars dataset
    answers = {"Korrekt": correct, "Falsch": wrong, "Unbeantwortet": unanswered}
    # bottom array for stacking bars
    bottom = np.zeros(len(names))
    # and colors per stack, in reverse order
    colors = ["silver", "lightcoral", "green"]
    # for each label, answer pair
    for labels, answer in answers.items():
        # create bar plot
        bars = axis.bar(
            names, answer, width=0.5, label=labels, bottom=bottom, color=colors.pop()
        )
        # stack next plot ontop
        bottom += answer
        # and add bar labels
        axis.bar_label(bars, fontsize=PlotParams.font_size)
    x_ticks = axis.get_xticks()
    axis.set_xticks(x_ticks, labels=names, rotation=45, fontsize=PlotParams.font_size)
    axis.tick_params(axis="y", labelsize=PlotParams.font_size)
    axis.legend(fontsize=PlotParams.font_size)
    axis.set_xlabel("Modell", fontsize=PlotParams.font_size)
    # set y-axis label
    axis.set_ylabel("Anzahl der Antworten", fontsize=PlotParams.font_size)
    # set title, with padding as bar_labels might overlap
    axis.set_title(
        title, pad=PlotParams.title_padding, fontsize=PlotParams.title_font_size
    )
    fig.tight_layout()
    # and save figure
    fig.savefig(file_name)


def show_makrof1_bars(f1, names, title, file_name):
    # create figure of size 20, 10
    fig = plt.figure(figsize=PlotParams.fig_size)
    # subplots() to get axis object
    axis = fig.subplots()

    # create bar plot
    f1 = [round(score, 2) for score in f1]
    bars = axis.bar(names, f1, width=0.5)
    x_ticks = axis.get_xticks()
    axis.set_xticks(x_ticks, labels=names, rotation=45, fontsize=PlotParams.font_size)
    axis.tick_params(axis="y", labelsize=PlotParams.font_size)
    # and add bar labels
    axis.bar_label(bars, fontsize=PlotParams.font_size)
    axis.set_xlabel("Modell", fontsize=PlotParams.font_size)
    # set y-axis label
    axis.set_ylabel("Makro F1", fontsize=PlotParams.font_size)
    # set title, with padding as bar_labels might overlap
    axis.set_title(
        title, pad=PlotParams.title_padding, fontsize=PlotParams.title_font_size
    )
    fig.tight_layout()
    # and save figure
    fig.savefig(file_name)


def show_comparison_bars(f1, evalf1, names, title, file_name):
    # create new x labels as we stack bars now horizontally
    x_labels = np.arange(len(names))
    # with defined width of each bar
    width = 0.4
    # counter for offsetting bars
    multiplier = 0

    # create figure and axis objects
    fig, axis = plt.subplots(figsize=PlotParams.fig_size, layout="constrained")
    # and stacked bars for each label
    f1_scores = {"Normal": evalf1, "Fehlerhaft": f1}

    # for each label and f1 score
    for label, f1_score in f1_scores.items():
        # calculate offset from actual x position
        offset = width * multiplier + width / 2
        f1_score = [round(score, 2) for score in f1_score]
        # and plot bars at offset
        bars = axis.bar(x_labels + offset, f1_score, width, label=label)
        # add bar labels
        axis.bar_label(bars, padding=3, fontsize=PlotParams.font_size)
        # and increase multiplier
        multiplier += 1

    axis.set_xlabel("Modell", fontsize=PlotParams.font_size)
    # y-axis label
    axis.set_ylabel("Makro F1", fontsize=PlotParams.font_size)
    # title with padding, as bar_labels might overlap
    # reset x-axis labels to correct position and value
    axis.set_xticks(x_labels + width, names, rotation=45, fontsize=PlotParams.font_size)
    axis.tick_params(axis="y", labelsize=PlotParams.font_size)
    # and add legend
    axis.legend(fontsize=PlotParams.font_size)
    # limit y axis to 0-1 as f1 only goes from 0-1
    axis.set_ylim(0, 1)
    axis.set_title(
        title, pad=PlotParams.title_padding, fontsize=PlotParams.title_font_size
    )

    fig.tight_layout()
    # and save the figure
    fig.savefig(file_name)


if __name__ == "__main__":
    main()
