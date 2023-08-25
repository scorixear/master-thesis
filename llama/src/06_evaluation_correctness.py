import json
import os
import json_fix # this import is needed for def __json__(self) although not used
import argparse
import matplotlib.pyplot as plt
import numpy as np

from question import Question, QuestionSource, QuestionType

from pandas import DataFrame
import pandas as pd
import seaborn
from model_helper import get_model_key, get_model_name, ModelHeatMap



def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="Evaluation of the generated questions")
    # path to evaluated questions json file
    parser.add_argument("-d", "--data", type=str, help="Path to the evaluated questions", 
                        default="evaluation/input")
    # path to output directory
    parser.add_argument("-o", "--output", type=str, help="Path to the output directory", default="evaluation/criterias/correctness")
    parser.add_argument("-s", "--skip", action="store_true", help="Skip recalculation of statistics")
    args = parser.parse_args()
    
    if not args.skip:
        df, heatmap_data = calculate_correctness(args)
    else:
        df = pd.read_csv(args.output + "/evaluation.csv")
        heatmap_data = ModelHeatMap.read_json(args.output + "/heatmap.json")
    
    
    # get model names for plots
    model_names = df["Model"].tolist()
    
    # bar plots with correct, wrong and unanswered questions
    num_correct = np.array(df["Num_Correct"].tolist())
    num_wrong = np.array(df["Num_Wrong"].tolist())
    num_unanswered = np.array(df["Num_Unanswered"].tolist())
    show_answer_bars(num_correct, num_wrong, num_unanswered, model_names, "Richtig, Falsch und Unbeantwortete Fragen", args.output+"/answers_total.png")
    for model in model_names:
        show_heatmap(heatmap_data.get_heatmap(model, "makrof1"), f"Makro F1 ({model})", args.output+f"/makrof1_{model}_heat.png")
    
    for type in QuestionType:
        num_correct = np.array(df[f"Num_Correct_{type}"].tolist())
        num_wrong = np.array(df[f"Num_Wrong_{type}"].tolist())
        num_unanswered = np.array(df[f"Num_Unanswered_{type}"].tolist())
        show_answer_bars(num_correct, num_wrong, num_unanswered, model_names, f"Richtig, Falsch und Unbeantwortete Fragen ({type})", args.output+f"/answers_{type}.png")
    for source in QuestionSource:
        num_correct = np.array(df[f"Num_Correct_{source}"].tolist())
        num_wrong = np.array(df[f"Num_Wrong_{source}"].tolist())
        num_unanswered = np.array(df[f"Num_Unanswered_{source}"].tolist())
        show_answer_bars(num_correct, num_wrong, num_unanswered, model_names, f"Richtig, Falsch und Unbeantwortete Fragen ({source})", args.output+f"/answers_{source}.png")
    # bar plots with macro f1 scores
    
    show_makrof1_bars(df["MacroF1"].tolist(), model_names, "Makro F1", args.output+"/makro_total.png")
    for type in QuestionType:
        show_makrof1_bars(df[f"MacroF1_{type}"].tolist(), model_names, f"Makro F1 ({type})", args.output+f"/makro_{type}.png")
    for source in QuestionSource:
        show_makrof1_bars(df[f"MacroF1_{source}"].tolist(), model_names, f"Makro F1 ({source})", args.output+f"/makro_{source}.png")

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
        for type in QuestionType:
            for source in QuestionSource:
                heatmap_data.set_value(model, type, source, "correct", 0)
                heatmap_data.set_value(model, type, source, "wrong", 0)
                heatmap_data.set_value(model, type, source, "unanswered", 0)
                heatmap_data.set_value(model, type, source, "makrof1", 0)
                heatmap_data.set_value(model, type, source, "f1", [])
        # for source in QuestionSource:
        #     heatmap_data.set_value(model, "total", source, "correct", 0)
        #     heatmap_data.set_value(model, "total", source, "wrong", 0)
        #     heatmap_data.set_value(model, "total", source, "unanswered", 0)
        #     heatmap_data.set_value(model, "total", source, "makrof1", 0)
        #     heatmap_data.set_value(model, "total", source, "f1", [])
    
    # initialize pandas dataframe
    dataframe_columns = ["Model", "Num_Correct", "Num_Wrong", "Num_Unanswered", "Num_Questions", "MacroF1"]
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
        for type in QuestionType:
            type_f1_scores[type] = []
            type_num_correct[type] = 0
            type_num_wrong[type] = 0
            type_num_unanswered[type] = 0
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
            type_f1_scores[QuestionType(question.type)].append(f1) # type: ignore
            source_f1_scores[QuestionSource(question.source)].append(f1) # type: ignore
            heatmap_data.append_value(name, question.type, question.source, "f1", f1)
            # heatmap_data.append_value(name, "total", question.source, "f1", f1)
            # increase counters depending on question type
            # and if question was answered correctly, wrong or not at all
            if(question.answered == 0):
                num_unanswered += 1
                type_num_unanswered[QuestionType(question.type)] += 1 # type: ignore
                source_num_unanswered[QuestionSource(question.source)] += 1 # type: ignore
                heatmap_data.update_value(name, question.type, question.source, "unanswered", 1)
                # heatmap_data.update_value(name, "total", question.source, "unanswered", 1)
            elif(question.answered == 1):
                num_wrong += 1
                type_num_wrong[QuestionType(question.type)] += 1 # type: ignore
                source_num_wrong[QuestionSource(question.source)] += 1 # type: ignore
                heatmap_data.update_value(name, question.type, question.source, "wrong", 1)
                # heatmap_data.update_value(name, "total", question.source, "wrong", 1)
            elif(question.answered == 2):
                num_correct += 1
                type_num_correct[QuestionType(question.type)] += 1 # type: ignore
                source_num_correct[QuestionSource(question.source)] += 1 # type: ignore
                heatmap_data.update_value(name, question.type, question.source, "correct", 1)
                # heatmap_data.update_value(name, "total", question.source, "correct", 1)
        
        # calcualte macro f1 scores
        macro_f1 = sum(f1_scores) / len(f1_scores)
        type_macro_f1: dict[QuestionType, float] = {}
        source_macro_f1: dict[QuestionSource, float] = {}
        for type in QuestionType:
            type_macro_f1[type] = sum(type_f1_scores[type]) / len(type_f1_scores[type])
            for source in QuestionSource:
                type_f1: list[int] = heatmap_data.get_value(name, type, source, "f1") # type: ignore
                type_makro_f1 = sum(type_f1) / len(type_f1)
                heatmap_data.set_value(name, type, source, "makrof1", type_makro_f1)
        for source in QuestionSource:
            source_macro_f1[source] = sum(source_f1_scores[source]) / len(source_f1_scores[source])
            # total_f1: list[int] = heatmap_data.get_value(name, "total", source, "f1") # type: ignore
            # total_makro_f1 = sum(total_f1) / len(total_f1)
            # heatmap_data.set_value(name, "total", source, "makrof1", total_makro_f1)


        # and the total amount of questions per type
        questions = num_correct + num_wrong + num_unanswered
        type_questions: dict[QuestionType, int] = {}
        source_questions: dict[QuestionSource, int] = {}
        for type in QuestionType:
            type_questions[type] = type_num_correct[type] + type_num_wrong[type] + type_num_unanswered[type]
        for source in QuestionSource:
            source_questions[source] = source_num_correct[source] + source_num_wrong[source] + source_num_unanswered[source]
            
        # add to dataframe
        final_results = [name, num_correct, num_wrong, num_unanswered, questions, macro_f1]
        final_results.extend([type_num_correct[type] for type in QuestionType])
        final_results.extend([type_num_wrong[type] for type in QuestionType])
        final_results.extend([type_num_unanswered[type] for type in QuestionType])
        final_results.extend([type_questions[type] for type in QuestionType])
        final_results.extend([type_macro_f1[type] for type in QuestionType])
        final_results.extend([source_num_correct[source] for source in QuestionSource])
        final_results.extend([source_num_wrong[source] for source in QuestionSource])
        final_results.extend([source_num_unanswered[source] for source in QuestionSource])
        final_results.extend([source_questions[source] for source in QuestionSource])
        final_results.extend([source_macro_f1[source] for source in QuestionSource])
        df.loc[len(df)] = final_results # type: ignore
    
    # save data to csv
    df.to_csv(args.output + "/evaluation.csv", index=False)
    heatmap_data.save_json(args.output + "/heatmap.json")
    return df, heatmap_data

def show_heatmap(heatmap_data: tuple[list[str], list[str], list[list[float]]], title: str, file_name: str):
    y_labels = heatmap_data[0]
    x_labels = heatmap_data[1]
    values = np.array(heatmap_data[2])
    fig = plt.figure(figsize=(8,6))
    axis = fig.subplots()
    
    seaborn.heatmap(values, xticklabels=x_labels, yticklabels=y_labels, ax=axis, vmin=1, vmax=0)
    axis.set_ylabel("Makro F1")
    axis.set_xlabel("Modelle")
    axis.set_title(title, pad=15)
    fig.tight_layout()
    fig.savefig(file_name)

def show_answer_bars(correct, wrong, unanswered, names, title, file_name):
    # create figure of 20, 10 size
    fig = plt.figure(figsize=(8,6))
    # subplots() to get axis object
    axis = fig.subplots()
    # create stacked bars dataset
    answers = {
        "Korrekt": correct,
        "Falsch": wrong,
        "Unbeantwortet": unanswered
    }
    # create bottom array with 0
    bottom = np.zeros(len(names))
    # and define colors (backwards because of stacking)
    colors = ["silver", "lightcoral", "green"]
    # for each label in answers dataset
    for labels, answer in answers.items():
        # create the bars for each model
        bars = axis.bar(names, answer, width=0.5, label=labels, bottom=bottom, color=colors.pop())
        # stack next bars on top
        bottom += answer
        # enable labeling of bars
        axis.bar_label(bars)
    x_ticks = axis.get_xticks()
    axis.set_xticks(x_ticks, labels=names, rotation=45)
    # add legend
    axis.legend()
    # y axis legend
    axis.set_ylabel("Anzahl der Fragen")
    # title with padding because bar labels might overlap
    axis.set_title(title, pad=15)
    # save figure
    fig.tight_layout()
    fig.savefig(file_name)

def show_makrof1_bars(f1, names, title, file_name):
    # create figure of size 20, 10
    fig = plt.figure(figsize=(8,6))
    # subplots to get axis object
    axis = fig.subplots()
    # create bars
    bars = axis.bar(names, f1, width=0.5)
    x_ticks = axis.get_xticks()
    axis.set_xticks(x_ticks, labels=names, rotation=45)
    # label bars
    axis.bar_label(bars)
    # set y axis label
    axis.set_ylabel("Makro F1")
    # set title and padding as bar labels might overlap
    axis.set_title(title, pad=15)
    # and save the figure
    fig.tight_layout()
    fig.savefig(file_name)

if __name__ == "__main__":
    main()
