# Paper
https://proceedings.neurips.cc/paper_files/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf

```bibtex
@inproceedings{NEURIPS2020_1457c0d6,
 author = {Brown, Tom and Mann, Benjamin and Ryder, Nick and Subbiah, Melanie and Kaplan, Jared D and Dhariwal, Prafulla and Neelakantan, Arvind and Shyam, Pranav and Sastry, Girish and Askell, Amanda and Agarwal, Sandhini and Herbert-Voss, Ariel and Krueger, Gretchen and Henighan, Tom and Child, Rewon and Ramesh, Aditya and Ziegler, Daniel and Wu, Jeffrey and Winter, Clemens and Hesse, Chris and Chen, Mark and Sigler, Eric and Litwin, Mateusz and Gray, Scott and Chess, Benjamin and Clark, Jack and Berner, Christopher and McCandlish, Sam and Radford, Alec and Sutskever, Ilya and Amodei, Dario},
 booktitle = {Advances in Neural Information Processing Systems},
 editor = {H. Larochelle and M. Ranzato and R. Hadsell and M.F. Balcan and H. Lin},
 pages = {1877--1901},
 publisher = {Curran Associates, Inc.},
 title = {Language Models are Few-Shot Learners},
 url = {https://proceedings.neurips.cc/paper_files/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf},
 volume = {33},
 year = {2020}
}
```

# Abstract
- scaling up model replaces fine-tuning
- improves capability in variety of nlp tasks

# 1 Introduction
- nlp shifted from task-specific architecture to task-agnostic pre-training and architectures
- last step of finetuning to desired task may not be necessary
  - previous work still far from even simple supervised baselines

- observed log-linear trends on performance with one order of magnitude of scaling
- extrapolate and test on two orders of magnitude scaling

- zero-shot = no examples, only natural language description of task
- one-shot/few-shot = examples provided in context
- few-shot performance much higher than zero-shot
    - slow outer-loop learning
    - fast in-context learning

- can surpase state-of-the-art with few-shot learning

- gap between zero/one/few-shot grows with model capacity

# 2 Approach
- scaling up model size, dataset size, diversity, length of training
- Fine-Tuning
  - update weights based on supervised labels
  - advantage: better performance on many benchmarks
  - disadvantage: new large dataset for each task, poor generalization
- Few-Shot
  - giving K examples with completion, requires last to be completed
  - typically k 10 to 100
  - major reduction in task-specific data
- One-Shot
  - k = 1
- Zero-Shot
  - no examples, but natual language description of task

## 2.1 Model and Architectures
- same as gpt2
- alternating dense and locally banded sparse attention patterns
- 8 sizes 125m to 175b parameters

## 2.2 Training Dataset
- download and filter CommonCrawl
- fuzzy deduplication at document level
- added known high-quality reference corpora (WebText dataset, books corpora, wikipedia)

## 2.3 Training Process
- larger models use larger batch size, require smaller learning rates
- used gradient snoise scaling to guide batch size choice

## 2.4 Evaluation
- Few-Shot = draw random K examples from training dataset
- natural language prompting
- for free-form completion, beam search with beam = 4 and length penalty = 0.6

# 3 Results
## 3.1 Language Modeling, Cloze and Completion Tasks
- calculated zero-shot perplexity on Penn Tree Bank dataset
- omited wikipedia related task (in dataset already present)
- LAMBADA dataset for predicting last word in a paragraph
  - gain of 8% over previous state-of-the-art
  - few-shot 18% for fill in the blanks
  - one-shot not good (requires more examples to recopgnize pattern)
- HellaSwag (find best ending for story), better than fine-tuned, but worse than ALUM
- StoryCloze (selecting correct ending sentence), better than zero-shot, lower than BERT fine-tuned

## 3.2 Question Answering
- TriviaQA: zero-shot outperforms finetuned T5, oneshot improves by 3.7%, few-shot by 3.2%
- ARC (common sense reasoning dataset) approaches RoBERTa baseline on Challenge Set, outperforms on Easy set
- CoQA (Reading comprehension), within 3 points of human baseline
- DROP (discrete reasoning andnumeracy), few-hot outperforms fine-tuned BERT, well below human performance

## 3.3 Translation
- 93% english in dataset
- zero-shot underperforms recent unsupervised nmt result
- one-shot improves by 7 BLEU, few-shot by 4
- translating into english overperforms, from english underperforms
  - could be because byte-level bpe encoding from gpt2 almost entirely on english dataset

## 3.4 SuperGLUE
- benchmark with standardized collection of datasets
- score improves with model size and number of examples
- a lot of tests show almost SOTA or better than SOTA performance

# 4 Measuring and Preventing Memorization Of Benchmarks
- model does not overfit against validation sets
- clean versions of benchmarks (<13-gram overlapp) compared to original score
  - most cases performance changes are negligible

# 5 Limitations
- repeats semantically
- loses coherence over long sequences
- contradicts themselves
- no bidirectional architecture, worse  performance for such tasks
  - fill in the blank
  - comparing two pieces
  - long passage input with very short answer

- objective weighs tokens equally => no preference for important tokens
- not grounded on other domains (video, physical interaction) => lack of context about the world => will hit limitations
- size is challenging to deploy => task-specific distillation

# 6 Related Work
- scale effect on language model performance
- approach for scaling
- decrease of computational cost
- task instructions in natural language
- multi-task, multi-stage
- metalearning
- algorithmic innovation (denoising-based bidirectionality, prefixLM, encoder-decoder architectures, random permutations during trainine, architecturs for sampling efficency, data and training improvements, embedding parameters efficiency)

# 7 Conclusion


# Broader Impacts
- misuse of language models
  - social harmful activities agumented by text generation (spam, phishing, abuse)
  - threat actor analysis (no significant usage of gpt2 sofar)
  - external incentive structures

- fairness, bias, and representation
  - gender bias
  - race bias
  - religion bias
  - future bias and fairness challeng

- energy isage
  - thousands of petaflop/s-days of compute
  - suprisingly efficient once trained
    - 100 pages of content = 0.4kW-hr
  - model distillation brings cost down

- News Generation
  -  86% detection for bad articles
  -  largest model 52% detection
  -  automatic text detection like GROVER and GLTR