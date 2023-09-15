# Paper
https://www.semanticscholar.org/paper/Improving-Language-Understanding-by-Generative-Radford-Narasimhan/cd18800a0fe0b668a1cc19f2ec95b5003d0a5035
```bibtex
@inproceedings{Radford2018ImprovingLU,
  title={Improving Language Understanding by Generative Pre-Training},
  author={Alec Radford and Karthik Narasimhan},
  year={2018}
}
```
# Abstract
- natural language understanding are tasks like textual entailment, question answering, semantic similarity, and document classification
- unlabeld text corpora are abundant, but labeled data is scarce
- generative pre-training and discriminative fine-tuning on each specific task
- task-aware input transformations during fine-tuning
- absolute improvements in commonsense reasoning, question answering and textual entailment

# 1. Introduction
- leveraging more than world-level information from unlabeld text is challenging
  - is unclear what type of optimization objectives are most effective at learning
  - no consensus on the most effective way to transfer learned representations to target tasks
- use of combinatoin of unsupervised pre-training and supervised fine-tuning
- large corpus of unlabeld text
- several datasets with manually annotated training examples
  - use language modeling objective
  - adapt parameters to target task

- Transformers as model architecture
  - provides more structured memory for handling long-term dependencies
- During transfer, utilize task-specific input adaptations (from traversl-style approaches)
  - process structured text input in single contiguous sequence

- evaluate on four types of tasks: natual language inference, question answering, semantic similarity, text classification
- analyze zero-shot behavours of pre-trained model

# 2. Related Work
Semi-supervised learning
- applications like sequence labeling, text classification
- earliest approaches: unlabeled data to compute word-level or phrase-level statistics; features in supervised model
  - improves performance on variety of tasks
- recent approaches: more than word-level -> phrase-level or sentence-level embeddings

Unsupervised pre-training
- used for image classificaton, regression tasks
- enables better generalization in deep neural networks
- Dai et al. restricts their prediciton ability to short range
- choice for transformers allows longer-range linguistic structure
- normally substantial amount of new parameters
- here require minimal changes to model architecture during transfer

Auxiliary training objectives
- alternative for semi-supervised learning
- tasks such as POS tagging, chunking, named entity recognition
- here used ,but unsupervised pre-training already learns several linguistic aspects

# 3. Framework
- two stages: learning high-capacity language model, fine-tunig to discriminative task

## 3.1 Unsupervised Pre-training
- unsupervised Corpus $\mathcal{U} = \{u_1,\dots,u_n\}$
- maximize likelihood $L_1(\mathcal{U}) = \sum\limits_i \log P(u_i | u_{i-k},\dots,u_{i-1};\Theta)$
  - k = size of context window
  - P = conditional probability
  - $\Theta$ = model parameters

- used multi-laye Transformer decoder
  - applies multi-head self-attention
  - position-wise feedforward layers
- $h_0 = UW_e + W_p$
- $h_l = transformer\_block(h_{l-1}) \forall i \in [1,n]$
- $P(u) = softmax(h_nW_e^T)$
  - $U$ = context vector of tokens
  - $n$ = number of layers
  - $W_e$ = embedding matrix
  - $W_p$ = positional embedding matrix

## 3.2 Supervised Fine-tuning
- labels dataset $\mathcal{C}$
  - $x^1,\dots,x^m$ = inputs
  - $y$ = label
- inputs passed through model, results in final transformer block activiaton $h_l^m$
- fed into added linear output layer, parameters $W_y$ to predict $y$
- $P(y | x^1,\dots,x^m) = softmax(h_l^mW_y)$
- objective to maximize $L_2(\mathcal{C}) = \sum\limits_{(x,y)} \log P(y|x^1,\dots,x^m)$
- auxiliary objective $L_3(\mathcal{C}) = L_2(\mathcal{C}) + \lambda L_1(\mathcal{C})$
  - $\lambda$ = hyperparameter

## 3.3 Task-specific input transformations
- some task require no input transformation (like text classification)
- question answering, textual entailment have strucuted inputs (ordered sentence pairs, triplets of document, question, answer)
- pretrained on contiguous sequences

- previous work proposes learning task specific architecturs on top of transfered representations
  - reintroduces significant amount of task-specific customization
- used traversal-style approach
  - convert structured input to ordered sequence

Textual entailment
- concatenate premise $p$ and hypothesis $h$ with delimiter $

Similarity
- modify input sequence, contains both possible sentence orderings
- process each indepenently, produces two sequence representations
- add element-wise before fed into linear output layer

Question Anwering and Commonsene Reasoning
- context $z$, question $q$, answers $\{a_k\}$
- concatenate $[z;q;$&#36;$;a_k]$
- processed independently, normalized via softmax

# 4. Experiments
## 4.1 Setup
- BooksCorpus dataset (7000 unique unpublished books)
- alternative 1B Word Benchmark

Model specification
- 12-layer decoder-only
- 768 dimensional states, 12 attention heads
- position-wise feed-forwars 3072 dimensional inner states
- Adam optimization
- learning rate 2.5e-4
- lineare warmup over first 2000 steps, annealed to 0 with cosine schedule
- 100 epochs, minibatch with 64 sequences of 512 tokens
- weight initialization: N(0,0.02)
- byte-pair encoding (BPE) vocabulary with 40,000 merges
- attention dropout 0.1
- modified version of L2 with $w = 0.01$
- activiation Function: GELU
- learned positional embeddings
- ftfy library to clean raw text

Fine-tuning details
- add dropout to classifier with $p = 0.1$
- learning rate 6.25e-5
- batch-size 32
- 3 epochs

## 4.2 Supervised fine-tuning
Question anwering and commmonsense reasoning
- requires single and multi-sentence reasoning
- used RACE dataset (English passages and associated questions of high and middle school, contains more reasoning type questions)

# 5. Analysis
Impact of number of layers transferred
- each transformer layer provides benefit up to 9%

Zero-shot behaviors
- hypothesis: underlying generative model learns to perform several tasks here evaluated, improves language modeling capability
- observed performance is stable and steadily increases over training
- suggests generative pretraining supports learning variety of task relevant to functionality

Ablation studies
- performance with auxiliary objective helps
- larger datasets benefit auxiliary objective, smaller dataset do not
- single-layer 2048 LSTM drops average score drop 5.6 (compared to Transformer)
- lack of pre-training hurts performance across all the tasks (14.8% decrease)

# 6. Conclusion
