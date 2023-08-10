import os
import json_fix # this import is needed for def __json__(self) although not used
import argparse
import matplotlib.pyplot as plt
import numpy as np

from question import Question

from pandas import DataFrame



def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="Evaluation of the generated questions")
    # path to evaluated questions json file
    parser.add_argument("-d", "--data", type=str, help="Path to the evaluated questions", 
                        default="evaluation/input")
    # path to output directory
    parser.add_argument("-o", "--output", type=str, help="Path to the output directory", default="evaluation/criterias/correctness")
    args = parser.parse_args()
    
    # read in evaluated questions
    models: list[list[Question]] = []
    model_names = []
    for file in os.listdir(args.data):
        # only read json files
        if file.endswith(".json"):
            # remove .json to get model name
            model_names.append(file[:-5])
            models.append(Question.read_json(os.path.join(args.data, file)))
    
    # initialize pandas dataframe
    df = DataFrame(columns=["Model", "Num_Correct", "Num_Wrong", "Num_Unanswered", "Num_Questions", "MacroF1", "Num_Correct_Single", "Num_Wrong_Single", "Num_Unanswered_Single", "Num_Questions_Single", "MacroF1_Single", "Num_Correct_Multi", "Num_Wrong_Multi", "Num_Unanswered_Multi", "Num_Questions_Multi", "MacroF1_Multi", "Num_Correct_Transfer", "Num_Wrong_Transfer", "Num_Unanswered_Transfer", "Num_Questions_Transfer", "MacroF1_Transfer"])
    
    # for each model
    for index, model in enumerate(models):
        # get model name
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
            # increase counters depending on question type
            # and if question was answered correctly, wrong or not at all
            if(question.answered == 0):
                num_unanswered += 1
            elif(question.answered == 1):
                num_wrong += 1
            elif(question.answered == 2):
                num_correct += 1
            if(question.type == "single"):
                if question.answered == 0:
                    num_single_unanswered += 1
                elif question.answered == 1:
                    num_single_wrong += 1
                elif question.answered == 2:
                    num_single_correct += 1
                single_f1_scores.append(f1)
            elif(question.type == "multi"):
                if question.answered == 0:
                    num_multi_unanswered += 1
                elif question.answered == 1:
                    num_multi_wrong += 1
                elif question.answered == 2:
                    num_multi_correct += 1
                multi_f1_scores.append(f1)
            elif(question.type == "transfer"):
                if question.answered == 0:
                    num_transfer_unanswered += 1
                elif question.answered == 1:
                    num_transfer_wrong += 1
                elif question.answered == 2:
                    num_transfer_correct += 1
                transfer_f1_scores.append(f1)
        # calcualte macro f1 scores
        macro_f1 = sum(f1_scores) / len(f1_scores)
        single_macro_f1 = sum(single_f1_scores) / len(single_f1_scores)
        multi_macro_f1 = sum(multi_f1_scores) / len(multi_f1_scores)
        transfer_macro_f1 = sum(transfer_f1_scores) / len(transfer_f1_scores)
        # and the total amount of questions per type
        questions = num_correct + num_wrong + num_unanswered
        single_questions = num_single_correct + num_single_wrong + num_single_unanswered
        multi_questions = num_multi_correct + num_multi_wrong + num_multi_unanswered
        transfer_questions = num_transfer_correct + num_transfer_wrong + num_transfer_unanswered
        # add to dataframe
        df.loc[len(df)] = [name, num_correct, num_wrong, num_unanswered, questions, macro_f1, num_single_correct, num_single_wrong, num_single_unanswered, single_questions, single_macro_f1, num_multi_correct, num_multi_wrong, num_multi_unanswered, multi_questions, multi_macro_f1, num_transfer_correct, num_transfer_wrong, num_transfer_unanswered, transfer_questions, transfer_macro_f1]
    
    # save data to csv
    df.to_csv(args.output + "/evaluation.csv", index=False)

    # get model names for plots
    model_names = df["Model"].tolist()
    
    # bar plots with correct, wrong and unanswered questions
    num_correct = np.array(df["Num_Correct"].tolist())
    num_wrong = np.array(df["Num_Wrong"].tolist())
    num_unanswered = np.array(df["Num_Unanswered"].tolist())
    show_answer_bars(num_correct, num_wrong, num_unanswered, model_names, "Richtig, Falsch und Unbeantwortete Fragen", args.output+"/answers_total.png")
    num_single_correct = np.array(df["Num_Correct_Single"].tolist())
    num_single_wrong = np.array(df["Num_Wrong_Single"].tolist())
    num_single_unanswered = np.array(df["Num_Unanswered_Single"].tolist())
    show_answer_bars(num_single_correct, num_single_wrong, num_single_unanswered, model_names, "Richtig, Falsch und Unbeantwortete Fragen (Single)", args.output+"/answers_single.png")
    num_multi_correct = np.array(df["Num_Correct_Multi"].tolist())
    num_multi_wrong = np.array(df["Num_Wrong_Multi"].tolist())
    num_multi_unanswered = np.array(df["Num_Unanswered_Multi"].tolist())
    show_answer_bars(num_multi_correct, num_multi_wrong, num_multi_unanswered, model_names, "Richtig, Falsch und Unbeantwortete Fragen (Multi)", args.output+"/answers_multi.png")
    num_transfer_correct = np.array(df["Num_Correct_Transfer"].tolist())
    num_transfer_wrong = np.array(df["Num_Wrong_Transfer"].tolist())
    num_transfer_unanswered = np.array(df["Num_Unanswered_Transfer"].tolist())
    show_answer_bars(num_transfer_correct, num_transfer_wrong, num_transfer_unanswered, model_names, "Richtig, Falsch und Unbeantwortete Fragen (Transfer)", args.output+"/answers_transfer.png")
    
    # bar plots with macro f1 scores
    show_makrof1_bars(df["MacroF1"].tolist(), model_names, "Makro F1", args.output+"/makro_total.png")
    show_makrof1_bars(df["MacroF1_Single"].tolist(), model_names, "Makro F1 (Single)", args.output+"/makro_single.png")
    show_makrof1_bars(df["MacroF1_Multi"].tolist(), model_names, "Makro F1 (Multi)", args.output+"/makro_multi.png")
    show_makrof1_bars(df["MacroF1_Transfer"].tolist(), model_names, "Makro F1 (Transfer)", args.output+"/makro_transfer.png")

def show_answer_bars(correct, wrong, unanswered, names, title, file_name):
    # create figure of 20, 10 size
    fig = plt.figure(figsize=(20,10))
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
    # add legend
    axis.legend()
    # y axis legend
    axis.set_ylabel("Anzahl der Fragen")
    # title with padding because bar labels might overlap
    axis.set_title(title, pad=15)
    # save figure
    fig.savefig(file_name)

def show_makrof1_bars(f1, names, title, file_name):
    # create figure of size 20, 10
    fig = plt.figure(figsize=(20,10))
    # subplots to get axis object
    axis = fig.subplots()
    # create bars
    bars = axis.bar(names, f1, width=0.5)
    # label bars
    axis.bar_label(bars)
    # set y axis label
    axis.set_ylabel("Makro F1")
    # set title and padding as bar labels might overlap
    axis.set_title(title, pad=15)
    # and save the figure
    fig.savefig(file_name)

if __name__ == "__main__":
    main()