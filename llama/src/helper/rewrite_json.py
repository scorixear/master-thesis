import json

file_path = "llama/src/output/generated_1e_spelling.json"

with open(file_path, "r", encoding="UTF-8") as f:
    data = json.load(f)
with open(file_path, "w", encoding="UTF-8") as f:
    new_data = []
    for d in data:
        new_data.append({
            "question": d["Question"],
            "transformed": d["Transformed"],
            "generated": d["Generated"],
            "true_answer": d["True_Answer"],
            "num_answers": d["Num_Answers"],
            "type": d["Type"],
            "source": d["Source"],
            "context": d["Context"],
            "true_input": d["True_Input"]
        })
    json.dump(new_data, f, indent=2)
