# Description

Contains scripts for training and evaluation of the `LLaMA2` model as well as its results.

# Table of Contents
- [Description](#description)
- [Table of Contents](#table-of-contents)
- [Folder Structure](#folder-structure)
- [Training Scripts](#training-scripts)
- [Helper Scripts](#helper-scripts)
- [JSON Structures](#json-structures)
  - [For Generating Answers](#for-generating-answers)
  - [For Evaluating generated Answers](#for-evaluating-generated-answers)
  - [For extended Evaluation of generated Answers](#for-extended-evaluation-of-generated-answers)
  - [For Calculating Criterias](#for-calculating-criterias)
  - [For Plotting Explainability](#for-plotting-explainability)
  - [For Plotting Question Understanding](#for-plotting-question-understanding)
- [Generated Plots](#generated-plots)
  - [Correctness](#correctness)
  - [Explainability](#explainability)
  - [Loss](#loss)
  - [Question Understanding](#question-understanding)
  - [Ranking](#ranking)
  - [Robustness](#robustness)

# Folder Structure

- `.env`: conda environment folder containing all libraries needed to train the model
- `data`: questions used for evaluation. Json Structure further below. Contains also questions with spelling mistakes
- `ds_configs`: DeepSpeed Configuration Files for each stage with and without cpu offloading
  - `ds_config.md`: contains annotations for the DeepSpeed configuration files
- `evaluation`: Contains input and results of the evaluation of the model
  - `criteries`: Contains the evaluated criteria
    - `correctness`: Number of Questions answered correctly in total, per Question Type and their calculated Macro F1 scores
    - `explainability`: Number of Answers that contained an explanation in addition to the answer
    - `loss`: Validation and Training Loss over multiple epochs
    - `question_understanding`: Number of Questions that were understood by the model (but possibly not answered correctly)
    - `ranking`: Ranking graphs of different criterias of the evaluated models
    - `robustness`: Comparison of Correctness between Questions with and without spelling mistakes
  - `input`: Generated Answers by each model used for `correctness`, `explainability` and `question_understanding`
  - `spelling`: Generated Answers by each model for questions with spelling mistakes; used for `robustness`
- `helper`: Contains Helper Scripts used by the training and evaluation scripts
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
- `04_predict_llama2_4bit.py`: Script for generating answer of continual pretrained LLaMA2 models, but adjusted to use bitsandbytes to load in model as 4bit version. Uses less memory.
- `04_predict_llama2_base.py`: Script for generating answers with the not continual pretrained (out of the box) LLaMA2 model
- `04_predict_llama2_lora.py`: Script for generating answers with the Model trained with a LoRA Adapter. Currently not working.
- `04_predict_llama2.py`: Script for generating answers of continual pretrained LLaMA2 models
- `05_evaluation_generation.py`: Script for rating/evaluating the generated answers by a model. Requires specific JSON structure (see below) from `04_predict_llama2.py`
- `05.2_evalutation_generation.py`: Script for extended evaluation of the generated answers by a model. Requires specific JSON structure (see below) from `05_evaluation_generation.py`
- `06_evaluation_correctness.py`: Script for calculating the correctness of the generated answers by a model. Requires specific JSON structure (see below) from `05.2_evalutation_generation.py`
- `06_evaluation_explainability_01.py`: Script for calculating the explainability of the generated answers by a model. Requires specific JSON structure (see below) from `05.2_evalutation_generation.py`
- `06_evaluation_explainability_02.py`: Script for generating bar plots from the results of `06_evaluation_explainability_01.py`
- `06_evalation_loss.py`: Script for generating loss plots from the training of the models
- `06_evaluation_question_understanding_01.py`: Script for calculating the question understanding of the generated answers by a model. Requires specific JSON structure (see below) from `05.2_evalutation_generation.py`
- `06_evaluation_question_understanding_02.py`: Script for generating bar plots from the results of `06_evaluation_question_understanding_01.py`
- `06_evaluation_ranking.py`: Script for generating Ranking plots from the results of `06_evaluation_correctness.py`
- `06_evaluation_robustness_01.py`: Script for generating evaluation datasets with spelling mistakes. Requires output from `05.2_evaluation_generation.py` and the misspelled questions from `data`
- `06_evaluation_robustness.py`: Script for calculating the robustness of the generated answers by a model. Requires specific JSON structure (see below) from `05.2_evalutation_generation.py` and results from `06_evaluation_correctness.py`
- `Finetune_Llama_Lora.ipynb`: Jupyter Notebook from `useftn.com` to finetune the LLaMA2 model with LoRA Adapter
- `question.py`: Question Class used in `06_evaluation_`-files to read in json data.
- `requirements.txt`: Python libraries needed to run the training scripts (`04`)

# Helper Scripts
- `__init__.py`: Empty file to make the folder a python module
- `heatmap.py`: Datastructure to represent a heatmap. Used in `06_evaluation_`-files to generate heatmaps. Also contains function to generate heatmaps.
- `model_helper.py`: Helper function for sorting model names by their epoch number and getting the model name from a file name
- `plot_helper.py`: Contains common formatting variables for plotting
- `question.py`: Contains Datastructure for the used json files and function to read and save these

# JSON Structures

## For Generating Answers
Required for scripts `04_predict_llama2_base.py`, `04_predict_llama2_4bit.py`, `04_predict_llama2.py`, `04_predict_llama2_lora.py` and `06_evaluation_robustness_01.py`.
Examples can be found in `/data`.
```json
[
    {
        "question": "Example Question", <-- this is the actual question / questions from the sources
        "transformed": "Example Question", <-- this is the question that was used for generating answers. It is "question" translated to english and slightly modified.
        "true_answer": "Example Answer", <-- this is the true answer that is expected
        "num_answers": 1, <-- number of answers that are in "true_answer" contained
        "source": "Example Source", <-- source of the question
        "context": "Example Context", <-- context of the question
    }
]
```

For generation all `04_`-Scripts need the following json files:
- `single_questions.json`
- `multi_questions.json`
- `transfer_questions.json`
For `06_evaluation_robustness_01.py`  single json file is needed that contains all questions with spelling mistakes.
Additionally each question needs to have a `type` attributed that is either `single`, `multi` or `transfer`.

## For Evaluating generated Answers
Required for script `05_evaluation_generation.py`.
Generated by `04_predict_llama2.py`, `04_predict_llama2_paula.py` or `04_predict_llama2_base.py`.
Examples can be found in `/output` named `generated_*.json`

```json
[
    {
        "question": "Example Question", <-- this is the actual question / questions from the sources
        "transformed": "Example Question", <-- this is the question that was used for generating answers. It is "question" translated to english and slightly modified.
        "generated": "Example Answer", <-- this is the generated answer
        "true_answer": "Example Answer", <-- this is the true answer that is expected
        "num_answers": 1, <-- number of answers that are in "true_answer" contained
        "type": "single", <-- type of question, either "single", "multi" or "transfer"
        "source": "Example Source", <-- source of the question
        "context": "Example Context", <-- context of the question
        "true_input": "Example Input", <-- actual input that was used for generating the answer
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
        "transformed": "Example Question", <-- this is the question that was used for generating answers. It is "question" translated to english and slightly modified.
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
        "transformed": "Example Question", <-- this is the question that was used for generating answers. It is "question" translated to english and slightly modified.
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
Examples can be found under `/evaluation/criterias/explainability` named `[model]_[not_]explained.json`

```json
[
    {
        "question": "Example Question", <-- this is the actual question / questions from the sources
        "transformed": "Example Question", <-- this is the question that was used for generating answers. It is "question" translated to english and slightly modified.
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
Examples can be found under `/evaluation/criterias/question_understanding` named `[model]_[not_]understood.json`

```json
[
    {
        "question": "Example Question", <-- this is the actual question / questions from the sources
        "transformed": "Example Question", <-- this is the question that was used for generating answers. It is "question" translated to english and slightly modified.
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

# Generated Plots
## Correctness
Generated by `06_evaluation_correctness.py`.
Saved to `/evaluation/criterias/correctness`.
- `answers_[type].png`: contains bar plots depicting number of questions answered correctly, wrongly or not at all
- `makro_[type].png`: contains bar plots depicting macro f1 scores achieved by the models
- `makrof1_[model]_heat.png`: Heatmap of macrof1 scores for type and source per model
- `makrof1_[source]_heat.png`: Heatmap of macrof1 scores for type and model per source
- `makrof1_[type]_heat.png`: Heatmap of macrof1 scores for source and model per type
- `makrof1_total_model_heat.png`: Heatmap of average macrof1 scores for type and source
- `makrof1_total_source_heat.png`: Heatmap of average macrof1 scores for model and source
- `makrof1_total_type_heat.png`: Heatmap of average macrof1 scores for model and type

## Explainability
Generated by `06_evaluation_explainability_02.py`.
Saved to `/evaluation/criterias/explainability`.
- `explained.png`: contains bar plots depicting number of answers that contain or do not contain an explanation
- `explained_[type].png`: contains bar plots depicting number of answers that contain or do not contain an explanation per question type
- `explained_[source].png`: contains bar plots depicting number of answers that contain or do not contain an explanation per source
- `explainability_[type].png`: contains heatmap of explainability for source and model per question type
- `explainability_[source].png`: contains heatmap of explainability for type and model per source
- `explainability_[model].png`: contains heatmap of explainability for type and source per model
- `explainability_total_model.png`: contains heatmap of average explainability for type and source
- `explainability_total_source.png`: contains heatmap of average explainability for source and model
- `explainability_total_type.png`: contains heatmap of average explainability for type and model

## Loss
Generated by `06_evaluation_loss.py`.
Saved to `/evaluation/criterias/loss`.
- `loss.png`: Line plot for training loss of all models
- `validation_loss.png`: Line plot for validation loss of all models

## Question Understanding
Generated by `06_evaluation_question_understanding_02.py`.
Saved to `/evaluation/criterias/question_understanding`.
- `understood.png`: contains bar plots depicting number of questions that are or are not understood by the models
- `understood_[type].png`: contains bar plots depicting number of questions that are or are not understood by the models per question type
- `understood_[source].png`: contains bar plots depicting number of questions that are or are not understood by the models per source
- `question_understanding_[type].png`: contains heatmap of question understanding for source and model per question type
- `question_understanding_[source].png`: contains heatmap of question understanding for type and model per source
- `question_understanding_[model].png`: contains heatmap of question understanding for type and source per model
- `question_understanding_total_model.png`: contains heatmap of average question understanding for type and source
- `question_understanding_total_source.png`: contains heatmap of average question understanding for source and model
- `question_understanding_total_type.png`: contains heatmap of average question understanding for type and model

## Ranking
Generated by `06_evaluation_ranking.py`.
Saved to `/evaluation/criterias/ranking`.
- `correct.png`: Line plot for number of questions answered correctly per model
- `correct_[type].png`: Line plot for number of questions answered correctly per model and question type
- `correct_[source].png`: Line plot for number of questions answered correctly per model and source
- `macrof1.png`: Line plot for macro f1 scores per model
- `macrof1_[type].png`: Line plot for macro f1 scores per model and question type
- `macrof1_[source].png`: Line plot for macro f1 scores per model and source
- `unanswered.png`: Line plot for number of questions not answered at all per model
- `unanswered_[type].png`: Line plot for number of questions not answered at all per model and question type
- `unanswered_[source].png`: Line plot for number of questions not answered at all per model and source

## Robustness
Generated by `06_evaluation_robustness.py`.
Saved to `/evaluation/criterias/robustness`.
- `answer_total.png`: contains bar plots depicting number of questions answered correctly, wrongly or not at all
- `answers_[type].png`: contains bar plots depicting number of questions answered correctly, wrongly or not at all per type
- `answer_[source].png`: contains bar plots depicting number of questions answered correctly, wrongly or not at all per source
- `makro_total.png`: contains bar plots depicting macro f1 scores achieved by the models
- `makro_comparison.png`: contains bar plots comparing macro f1 scores with correctly spelled questions from correctness evaluation
- `makro_[type].png`: contains bar plots depicting macro f1 scores achieved by the models
- `makro_[type]_comparison.png`: contains bar plots comparing macro f1 scores with correctly spelled questions from correctness evaluation
- `makro_[source].png`: contains bar plots depicting macro f1 scores achieved by the models per source
- `makro_[source]_comparison.png`: contains bar plots comparing macro f1 scores with correctly spelled questions from correctness evaluation per source
