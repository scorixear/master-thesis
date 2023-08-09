import os
import json_fix
import argparse
import matplotlib.pyplot as plt
import numpy as np

from question import Question
from pandas import DataFrame
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Evaluation of the generated questions")
    parser.add_argument("-d", "--data", type=str, help="Path to the evaluated questions", default="evaluation/spelling")
    parser.add_argument("-e", "--eval", type=str, help="Path to the evaluation file", default="evaluation/criterias/correctness/evaluation.csv")
    parser.add_argument("-o", "--output", type=str, help="Path to the output file", default="evaluation/criterias/robustness")
    args = parser.parse_args()
    
    models: list[list[Question]] = []
    model_names = []
    for file in os.listdir(args.data):
        if file.endswith(".json"):
            model_names.append(file[:-5])
            models.append(Question.read_json(os.path.join(args.data, file)))
    df = DataFrame(columns=["Model", "Num_Correct", "Num_Wrong", "Num_Unanswered", "Num_Questions", "MacroF1", "Num_Correct_Single", "Num_Wrong_Single", "Num_Unanswered_Single", "Num_Questions_Single", "MacroF1_Single", "Num_Correct_Multi", "Num_Wrong_Multi", "Num_Unanswered_Multi", "Num_Questions_Multi", "MacroF1_Multi", "Num_Correct_Transfer", "Num_Wrong_Transfer", "Num_Unanswered_Transfer", "Num_Questions_Transfer", "MacroF1_Transfer"])
    
    evaluated = pd.read_csv(args.eval)
    
    for index, model in enumerate(models):
        name = model_names[index]
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
        f1_scores = []
        single_f1_scores = []
        multi_f1_scores = []
        transfer_f1_scores = []
        
        for question in model:
            correct: float = question.points
            true: float = question.num_answers
            total: float = question.total_answers
            if total == 0 or true == 0:
                f1: float = 0
            else:
                prec = correct / total
                recall = correct / true
                if prec + recall == 0:
                    f1: float = 0
                else:
                    f1: float = 2*(prec*recall)/(prec+recall)
            f1_scores.append(f1)
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
        macro_f1 = sum(f1_scores) / len(f1_scores)
        macro_f1_single = sum(single_f1_scores) / len(single_f1_scores)
        macro_f1_multi = sum(multi_f1_scores) / len(multi_f1_scores)
        macro_f1_transfer = sum(transfer_f1_scores) / len(transfer_f1_scores)
        
        questions = num_correct + num_wrong + num_unanswered
        questions_single = num_single_correct + num_single_wrong + num_single_unanswered
        questions_multi = num_multi_correct + num_multi_wrong + num_multi_unanswered
        questions_transfer = num_transfer_correct + num_transfer_wrong + num_transfer_unanswered
        
        df.loc[len(df)] = [name, num_correct, num_wrong, num_unanswered, questions, macro_f1, num_single_correct, num_single_wrong, num_single_unanswered, questions_single, macro_f1_single, num_multi_correct, num_multi_wrong, num_multi_unanswered, questions_multi, macro_f1_multi, num_transfer_correct, num_transfer_wrong, num_transfer_unanswered, questions_transfer, macro_f1_transfer]
        
    df.to_csv(args.output + "/evaluation.csv", index=False)
    
    model_names = df["Model"].tolist()
    
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
    
    show_makrof1_bars(df["MacroF1"].toList(), model_names, "Makro F1 - Robustheit", args.output + "/makro_total.png")
    show_makrof1_bars(df["MacroF1_Single"].toList(), model_names, "Makro F1 (Single) - Robustheit", args.output + "/makro_single.png")
    show_makrof1_bars(df["MacroF1_Multi"].toList(), model_names, "Makro F1 (Multi) - Robustheit", args.output + "/makro_multi.png")
    show_makrof1_bars(df["MacroF1_Transfer"].toList(), model_names, "Makro F1 (Transfer) - Robustheit", args.output + "/makro_transfer.png")
    
    
    makro_eval = evaluated["MacroF1"].tolist()
    makro_eval_single = evaluated["MacroF1_Single"].tolist()
    makro_eval_multi = evaluated["MacroF1_Multi"].tolist()
    makro_eval_transfer = evaluated["MacroF1_Transfer"].tolist()
    
    show_comparison_bars(df["MacroF1"].tolist(), makro_eval, model_names, "Makro F1 Vergleich - Robustheit", args.output + "/makro_comparison.png")
    show_comparison_bars(df["MacroF1_Single"].tolist(), makro_eval_single, model_names, "Makro F1 Vergleich (Single) - Robustheit", args.output + "/makro_single_comparison.png")
    show_comparison_bars(df["MacroF1_Multi"].tolist(), makro_eval_multi, model_names, "Makro F1 Vergleich (Multi) - Robustheit", args.output + "/makro_multi_comparison.png")
    show_comparison_bars(df["MacroF1_Transfer"].tolist(), makro_eval_transfer, model_names, "Makro F1 Vergleich (Transfer) - Robustheit", args.output + "/makro_transfer_comparison.png")

    #plt.show()
    
def show_answer_bars(correct, wrong, unanswered, names, title, file_name):
    fig = plt.figure(figsize=(20, 10))
    axis = fig.subplots()
    answers = {
        "Korrekt": correct,
        "Falsch": wrong,
        "Unbeantwortet": unanswered
    }
    
    bottom = np.zeros(len(names))
    colors = ["grey", "red", "green"]
    for labels, answer in answers.items():
        bars = axis.bar(names, answer, width=0.5, label=labels, bottom=bottom, colors=colors.pop())
        bottom += answer
        axis.bar_label(bars)
    axis.legend()
    axis.set_title(title, pad=15)
    fig.savefig(file_name)
def show_makrof1_bars(f1, names, title, file_name):
    fig = plt.figure(figsize=(20, 10))
    axis = fig.subplots()
    
    bars = axis.bar(names, f1, width=0.5)
    axis.bar_label(bars)
    axis.set_title(title, pad=15)
    fig.savefig(file_name)

def show_comparison_bars(f1, evalf1, names, title, file_name):
    x_labels = np.arange(len(names))
    width = 0.25
    multiplier = 0
    
    fig, axis = plt.subplots(figsize=(20, 10), layout="constrained")
    f1_scores = {
        "Normal": evalf1,
        "Fehlerhaft": f1
    }
    
    for label, f1_score in f1_scores.items():
        offset = width*multiplier
        bars = axis.bar(x_labels+offset, f1_score, width, label=label)
        axis.bar_label(bars, padding=3)
        multiplier += 1

    axis.set_ylabel("MakroF1")
    axis.set_title(title, pad=15)
    axis.set_xticks(x_labels+width, names)
    axis.legend(loc="upper left", ncols=2)
    axis.set_ylim(0, 250)
    
    fig.savefig(file_name)

if __name__ == "__main__":
    main()