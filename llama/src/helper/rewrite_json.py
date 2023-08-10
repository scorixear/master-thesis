import json

file_path = "llama/src/data/multi_questions_spelling_llama2_1e.json"

with open(file_path, "r", encoding="UTF-8") as f:
    data = json.load(f)
with open(file_path, "w", encoding="UTF-8") as f:
    new_data = []
    for d in data:
        new_data.append({
            "question": d["Fragen"],
            "transformed": d["Umformuliert"],
            "true_answer": d["Antworten"],
            "num_answers": d["Anzahl_Antworten"],
            "source": d["Quelle"],
            "context": d["Kontext"],
        })
    json.dump(new_data, f, indent=2)
