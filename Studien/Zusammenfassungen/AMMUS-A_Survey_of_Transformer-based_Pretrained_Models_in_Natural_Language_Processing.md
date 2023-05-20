# Paper
```bibtex
@ARTICLE{Kalyan2021-yx,
  title    = "{AMMU}: A survey of transformer-based biomedical pretrained
              language models",
  author   = "Kalyan, Katikapalli Subramanyam and Rajasekharan, Ajit and
              Sangeetha, Sivanesan",
  journal  = "Journal of biomedical informatics",
  volume   =  126,
  pages    = "103982",
  year     =  2022,
  doi      = "10.1016/j.jbi.2021.103982",
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
  - Kaplan proved performance can be increased by increasing model size (Scaling Laws)
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
General
- GPT1, BERT, BART
Social Media-based
- limited performance
- normally only effective in continual pretraining
- HateBERT, BERT-SentiX
Language-based
- monolingual/multilingual
- e.g. mBert for multilingual
- multilingual cannot represent all languages equally
- monolingual: BanglaBERT, IndoBERT, AraBERT
- multilingual: mT5, mBERT, mBART
Domain-Specific
- domains: finance, legal, news, programming, dialogue, networking, academic, biomedical
- usually continual pretraining
- BioBERT, CoText, BluBERT
- converges faster
- domain-specific vocabulary good

## 4.2 Architecture
Encoder-based
- embedding layer + stack of transformer encoder layers
- BERT-base = 12 encoder layers
- BERT-large = 24 encoder layers
- RoBERTa, XLNet, BERT
Decoder-based
- embedding layer + stack of transformer decoder layers
- decoder layer = masked multi-head attention + feed-foward network layers
- multi-head attention module wit encoder-decoder cross-attention removed
- GPT1, GPT2, GPT3
Encoder-Decoder-based
- better for sequence-to-sequence tasks (translation, summarization)
- MASS, BART, T5, PALM

## 4.3 SSL
Generative SSL
- prediction of tokens based on current Tokens (CLM)
- prediction of masked tokens based on context (MLM)
- reconstruction of corrupted text (DAE)
- GPT1, GPT2, RoBERTa, XLM, BART, MASS
Contrastive SSL
- used in continual pretraining
- improves sentence-level semantics
- learn by comparison
- MirrorBERT, CERT, SImCSE
Adversarial SSL
- distinguishing corrupted tokens (replaced, shuffled)
- ELECTRA, XLM-E
Hybrid SSL
- combination of generative and contrastive SSL = BERT
- RoBERTa = generative, contrastive, adversarial SSL
## 4.4 Extensions
Compact T-PTLMs
- model compression techniques toi reduce size
- pruning
  - models often over-parameterized (weights can be removed without impact)
  - reduces storage space and inference time
  - most of attention heads redundant during inference
  - encoder layer dropped during pretraining
  - layer dropping eliminiates training from scratch
- Knowledge Distillation
  - training student models from teacher models
  - student learns generalization from teacher
  - using L2 loss from teacher and student logits
  - using corss-entropy between softmax of logits of student and teacher
  - DistilBert
- Quantization
  - fewer bits to represent weights (generally 32/16 bits)
  - mixed-bit quanitation, knowledge distillation combined
  - Q8BERT
- Parameter Sharing
  - cross-layer parameter sharing
  - factorized embedding parameterization
    - split vocab in two small matricies
    - allows growing hidden vector size without increasing vocab paramteres
  - prevents growth of parameters with increase in depth
  - ALBERT
Character-Based T-PTLMs
- problem sub-word: large vocabulary size and OOV problem
- idea: rare & misspelled words represented as subwords, others as words
- drawback
  - cannot encode fine-grained characterlevel information
  - brittleness to noise (simple typos changes representation)
- dual-channel CNN in every transformer; enables character & sub-word channels
- CharBERT, AlphaBERT
Green T-PTLMs
- vs continual pretraining for specific domains
- expensive, not environmentally friendly
- extending vocab
- extending domain-specific WordPiece embeddings
- only extension module parameters updated, rest freezed
- GreenBioBERT, exBERT
Sentence-based T-PTLMs
- fine-tuning over NLI ans STSb (sentence pair classification tasks)
- SBERT, IS-BERT, Mirror-BERT
Tokenization-Free T-PTLMs
- subword/character tokenization drawbacks
  - fixed vocabulary
  - matrix (each token gets vector and softmax matrix) = more model parameters
  - adaptation to other models inefficient
  - explicit tokenizers, split at space / punctation => not usable for datasets with no space deliminiator
- convolutional layer on character sequence
- higher depth of encoder
- CANINE, ByT5
Large Scale T-PTLMs
- performance increases with model size, training on larger volumes, training more steps
- GPT3, PANGU, GShard
Knowledge Enriched T-PTLMs
- intregrating knowledge from external knowledge sources
- Knowledge Sources: WordNet, WikiData, UMLS
- novel pretraining tasks
- CasualBERT, KnowBERT, SenseBERT
Long-Sequence T-PTLMs
- quadratic time complexity of self-attention modules limits long input sequences
- sparse/linearized self-attention
- sparce: reduces query-key pairs that each query attends to
- linearized: disentangling attention with kernel feature maps
- BigBird, Reformer, Performer
Efficient T-PTLMs
- DeBERTa
- disentangled attention mechanism, enhanced masked decoder
  - represent word with separate vectors for content and position
  - predict masked tokens instead of softmax layer
- ConvBERT
- mixed attention block
  - self-attention and span based dynamic convolution modules
  - span-based model local dependencies, self-attention models global dependencies
# 5 Downstream Adaption Methods
## 5.1 Feature-based
- contextual word vectors
  - are contextual unlike word2vec, GloVe
  - overcome OOV words problem
  - encode more information
- requires training downstream model from scratch
## 5.2 Fine-tuning
- imparts task-specific knowledge
- adapting weights on task-specific loss
- clusters different labels away
- higher layers more subject to changes
- Vanilla Fine-tuning
  - prone to overfit with small datasets
  - based on task-specific loss
- Intermediate Fine-tuning
  - train on intermediate dataset with labels
  - does not guarantee better performance
  - domain adaptive
    - train on domain dataset with large number of labeled instances
  - Task adaptive
    - train on task dataset with labeled instances
    - do not need to be from same domain
- Multi-task fine-tuning
  - auxiliary tasks
  - training from multiple datasources => less labeled data required
  - avoids overfitting to specific target task
  - vanilla
    - fine-tune on multiple dataset simultaneously
    - taskspecific layer for embedding and transformer
    - not guaranteed to improve performance
  - Iterative
    - select best dataset for fine-tuning
  - Hybrid
    - fine-tune on multiple related datasets
    - then finetune on target dataset with msall learning rate
- Parameter Efficient Fine-tuning
  - adapters
    - two feed-forward layers
    - non-linear layer between
    - projects into smaller layer, then back to original size
    - added to each sublayer
    - only adapter parameters updated during fine-tuning
    - improves in intermediate fine-tuning
  - pruning-based fine-tuning
    - remove unused parameters

## 5.3 Prompt-based Tuning
- discrepancy between finetuning and pretraining task degrades performance
- prompt have close or pre-fix shape
- generated manually or automatically
  - prompt mining, prompt generation, prompt paraphrasing, gradient-based search

# 6 Evaluation
- knowledge types: syntactic, semantic, factual, common-sense
- effectiveness evaluation: instrinsic, extrinsic
  - instrinsic: probes knowledge encoded
  - extrinsic: real-world downstream tasks

## 6.1 Intrinsic Evaluation
- probes: LAMA, XLAMA, X-FACTR, MickeyProbe
- LAMA: factual and common-sense under zero-shot settings
  - corpus of facts (relation triplet, question-answer pair)
  - converted to fill-in-the-blank
  - evaluated based on prediction of blank tokens
  - drawbacks
    - limites prediction over model vocabulary
    - probes only english languags
    - restricts to single token entities
    - easy to guess examples
- XLAMA: multiple languages, multi-token entities
- X-FACTR: multiple languages, multi-token
- MickeyProbe: common-sense probe, sentence-level ranking

## 6.2 Extrinsic Evaluation
- assess performance of downstream tasks
- evaluating generalization ability
- consists of: dataset, leaderboard, single metric
- datasets represent diverse challenging tasks
- GLUE, SuperGLUE: natural language understanding ability
  - GLUE: 9 tasks, single sentence & sentence pairs
  - SuperGLUE: more challening tasks (QA, Word sense disambiguation, coreference resolution)
- GENIE; GEM, GLGE: natural language generation ability
  - GENIE: 4 tasks (summarization, question generation, dialogue generation, translation)
  - GEM: 8 tasks (summarization, question generation, dialogue generation, translation, commonsense reasoning)
  - GLGE: 4 tasks (summarization, question generation, dialogue generation, translation)
- XGLUE, XTREME: cross-lingual models
- TweetEval, UMSAB: social media based
  - tweet classification

# 7 Useful Libraries
- Transformers, Fairseq: model training and evaluation
- SimpleTransformers, HappyTransformers, AdaptNLP: easier training and evaluation
- FastSeq, DeepSpeed, FastT5, OnnxT5, LightSeq: increase model speed
- Ecco, BertViz, exBERT: visual analysis
- Transformer-interpret, Captum: explain model decision

# 8 Discussion and Future Directions
## 8.1 Better Pretraining Methods
- Knowledge inherited Pretraining
  - SSL and Knowledge Distillation
## 8.2 Sample Efficient Pretraining Tasks
- MLM is less sample efficient
- RTD, RTS, STD early attempts for sample-efficient pretraining tasks
## 8.3 Efficient Models
- better perfromance even though with less data
## 8.4 Better Position Encoding Mechanisms
- absolute position embeddings suffer from generalization issues
- relative position embeddings robust to sequence length, difficult to implement, yield less performance
## 8.5 Improving existing T-PMTLs
- e.g. by sentence-level semantics
## 8.6 Beyond Vanilla Fine-tuning
- vanilla drawback: requires maintaining separate copy for each task
- Adapters, Pruning-based tuning: parameter efficient
## 8.7 Benchmarks
- not sufficient to cover al scenarios
  - progress in compact pretrained models
  - robustness
  - specific to social media / other domains
## 8.8 Compact Models
- pruning, quantization, knowledge distillation, paraemter sharing,  factorization
## 8.9 Robustness to Noise
- brittle to noise due to sub-word embeddings
- character embeddings, hybrid, tokenization-free
## 8.10 Novel Adaptation Methods
- continual pretraining: lack of domain-specific vocabulary
- vocabulary expansion, ad apt and distill
## 8.11 Privacy Issues
- data leakage if dataset is private
- possible to retrieve sensitive data
## 8.12 Mitigating Bias
- prone to learn and amplify bias
- data augmentation-based approach, dynamically identify bias-sensitive tokens
## 8.13 Mitigating Fine-Tuning Instabilities
- catastrophic forgetting, small dataset sizes
- optimization difficulties (vanishing gradients), generalization issues
- intermediate fine-tuning, mix-out, smaller learning rates, supervised contrastive loss