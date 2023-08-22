import argparse
import pandas as pd
from question import QuestionType, QuestionSource
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description="Evaluation of the generated questions")
    parser.add_argument("-d", "--data", type=str, help="Path to correctness csv file", default="evaluation/criterias/correctness/evaluation.csv")
    parser.add_argument("-o", "--output", type=str, help="Path to output folder", default = "evaluation/criterias/ranking")
    
    args = parser.parse_args()
    if(args.output.endswith("/") or args.output.endswith("\\")):
        args.output = args.output[:-1]
    
    evaluated = pd.read_csv(args.data)
    
    ranking_variables = ["Num_Correct", "MacroF1"]
    ranking_reverse_variabels = ["Num_Unanswered"]
    
    ranking_variables.extend([f"Num_Correct_{qtype}" for qtype in QuestionType])
    ranking_variables.extend([f"MacroF1_{qtype}" for qtype in QuestionType])
    ranking_variables.extend([f"Num_Correct_{qsource}" for qsource in QuestionSource])
    ranking_variables.extend([f"MacroF1_{qsource}" for qsource in QuestionSource])
    
    ranking_reverse_variabels.extend([f"Num_Unanswered_{qtype}" for qtype in QuestionType])
    ranking_reverse_variabels.extend([f"Num_Unanswered_{qsource}" for qsource in QuestionSource])
    
    model_names = evaluated["Model"]
    
    ranked_results: dict[str, list[tuple[str, int]]] = {}
    
    for value in ranking_variables:
        unsorted_values: list[tuple[str, int]] = []
        for model in model_names:
            unsorted_values.append((model, evaluated[evaluated["Model"] == model][value].values[0]))
        sorted_values = sorted(unsorted_values, key=lambda x: x[1], reverse=True)
        ranked_results[value] = sorted_values
    for value in ranking_reverse_variabels:
        unsorted_values: list[tuple[str, int]] = []
        for model in model_names:
            unsorted_values.append((model, evaluated[evaluated["Model"] == model][value].values[0]))
        sorted_values = sorted(unsorted_values, key=lambda x: x[1])
        ranked_results[value] = sorted_values

    # num correct
    draw_ranking([x[1] for x in ranked_results["Num_Correct"]], [x[0] for x in ranked_results["Num_Correct"]], "Anzahl korrekter Antworten", "Anzahl korrekter Antworten", f"{args.output}/correct.png")
    draw_ranking([x[1] for x in ranked_results["Num_Unanswered"]], [x[0] for x in ranked_results["Num_Unanswered"]], "Anzahl unbeantworteter Fragen", "Anzahl unbeantworteter Fragen", f"{args.output}/unanswered.png")
    draw_ranking([x[1] for x in ranked_results["MacroF1"]], [x[0] for x in ranked_results["MacroF1"]], "Makro F1", "Makro F1", f"{args.output}/macrof1.png")
    for type in QuestionType:
        draw_ranking([x[1] for x in ranked_results[f"Num_Correct_{type}"]], [x[0] for x in ranked_results[f"Num_Correct_{type}"]], "Anzahl korrekter Antworten", f"Anzahl korrekter Antworten ({type})", f"{args.output}/correct_{type}.png")
        draw_ranking([x[1] for x in ranked_results[f"Num_Unanswered_{type}"]], [x[0] for x in ranked_results[f"Num_Unanswered_{type}"]], "Anzahl unbeantworteter Fragen", f"Anzahl unbeantworteter Fragen ({type})", f"{args.output}/unanswered_{type}.png")
        draw_ranking([x[1] for x in ranked_results[f"MacroF1_{type}"]], [x[0] for x in ranked_results[f"MacroF1_{type}"]], "Makro F1", f"Makro F1 ({type})", f"{args.output}/macrof1_{type}.png")
    for source in QuestionSource:
        draw_ranking([x[1] for x in ranked_results[f"Num_Correct_{source}"]], [x[0] for x in ranked_results[f"Num_Correct_{source}"]], "Anzahl korrekter Antworten", f"Anzahl korrekter Antworten ({source})", f"{args.output}/correct_{source}.png")
        draw_ranking([x[1] for x in ranked_results[f"Num_Unanswered_{source}"]], [x[0] for x in ranked_results[f"Num_Unanswered_{source}"]], "Anzahl unbeantworteter Fragen", f"Anzahl unbeantworteter Fragen ({source})", f"{args.output}/unanswered_{source}.png")
        draw_ranking([x[1] for x in ranked_results[f"MacroF1_{source}"]], [x[0] for x in ranked_results[f"MacroF1_{source}"]], "Makro F1", f"Makro F1 ({source})", f"{args.output}/macrof1_{source}.png")
    
def draw_ranking(data: list[int], labels: list[str], y_value: str, title: str, file_name: str):
    fig = plt.figure(figsize=(20,10))
    axis = fig.subplots()
    
    axis.plot(labels, data, marker="o")
    axis.set_title(title, pad=15)
    axis.set_xlabel("Model")
    axis.set_ylabel(y_value)
    fig.savefig(file_name)

if __name__ == "__main__":
    main()
