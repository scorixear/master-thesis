# Paper
```bibtex
@ARTICLE{Kalyan2021-yx,
  title    = "{AMMU}: A survey of transformer-based biomedical pretrained
              language models",
  author   = "Kalyan, Katikapalli Subramanyam and Rajasekharan, Ajit and
              Sangeetha, Sivanesan",
  journal  = "J Biomed Inform",
  volume   =  126,
  pages    = "103982",
  month    =  dec,
  year     =  2021,
  address  = "United States",
  language = "en"
}
```

# Abstract

# 1 Introduction
- Transformer-based pretrained language models = T-PTLMs
- ability to learn universal language representations
  - from large volumes of unlabeled text
  - transfer knowledge to downstream tasks
- better gpus & word-embeddings increased use of deep learning
- main drawback: requires training from scratch
- CNN & RNN drawbacks: process words sequentially
  - locality bias
  - no parallel computer
  - -> transformer
- self-attention solves parallelization, all tokens attend to all tokens in input
- only requires large unlabeled text, labeled data very expensive
- T-PTLMs combine transformers and self-supervised
  - GPT (decoder), BERT (encoder) first models
  - Kaplan proved performance can be increased by increasing model size (TODO:)
  - more models, bigger, for other domains

- can be adapted to downstream tasks by fine-tuning & prompt-tuning on target dataset
- contents of paper
  - self-supervised learning overview
  - core concepts related to T-PTLMs
  - new taxonomy to categorize T-PTLMs
  - new taxonomy to categorize downstream adaptation methods
  - benchmark overview
  - library overview
  - future resarch directions

# 2 Self-supervised learning
## 2.1 Why Self-Superivsed Learning
- supervised learning = good performance on specific task
  - dependence on human labaled instances (expensive, time-consuming)
  - lack of generalization ability
  - many domains do not have labeled data
  - inability to learn from unlabeled data

## 2.2 What is Self-Supervised Learning
- labels automatically generated based on data attributes
- pretraining can invollve more than one pretraining task
  - RoBERTa: masked language modelling
  - BERT: masked language modelling & next sentence prediction
- model learns general language representation
  - ecodes syntax and semantic
- similarities to unsupervised learning
  - does not require human labeled instances
  - but requires supervision
  - in unsupervised learning target is to identify hidden patterns
  - in ssl target is to learn meaningful representations
- similarities to supervised learning
  - learning paradigma requires supervision
  - but generates labels automatically
  - goal of supervised learning is to provide task-specific knowledge
  - goal of ssl is to provide universal knowledge

- learn universal language representations (good background for downstream tasks)
- better generalization ability

## 2.3 Types of Self-Supervised Learning
- generative
  - learn by decoding encoded input
  - autoregeressive, autoencoding, hybrid language models
  - autoregressive: predict next token based on previous tokens (GPT)
  - autoencoding: predict masked tokens based on unmasked tokens (BERT)
  - hybrid: combine both (XLNet)
- contrastive
  - learn by comparing
  - next sentence prediciton, sentence order prediction
  - next sentence prediction: predict if sentences are consecutive (BERT)
  - sentence order prediction: predict if sentences are in correct order (RoBERTa)
- adversarial
  - learn by identifying tokens that are replaced, shuffled, randomly substituted
  - replaced token detection, shuffled tokendetection, random token detection

# 3 T-PTLM Core Concepts
## 3.1 Pretraining
- in CNN (Computer Vision) on large, labeled datasets
- benefits of pretrainig
  - model learns universal language representations
  - can be adapted to downstream tasks
  - perform better with smaller datasets
  - avoids overfitting on small datasets

### 3.1.1 Pretraining Steps
- Prepare pretraining corpus
  - obtain and clean
  - better to have multiple sources for further performance boost
  - deduplicated corpus requires fewer training steps
- Generate vocabulary
  - use of tokenizers (WordPiece, Byte Pair Encoding, Byte Level BPE, SentencePiece)
  - consists of: unique characters, commonly used subwords, words
  - for each T-PTLM different tokenizers, different vocabularies
  - 30k - 250k size
- Design the pretraining task 
  - be challenging enough to allow the model to learn semantics at word, phrase, sentence, or document level
  - provide more training signal so that the model learns more language informatin with less pretraining corpus
  - close to downstream tasks
- Choose the pretraining method
  - continual pretraining, adapt and distill, pretrin on domain-specific data, simultaneous pretraining
- Choose the pretraining dynamics
  - dynamic masking, large batch sizes, more pretrainign steps, long input sequences
  - enhances performance
  - linearly increase larning rate in early pretrainig steps

### 3.1.2 Pretraining Corpus
- general domain
  - less noisy
  - written formally by professionals
- social media
  - mostly noisy
  - written colloquially by the general public
- domain specific
  - contain domain-specific words
- choose corpus based on downstream task
- performance increases with larger training sets
  - C4 Data (750GB)
  - CC-100 (2.5TB)

## 3.2 Types of Pretraining Methods
### 3.2.1 Pretraining from Scratch
- model consist of embedding layer, transformer encoder, transformer decoder layers
- randomly initialized
- learned by minimizing losses (one or more pretraining tasks)
  - BERT: from scratch, MLM, NSP tasks
- computationally expensive

### 3.2.2 Continual Pretraining
- initializing from existing pretrained models
- further pretrain on target domain, not learned from scratch
- commonly used for specific domains
- advantages
  - avoids pretraining from scratch
  - less expensive
  - less training required
- disadvantages
  - lack of target domain-specific vocabulary
  - words split in subwords -> hinders model learning, degrades performance
  - solution: target domain vocabulary
- embedding layer randomly inizialized, other parameters initialized from pretrained model
  - performance slightly less but on par with PTS
  - adapt & distill: vocabulary expansion, knowledge distillation
  - not necessary to use same pretraining tasks

### 3.2.3 Simultaneous Pretraining
- PTS and CPT require large unlabeled corpus
- domain specific corpus is small, only using this overfits model
- SPT uses both corpi
- upsampling domain-specific text

### 3.2.4 Task Adaptive Pretraining
- allows models to learn fine-grained task-specific knowledge & domain-specific knowledge
- train on task-specific unlabelled text
- further improves performance after PTS or CPT

### 3.2.5 KNowledge Inherited Pretraining
- humans learn not only from self-learning but also frmo other knowledgeable people
- KIPT: includes knowledge distillation
- vs KD:
  - in KD student model compact in size to teacher model
  - in KIPT studen model larger in size
  - in KD student model solely learns from teacher model
  - in KIPT student model learns from teacher model and unlabeled data
- learns more, converges faster, outperforms other models

## 3.3 Pretraining Tasks
- tasks are self-supervised: make use of pseudo-labels
- should provid more training signals
- should be similar to downstream task

Casual Language Modeling
- predict next word based on context
Masked Language Modeling
- clm do not leverage both contexts
- mlm leverages both contexts
- masked token vectors into softmax layer
Replaced Token Detection
- mlm provides less training signals (15% of tokens learned)
- mlm masks with special mask token
- rtd masks with output tokens
- rtd is classification task = is token replaced
- separate generator to corrupt input
Shuffled Token Detection
- identify shuffled tokens
- avoids discrepancy between pretraining and fine-tuning
Random Token Substitution
- identify randomly substituted tokens
- does not require additional generator
Swapped Language moideling
- corrupt data with random tokens from vocabulary
Translation Language Modeling
- use parallel data in cross-lingual training
- input pair of sentences (translation)
- tokens randomly masked
Alternate language Modeling
- cross-lingual training
- randpmly substitution of phrases in x with y
- outperforms xlm (tlm)
Sentence Boundary Objective
- predict masked tokens based on span boundary tokens and position embeddings
- mask only contiguous spans
Next Sentence Prediction
- identify consecutive sentences
- useufll for question answering, nli, sts
Sentence Order Prediction
- identify if sentences are swapped
Sequence-to-Sequence LM
- context includes masked input sequence
- and left side words in predicted target sequence
Denoising Auto Encoder
- reconstruct text from corrupted text
- at different levels corrupted (token, phrase, sentence, document)

## 3.4 Embeddings
- input = matrix of numbers, perform matrix operations
- input text mapped to dense, low-dimensional vectors = embeddings
- characters/subwords preferred over word-embeddings
  - small vocabulary size (determines also size of language model)
  - can represent any word, overcomes OOV problem
  - can encode fine-grained information
- additional information: language, position
- main embeddings, auxiliary embeddings (additional information)

### 3.4.1 Main Embeddings
- input mostly sequence of words / medical codes
Text Embeddings
- combination of character, sub-word embeddings
Character Embeddings
- each character to dense low-dimensional vector
- letters, symbols, numbers, punctuation
- randomly initialized
- learned during model pretraining
Sub-Word Embeddings
- special tokenizers for generating vocabulary
- starting with base vocabulary (characters)
- iteratively augment with symbol pairs based on frequeny until max size is reached
- bpe characters represented as byets
- Unigram starts with word-vocab, cuts word iteratively
- WordPiece & BPE assume Space as word separator
  - SentencePiece treats space as character
- too small vocabulary = longer input sequences, hinders learning, increases pretraining
- too large vocabulary = increases size of model
- initialized with random embedding, learned during pretraining
Hybrid Embeddings
Code Embeddings
- medical codes

### 3.4.2 Auxiliary Embeddings
Position Embeddings
- traditionally (CNN, RNN) not used, because implicitly learn order of tokens
- can be absolute or relative
- learned along with other parameters
- or predetermined
Segment Embeddings
- sentence pair tasks
- distinguish between sentences
- same for all tokens in a sentence
Language Embeddings
- not used in XLM-R to better deal with code switching
Entity Type Embeddings
- additional information like paper, published venue, author affiliation, research domain, authors
Age and Gender Embeddings
- medical pretrained models
- eg sequence of patient visist, additional information such as age and gener
Semantic Group Embeddings

# 4 Taxonomy
## 4.1 Pretraining Corpus-based
