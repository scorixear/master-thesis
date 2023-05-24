# Paper
 = GPT2 Paper
 ```bibtex
 @article{radford2019language,
  title={Language Models are Unsupervised Multitask Learners},
  author={Radford, Alec and Wu, Jeff and Child, Rewon and Luan, David and Amodei, Dario and Sutskever, Ilya},
  year={2019},
  url={https://d4mucfpksywv.cloudfront.net/better-language-models/language-models.pdf}
}
```

# Abstract
- llm learn tasks without explicit supervision
  - question answering, machine translation, summarization
  - webtext dataset (millions of pages)
- capacity essential for zero-shot task tranfer

# 1 Introduction
- normally combination of high-capacity models and supervised learning
- brittle and sensitive to slight changes in data distribution and task specification
- target: competent generalist without the need of manually created labeled datasets

- dominant approach: collect dataset with correct behaviour, train to imitate, test on independent examples
- suspicion: only trained on single task with single domain
- very difficult to continue scaling the creation of datasets
- best performing system utilize combination of pre-training and supervised fine-tuning
- recent work suggests, task-specific architectures are no longer necessary
- more work showed without supervised training emerges commonsense reasoning and sentiment analysis

- connect both lines, show zero-shot setting without any parameter or architecture modification
- achieved promising, competitive, state of the art results depending on task

# 2 Approach
- core = Language modelling = unsupervised distribution estimation from sets of examples
- tasks usually formulated as estimating conditional distribution of $p(output|input)$
- for multi task, conditional distributon $p(output|input,task)$
- tasks expressed in language, still part of input
- supervised objective is subset ofsequence as the unsupervised objective
- global minimum of supervised is global minimum of unsupervised
- problem: can we optimize unsupervised to convergence
- experiments show unsupervised learning is much slower

- dialog learning (prediction teachers output) might be overly restrictive
- speculate it can do from internet text without any dialog

## 2.1 Training Dataset
- common crawl most text is unitelligible
- hard to filter, therefore created own datset with focus on document quality
- webscrabe from reddit links with at least 3 karma
- heuristic indicator of human interest
- 40GB of text

## 2.2 Input Representation
- word-level outpferorm byte-level lms
- but cannot represent any string
- byte pair encoding is middle ground
- works on unicode code points, not byte sequences
- usage of byte level ersion, to reduce size of base vocab to 256
- prevent merging across character categories (excpetion for spaces)

## 2.3 Model
- transformer based
- layer normalization moved to input of each sub block
- additional layer normalization after final self-attention block
- scale weight of residual layers at initialzation by $\frac{1}{\sqrt{N}}$
- vocabulary expanded to 50,257 tokens
- context size increased to 1024
- batchszie of 512

# 3 Experiments
- smallest model equal to gpt
- 2nd smallest equal to bert
- largest over 1 magnitude larger, called gpt-2

## 3.1 Language MOdeling
- improvement on 7 of 8 datasets
- large improvements on small datasets
- significantly worse in one billion word benchmark

## 3.2 Children's Book Test
- prediction of correct word out of 10 choices
- performance steadily increases with model size

## 3.3 LAMBADA
- predict final word of senteces with > 50 Tokens
- huge improvement, errors are smostly accurate continuations

## 3.4 Winograd Schema Challenge
- measure commonsense reasoning
- ability to resolve ambiguities in text

## 3.5 Reading Comprehension
- answer questions depending on conversation history

## 3.6 Summarization
- TL;DR: after article, to generate 100 tokens

## 3.7 Translation
- first generated sentence as tranlation
- good results despite removing non-englihsh text
- french text was only 10MB

## 3.8 Question Answering
- 5.3 times more correct answers
- model capacity os factor in performance
- still much worse than open domain question answering systems

# 4 Generalization vs Memorization
- image dataset contain non-trivial amount of near-duplicate images
- similar phenomena could behappening with webtext
- calculate bloom filters for overlap
- many dataset ahve large overlap of 5.9% average
- analysis suggest overlap provied small but consisten benefit
- no significantly larger overlaps
- suggest gpt2 still underfitting on webtext


# 5 Related Work
- lm pretraining is helpful when finetuning on difficult tasks suchas question answering systems (TODO:)

# 6 Discussion

