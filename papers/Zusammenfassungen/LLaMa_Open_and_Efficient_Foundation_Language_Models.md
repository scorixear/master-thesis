# Paper
only arxiv publish
```bibtex
@misc{touvron2023llama,
      title={LLaMA: Open and Efficient Foundation Language Models}, 
      author={Hugo Touvron and Thibaut Lavril and Gautier Izacard and Xavier Martinet and Marie-Anne Lachaux and Timothée Lacroix and Baptiste Rozière and Naman Goyal and Eric Hambro and Faisal Azhar and Aurelien Rodriguez and Armand Joulin and Edouard Grave and Guillaume Lample},
      year={2023},
      eprint={2302.13971},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

# Abstract
- LLaMa = collection of foundation language models (7B - 65B Parameters)
- possible to train with publicly available datasets only

# 1 Introduction
- LLM perform tasks from textual instructions or few examples
- best performance achieved by smaller models trained on more data
- most important is cheaper inference at the cost of longer training
  - training 7B model past 1T tokens continues to improve
- publicly available data makes model open source compatible

# 2 Approach
- training follows common methods
- inspired by chinchilla scaling laws

## 2.1 Pre-training Data
- common crawl 67%
  - 2017 - 2020
  - deduplicated at line level
  - non-english removed (fastText linear classifier)
  - low-quality removed (n-gram language model)
  - discarded pages not used as references in wikipedia
- C4 15%
  - diverse pre-processed CommonCrawl
  - deduplication, language identification
  - quality filtering (heuristics: presence of punctuation, number of word and sentences)
- Github 4.5%
  - distributed under Apache, BSD, MIT Licenses
  - filtered (line length, alphanumeric character proportions)
  - removed boilerplate (headers, regular expressions)
  - deduplicated at file level (exact matches)
- Wikipedia 4.5%
  - June - August 2022
  - 20 Languages
  - removed hyperlinks, comments, formatting boilerplate
- Gutenberg and Books3 4.5%
  - deduplication at book level (>90% content overlap)
- ArXiv 2.5%
  - removed everything before first section, bibliography, comments, inline-expanded definitions, macros
- Stack Exchange 2%
  - removed html tags
  - sorted answers by score

Tokenizer
- byte-pair encoding(TODO: link)
  - Sentence-piece implementation
- fallback to bytes for unknown UTF-8
- 1.4T Tokens (mostly only used once during training)
- wikipedia and books 2 epochs

## 2.2 Architecture
- transformer architecture
- pre-normalization [GPT3]
  - normalize input of transformer sublayer instead of output
  - improves training stability
- SwiGLU activation function [PaLM]
  - replaces ReLU 
  - improves performance
- Rotary Embeddings [GPTNeo]
  - rotary positional embeddings instead of absolute at each layer

## 2.3 Optimizer
- AdamW $\beta_1=0.9,\beta_2=0.95$
- cosine learning rate schedule (final learning rate 10%)
- weight decay 0.1
- gradient clipping 1.0
- 2000 warmup steps

## 2.4 Efficient implementation
- casual multi-head attention
  - xformers library
  - not storing attention weight
  - not computing key/query scores
  - that are masked
- reduce recomputation of activations
  - using checkpoints
- gradient checkpointing
  - reduce memory usage
  - increase training speed
  - save outputs of linear layers
- 380 tokens / sec /GPU
- 2048 GPUs, 80GB RAM
- tooke 21 days

# 3 Main Results
- few shot 1 - 64 examples
- compare to gpt-3, gopehr, chinchilla, OPT, GPT-J, GPT-Neo
- free-form generation, multiple choice tasks
  - multiple choice = choose most appropriate completion

## 3.1 Common Sense Resoning
- benchmarks: BoolQ, PIQA, SIQA, HellaSwag, WinoGrande, ARC easy and challenge, OpenBookQA
- evaluated in zero-shot setting
- LLaMa-65B outperforms Chinchilla-70B except on BoolQ
- LLaMa-65B outperforms PaLM-540B except on Bool! and WinoGrande
- LLaMa-13B outperforms GPT-3 on most benchmarks

## 3.2 Closed-book Question Answering
- benchmarks: Natual Questions, TriviaQA
- LLaMa-65B achieves SOTA (zero-shot and few-shot)
- LLaMa-13B competitive with GPT-3 and Chinchilla (single V100 GPU during inference)

## 3.3 Reading Comprehension
- benchmark: RACE
- LLaMa-65B competitive with PaLM-540B
- LLaMa-13B outperforms GPT-3

## 3.4 Mathematical Reasoning
- benchmark: MATH, GSM8k
- LLaMa-65B outperforms Minerva-62B on GSMK8k

## 3.5 Code generation
- benchmarks: HumanEval, MBPP
- LLaMa-65 outperforms PaLM-62B
- LLaMa-13B outperforms LaMDA-137B

## 3.6 Massive Multitask Language Understanding
- = MMLU benchmark
- 5-shot setting
- LLaMa-65B behind Chinchilla-70B, PaLM-540B
  - limited amount of books and academic papers

## 3.7 Evolution of performance during training
- most benchmarks improve steadily (correlates with training perplexity)
- except in SIQA and WinoGrande

# 4 Instruction Finetuning
- briefly finetuning on instructions leads to rapid improvements in MMLU
- LLaMa-I outperforms OPT-IML, Flan-PaLM, but far from SOTA (GPT code-davinci-002)

# Bias, Toxicity and Misinformation

## 5.1 RealToxicityPrompts
- insults, hate speech, threats
- = 100k prompts
- evaluated by request to PerspectiveAPI
- 0 - 1 = non-toxic - toxic
- toxicity increases with size of model
- respectful prompts have leading prompt text

## 5.2 CrowS-Pairs
- for bias
- 9 categories: gender, religion, race/color, sexual orientation, age, nationality, disability, physical appearance, socioeconomic status
- measure preference against stereotype and anti-stereotype
- zero-shot setting
- particulary biased in religion, age, gender
- expect to come from CommonCrawl

## 5.3 WinoGender
- sentence has three mentions: occupation, participant, pronoun
- pronoun = co-reference to either occupation or participant
- model determines co-reference relation
- clearly shows societal biases

## 5.4 TruthfulQA
- designed to be adversarial
- 38 categories
- uncovers truth about real world, not in context of a specific setting
- LLaMa outperforms GPT-3
- likely to hallucinate incorrect answers

# 6 Carbon Footprint
- costs 2,638 MWh = 1,015t CO2

# 7 Related Work
# Acknowledgements
