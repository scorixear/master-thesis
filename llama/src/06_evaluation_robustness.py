import os
import json_fix # this import is needed for def __json__(self) although not used
import argparse
import matplotlib.pyplot as plt
import numpy as np

from question import Question
from pandas import DataFrame
import pandas as pd


def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="Evaluation of the generated questions")
    # path to evaluated questions json file directory
    parser.add_argument("-d", "--data", type=str, help="Path to the evaluated questions", default="evaluation/spelling")
    # path to correctness evaluation csv file
    parser.add_argument("-e", "--eval", type=str, help="Path to the evaluation file", default="evaluation/criterias/correctness/evaluation.csv")
    # path to output directory
    parser.add_argument("-o", "--output", type=str, help="Path to the output directory", default="evaluation/criterias/robustness")
    args = parser.parse_args()
    
    models: list[list[Question]] = []
    model_names = []
    # read in all json files in directory
    for file in os.listdir(args.data):
        # only read json files
        if file.endswith(".json"):
            # remove .json to get model name
            model_names.append(file[:-5])
            # and parse questions
            models.append(Question.read_json(os.path.join(args.data, file)))
    # initialize pandas dataframe
    df = DataFrame(columns=["Model", "Num_Correct", "Num_Wrong", "Num_Unanswered", "Num_Questions", "MacroF1", "Num_Correct_Single", "Num_Wrong_Single", "Num_Unanswered_Single", "Num_Questions_Single", "MacroF1_Single", "Num_Correct_Multi", "Num_Wrong_Multi", "Num_Unanswered_Multi", "Num_Questions_Multi", "MacroF1_Multi", "Num_Correct_Transfer", "Num_Wrong_Transfer", "Num_Unanswered_Transfer", "Num_Questions_Transfer", "MacroF1_Transfer"])
    
    # read in correctness evaluation
    evaluated = pd.read_csv(args.eval)
    # for each model
    for index, model in enumerate(models):
        # get name
        name = model_names[index]
        # initialize counters
        num_correct = 0
        num_wrong = 0
        num_unanswered = 0
        num_single_correct = 0
        num_single_wrong = 0
        num_single_unanswered = 0
        num_multi_correct = 0
        num_multi_wrong = 0
        num_multi_unanswered = 0
        num_transfer_correct = 0
        num_transfer_wrong = 0
        num_transfer_unanswered = 0
        # initialize f1 scores
        f1_scores = []
        single_f1_scores = []
        multi_f1_scores = []
        transfer_f1_scores = []
        
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
                    f1: float = 2*(prec*recall)/(prec+recall)
            # and append
            f1_scores.append(f1)
            # count correct, wrong and unanswered questions
            # for each question type
            if question.answered == 0:
                num_unanswered += 1
            elif question.answered == 1:
                num_wrong += 1
            elif question.answered == 2:
                num_correct += 1
            if question.type == "single":
                if question.answered == 0:
                    num_single_unanswered += 1
                elif question.answered == 1:
                    num_single_wrong += 1
                elif question.answered == 2:
                    num_single_correct += 1
                single_f1_scores.append(f1)
            elif question.type == "multi":
                if question.answered == 0:
                    num_multi_unanswered += 1
                elif question.answered == 1:
                    num_multi_wrong += 1
                elif question.answered == 2:
                    num_multi_correct += 1
                multi_f1_scores.append(f1)
            elif question.type == "transfer":
                if question.answered == 0:
                    num_transfer_unanswered += 1
                elif question.answered == 1:
                    num_transfer_wrong += 1
                elif question.answered == 2:
                    num_transfer_correct += 1
                transfer_f1_scores.append(f1)
        # calculate macro f1 scores
        # but include max number of question answered
        # as they are counted as f1 = 0 in correctness
        # this represents the correct macro f1 score
        macro_f1 = sum(f1_scores) / 97
        macro_f1_single = sum(single_f1_scores) / 38
        macro_f1_multi = sum(multi_f1_scores) / 38
        macro_f1_transfer = sum(transfer_f1_scores) / 21
        
        # and calculate total number of questions
        questions = num_correct + num_wrong + num_unanswered
        questions_single = num_single_correct + num_single_wrong + num_single_unanswered
        questions_multi = num_multi_correct + num_multi_wrong + num_multi_unanswered
        questions_transfer = num_transfer_correct + num_transfer_wrong + num_transfer_unanswered
        
        # append to dataframe
        df.loc[len(df)] = [name, num_correct, num_wrong, num_unanswered, questions, macro_f1, num_single_correct, num_single_wrong, num_single_unanswered, questions_single, macro_f1_single, num_multi_correct, num_multi_wrong, num_multi_unanswered, questions_multi, macro_f1_multi, num_transfer_correct, num_transfer_wrong, num_transfer_unanswered, questions_transfer, macro_f1_transfer]
    # save dataframe
    df.to_csv(args.output + "/evaluation.csv", index=False)
    
    model_names = df["Model"].tolist()
    
    # create bar plots for correct, wrong and unanswered questions
    num_correct = np.array(df["Num_Correct"].tolist())
    num_wrong = np.array(df["Num_Wrong"].tolist())
    num_unanswered = np.array(df["Num_Unanswered"].tolist())
    show_answer_bars(num_correct, num_wrong, num_unanswered, model_names, "Richtig, Falsch und Unbeantwortete Fragen - Robustheit", args.output + "/answers_total.png")
    
    num_single_correct = np.array(df["Num_Correct_Single"].tolist())
    num_single_wrong = np.array(df["Num_Wrong_Single"].tolist())
    num_single_unanswered = np.array(df["Num_Unanswered_Single"].tolist())
    show_answer_bars(num_single_correct, num_single_wrong, num_single_unanswered, model_names, "Richtig, Falsch und Unbeantwortete Fragen (Single) - Robustheit", args.output + "/answers_single.png")
    
    num_multi_correct = np.array(df["Num_Correct_Multi"].tolist())
    num_multi_wrong = np.array(df["Num_Wrong_Multi"].tolist())
    num_multi_unanswered = np.array(df["Num_Unanswered_Multi"].tolist())
    show_answer_bars(num_multi_correct, num_multi_wrong, num_multi_unanswered, model_names, "Richtig, Falsch und Unbeantwortete Fragen (Multi) - Robustheit", args.output + "/answers_multi.png")
    
    num_transfer_correct = np.array(df["Num_Correct_Transfer"].tolist())
    num_transfer_wrong = np.array(df["Num_Wrong_Transfer"].tolist())
    num_transfer_unanswered = np.array(df["Num_Unanswered_Transfer"].tolist())
    show_answer_bars(num_transfer_correct, num_transfer_wrong, num_transfer_unanswered, model_names, "Richtig, Falsch und Unbeantwortete Fragen (Transfer) - Robustheit", args.output + "/answers_transfer.png")
    
    # create bar plots for macro f1 scores
    show_makrof1_bars(df["MacroF1"].tolist(), model_names, "Makro F1 - Robustheit", args.output + "/makro_total.png")
    show_makrof1_bars(df["MacroF1_Single"].tolist(), model_names, "Makro F1 (Single) - Robustheit", args.output + "/makro_single.png")
    show_makrof1_bars(df["MacroF1_Multi"].tolist(), model_names, "Makro F1 (Multi) - Robustheit", args.output + "/makro_multi.png")
    show_makrof1_bars(df["MacroF1_Transfer"].tolist(), model_names, "Makro F1 (Transfer) - Robustheit", args.output + "/makro_transfer.png")
    
    # extract data from correctness evaluation
    makro_eval = evaluated["MacroF1"].tolist()
    makro_eval_single = evaluated["MacroF1_Single"].tolist()
    makro_eval_multi = evaluated["MacroF1_Multi"].tolist()
    makro_eval_transfer = evaluated["MacroF1_Transfer"].tolist()
    
    # and create bar plots for comparison
    show_comparison_bars(df["MacroF1"].tolist(), makro_eval, model_names, "Makro F1 Vergleich - Robustheit", args.output + "/makro_comparison.png")
    show_comparison_bars(df["MacroF1_Single"].tolist(), makro_eval_single, model_names, "Makro F1 Vergleich (Single) - Robustheit", args.output + "/makro_single_comparison.png")
    show_comparison_bars(df["MacroF1_Multi"].tolist(), makro_eval_multi, model_names, "Makro F1 Vergleich (Multi) - Robustheit", args.output + "/makro_multi_comparison.png")
    show_comparison_bars(df["MacroF1_Transfer"].tolist(), makro_eval_transfer, model_names, "Makro F1 Vergleich (Transfer) - Robustheit", args.output + "/makro_transfer_comparison.png")
    
def show_answer_bars(correct, wrong, unanswered, names, title, file_name):
    # create figure of size 20, 10
    fig = plt.figure(figsize=(20, 10))
    # subplots() to get axis object
    axis = fig.subplots()
    # create stacked bars dataset
    answers = {
        "Korrekt": correct,
        "Falsch": wrong,
        "Unbeantwortet": unanswered
    }
    # bottom array for stacking bars
    bottom = np.zeros(len(names))
    # and colors per stack, in reverse order
    colors = ["silver", "lightcoral", "green"]
    # for each label, answer pair
    for labels, answer in answers.items():
        # create bar plot
        bars = axis.bar(names, answer, width=0.5, label=labels, bottom=bottom, color=colors.pop())
        # stack next plot ontop
        bottom += answer
        # and add bar labels
        axis.bar_label(bars)
    axis.legend()
    # set y-axis label
    axis.set_ylabel("Anzahl der Antworten")
    # set title, with padding as bar_labels might overlap
    axis.set_title(title, pad=15)
    # and save figure
    fig.savefig(file_name)

def show_makrof1_bars(f1, names, title, file_name):
    # create figure of size 20, 10
    fig = plt.figure(figsize=(20, 10))
    # subplots() to get axis object
    axis = fig.subplots()
    
    # create bar plot
    bars = axis.bar(names, f1, width=0.5)
    # and add bar labels
    axis.bar_label(bars)
    # set y-axis label
    axis.set_ylabel("Makro F1")
     # set title, with padding as bar_labels might overlap
    axis.set_title(title, pad=15)
    # and save figure
    fig.savefig(file_name)

def show_comparison_bars(f1, evalf1, names, title, file_name):
    # create new x labels as we stack bars now horizontally
    x_labels = np.arange(len(names))
    # with defined width of each bar
    width = 0.25
    # counter for offsetting bars
    multiplier = 0
    
    # create figure and axis objects
    fig, axis = plt.subplots(figsize=(20, 10), layout="constrained")
    # and stacked bars for each label
    f1_scores = {
        "Normal": evalf1,
        "Fehlerhaft": f1
    }
    
    # for each label and f1 score
    for label, f1_score in f1_scores.items():
        # calculate offset from actual x position
        offset = width*multiplier
        # and plot bars at offset
        bars = axis.bar(x_labels+offset, f1_score, width, label=label)
        # add bar labels
        axis.bar_label(bars, padding=3)
        # and increase multiplier
        multiplier += 1

    # y-axis label
    axis.set_ylabel("Makro F1")
    # title with padding, as bar_labels might overlap
    axis.set_title(title, pad=15)
    # reset x-axis labels to correct position and value
    axis.set_xticks(x_labels+width, names)
    # and add legend
    axis.legend(loc="upper left")
    # limit y axis to 0-1 as f1 only goes from 0-1
    axis.set_ylim(0, 1)
    # and save the figure
    fig.savefig(file_name)

if __name__ == "__main__":
    main()