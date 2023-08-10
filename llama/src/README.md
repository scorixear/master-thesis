# Description

Contains scripts for training and evaluation of the `LLaMA2` model as well as its results.

# Folder Structure

- `.env`: conda environment folder containing all libraries needed to train the model
- `data`: questions used for evaluation. Json Structure further below. Contains also questions with spelling mistakes
- `ds_configs`: DeepSpeed Configuration Files for each stage with and without cpu offloading
- `evaluation`: Contains input and results of the evaluation of the model
  - `criteries`: Contains the evaluated criteria
    - `correctness`: Number of Questions answered correctly in total, per Question Type and their calculated Macro F1 scores
    - `explainability`: Number of Answers that contained an explanation in addition to the answer
    - `question_understanding`: Number of Questions that were understood by the model (but possibly not answered correctly)
    - `robustness`: Comparison of Correctness between Questions with and without spelling mistakes
  - `input`: Generated Answers by each model used for `correctness`, `explainability` and `question_understanding`
  - `spelling`: Generated Answers by each model for questions with spelling mistakes; used for `robustness`
- `input`: Training Dataset, contains cleaned up "Health Information Systems" book in Markdown format
- `output`: Contains Generated Answers by each model for questions with and without spelling mistakes. Json structure further below.
- `slurm`: Contains slurm job files used to run training and evaluation scripts
- `trained`: Contains trained models (currently only 3 epochs, not included in git due to size)

# Training Scripts
- `01_download_llama.sh`: Script provided by Meta for downloading the LLaMA weights
- `02_prepare_weights.py`: Script provided by Huggingface for converting the LLaMA weights to a format that can be used by the Huggingface library
- `03_train_llama.py`: Script for training the LLaMA model
- `03_train_llama2.py`: Script for training the LLaMA2 model
- `03_train_lora.py`: Script for training the LLaMA2 model with LoRA Adapter
- `03_trainig_args.json`: Example training arguments for the LLaMA2 model training script
- `04_predict_llama2_base.py`: Script for generating answers with the not continual pretrained (out of the box) LLaMA2 model
- `04_predict_llama2.py`: Script for generating answers of continual pretrained LLaMA2 models
- `05_evaluation_generation.py`: Script for rating/evaluating the generated answers by a model. Requires specific JSON structure (see below) from `04_predict_llama2.py`
- `05.2_evalutation_generation.py`: Script for extended evaluation of the generated answers by a model. Requires specific JSON structure (see below) from `05_evaluation_generation.py`
- `06_evaluation_correctness.py`: Script for calculating the correctness of the generated answers by a model. Requires specific JSON structure (see below) from `05.2_evalutation_generation.py`
- `06_evaluation_explainability_01.py`: Script for calculating the explainability of the generated answers by a model. Requires specific JSON structure (see below) from `05.2_evalutation_generation.py`
- `06_evaluation_explainability_02.py`: Script for generating bar plots from the results of `06_evaluation_explainability_01.py`
- `06_evaluation_question_understanding_01.py`: Script for calculating the question understanding of the generated answers by a model. Requires specific JSON structure (see below) from `05.2_evalutation_generation.py`
- `06_evaluation_question_understanding_02.py`: Script for generating bar plots from the results of `06_evaluation_question_understanding_01.py`	
- `06_evaluation_robustness.py`: Script for calculating the robustness of the generated answers by a model. Requires specific JSON structure (see below) from `05.2_evalutation_generation.py` and results from `06_evaluation_correctness.py`
- `ds_config.md`: contains annotations for the DeepSpeed configuration files
- `Finetune_Llama_Lora.ipynb`: Jupyter Notebook from `useftn.com` to finetune the LLaMA2 model with LoRA Adapter
- `question.py`: Question Class used in `06_evaluation_`-files to read in json data.
- `requirements.txt`: Python libraries needed to run the training scripts (`04`)


# JSON Structures

## For Generating Answers
Required for scripts `04_predict_llama2_base.py` and `04_predict_llama2.py`.
Examples can be found in `/data`.
```json
[
    {
        "Fragen": "Example Question", <-- this is the actual question / questions from the sources
        "Umformuliert": "Example Question", <-- this is the question that was used for generating answers. It is "Fragen" translated to english and slightly modified.
        "Antworten": "Example Answer", <-- this is the true answer that is expected
        "Anahl_Antworten": 1, <-- number of answers that are in "Antworten" contained
        "Quelle": "Example Source", <-- source of the question
        "Kontext": "Example Context", <-- context of the question
    }
]
```

For generation both scripts need the following json files:
- `single_questions.json`
- `multi_questions.json`
- `transfer_questions.json`

## For Evaluating generated Answers
Required for script `05_evaluation_generation.py`.
Generated by `04_predict_llama2.py` or `04_predict_llama2_base.py`.
Examples can be found in `/output` named `generated_*.json`

```json
[
    {
        "Question": "Example Question", <-- this is the actual question / questions from the sources
        "Transformed": "Example Question", <-- this is the question that was used for generating answers. It is "Fragen" translated to english and slightly modified.
        "Generated": "Example Answer", <-- this is the generated answer
        "True_Answer": "Example Answer", <-- this is the true answer that is expected
        "Num_Answers": 1, <-- number of answers that are in "True_Answer" contained
        "Type": "single", <-- type of question, either "single", "multi" or "transfer"
        "Source": "Example Source", <-- source of the question
        "Context": "Example Context", <-- context of the question
        "True_Input": "Example Input", <-- actual input that was used for generating the answer
    }
]
```

## For extended Evaluation of generated Answers
Required for script `05.2_evaluation_generation.py`.
Generated by `05_evaluation_generation.py`.
Examples can be found in `/output` named `evaluated_*.json`

```json
[
    {
        "question": "Example Question", <-- this is the actual question / questions from the sources
        "transformed": "Example Question", <-- this is the question that was used for generating answers. It is "Fragen" translated to english and slightly modified.
        "generated": "Example Answer", <-- this is the generated answer
        "true_answer": "Example Answer", <-- this is the true answer that is expected
        "num_answers": 1, <-- number of answers that are in "true_answer" contained
        "type": "single", <-- type of question, either "single", "multi" or "transfer"
        "source": "Example Source", <-- source of the question
        "context": "Example Context", <-- context of the question
        "true_input": "Example Input", <-- actual input that was used for generating the answer
        "answered": 2, <-- if the question was answered correctly, 0 if answer is not related to question, 1 if wrong, 2 if correct
        "points": 1, <-- number of correct answers in the generated answer. Between 0 and "num_answers"
    }
]
```

## For Calculating Criterias
Required for scripts `06_evaluation_correctness.py`, `06_evaluation_explainability_01.py`, `06_evaluation_question_understanding_01.py` and `06_evaluation_robustness.py`.
Generated by `05.2_evaluation_generation.py`.
Examples can be found under `/output` named `evaluated_*_2.json`.

```json
[
    {
        "question": "Example Question", <-- this is the actual question / questions from the sources
        "transformed": "Example Question", <-- this is the question that was used for generating answers. It is "Fragen" translated to english and slightly modified.
        "generated": "Example Answer", <-- this is the generated answer
        "true_answer": "Example Answer", <-- this is the true answer that is expected
        "num_answers": 1, <-- number of answers that are in "true_answer" contained
        "type": "single", <-- type of question, either "single", "multi" or "transfer"
        "source": "Example Source", <-- source of the question
        "context": "Example Context", <-- context of the question
        "true_input": "Example Input", <-- actual input that was used for generating the answer
        "answered": 2, <-- if the question was answered correctly, 0 if answer is not related to question, 1 if wrong, 2 if correct
        "points": 1, <-- number of correct answers in the generated answer. Between 0 and "num_answers"
        "total_answers": 1, <-- total number of answers in the generated answer
    }
]
```

## For Plotting Explainability
Required for script `06_evaluation_explainability_02.py`.
Generated by `06_evaluation_explainability_01.py`.
Examples can be found under `/evaluation/criterias/explainability` named `[model]_[not]_explained.json`

```json
[
    {
        "question": "Example Question", <-- this is the actual question / questions from the sources
        "transformed": "Example Question", <-- this is the question that was used for generating answers. It is "Fragen" translated to english and slightly modified.
        "generated": "Example Answer", <-- this is the generated answer
        "true_answer": "Example Answer", <-- this is the true answer that is expected
        "num_answers": 1, <-- number of answers that are in "true_answer" contained
        "type": "single", <-- type of question, either "single", "multi" or "transfer"
        "source": "Example Source", <-- source of the question
        "context": "Example Context", <-- context of the question
        "true_input": "Example Input", <-- actual input that was used for generating the answer
        "answered": 2, <-- if the question was answered correctly, 0 if answer is not related to question, 1 if wrong, 2 if correct
        "points": 1, <-- number of correct answers in the generated answer. Between 0 and "num_answers"
        "total_answers": 1, <-- total number of answers in the generated answer
    }
]
```

## For Plotting Question Understanding
Required for script `06_evaluation_question_understanding_02.py`.
Generated by `06_evaluation_question_understanding_01.py`.
Examples can be found under `/evaluation/criterias/question_understanding` named `[model]_[not]_understood.json`

```json
[
    {
        "question": "Example Question", <-- this is the actual question / questions from the sources
        "transformed": "Example Question", <-- this is the question that was used for generating answers. It is "Fragen" translated to english and slightly modified.
        "generated": "Example Answer", <-- this is the generated answer
        "true_answer": "Example Answer", <-- this is the true answer that is expected
        "num_answers": 1, <-- number of answers that are in "true_answer" contained
        "type": "single", <-- type of question, either "single", "multi" or "transfer"
        "source": "Example Source", <-- source of the question
        "context": "Example Context", <-- context of the question
        "true_input": "Example Input", <-- actual input that was used for generating the answer
        "answered": 2, <-- if the question was answered correctly, 0 if answer is not related to question, 1 if wrong, 2 if correct
        "points": 1, <-- number of correct answers in the generated answer. Between 0 and "num_answers"
        "total_answers": 1, <-- total number of answers in the generated answer
    }
]
```
