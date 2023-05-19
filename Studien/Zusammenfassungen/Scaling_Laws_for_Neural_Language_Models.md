# Paper
```bibtex
@misc{kaplan2020scaling,
      title={Scaling Laws for Neural Language Models}, 
      author={Jared Kaplan and Sam McCandlish and Tom Henighan and Tom B. Brown and Benjamin Chess and Rewon Child and Scott Gray and Alec Radford and Jeffrey Wu and Dario Amodei},
      year={2020},
      eprint={2001.08361},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
}
```

# 1 Introduction
- empirically investigate dependency of language modeling loss on model architecture, size, computing power used to train them, data available
- focus on transformer architecture
- trends over seven orders of magnitude in scale

## 1.1 Summary
- performance depends strongly on scale, weakly on model shape
  - strongly on number of parameters excluding embedding, size of dataset, amount of compute
  - weakly on architectural hyper parameters (depth vs width)
- smooth power laws
  - if not bottlenecked by other two factors
- universality of overfitting
  - scale predictily if N and D incrase in tandem
  - diminishing returns if either N or D held fixed
  - $N^0.74/D$ -> increase model size x8, increase dataset x5
- Universality of training
  - follow power-laws where parameters are indepentend from model size
- Transfer improves with test performance
  - constant offset of loss between different distributions vs training validation
  - transfer incurs constant penalty, but roughly in line with performance on training set
- Sample Efficiency
  - larger models more sample-efficient, reaching same performance with fewer optimization steps and fewer data points
- Convergence is inefficient
  - with fixed C, but unlimited N and D, best performance achieve when stopping significntly short of convergence
  - $D \approx C^0.27$
- Optimal batch size
  - batch size roughly power of loss only
  - determinable by measuring gradient noise scale
  - e.g. 1-2m tokens for largest model

## 1.2 Summary of Scaling Laws
- test loss predictions

| Law | Parameters | Unit |
| --- | --- | --- |
| $L(N) = (N_c/N)^{\alpha_N}$ | $\alpha_N\sim0.076,N_c\sim8.8\times10^{13}$ | non-embedding parameters |
| $L(D) = (D_c/D)^{\alpha_D}$ | $\alpha_D\sim0.095,D_c\sim5.4\times10^{13}$ | tokens |
| $L(C_{min}) = (C_c^{min}/C_{min})^{\alpha_C^{min}}$ | $\alpha_C^{min}\sim0.050,C_c\sim3.1\times10^8$ | PF-days |
| $\newcommand\ddfrac[2]{\frac{\displaystyle #1}{\displaystyle #2}} B_{crit}(L) = \dfrac{B_*}{L^{1/\alpha_B}}$ | $\alpha_B\sim0.21, B_*\sim2\times10^8$ | tokens | 

- hold for 8 orders of magnitude for $C_{min}$, 6 order for $N$ and 2 for $D$
- depend very weakly on model shape and other transformer hyperparameters
- $\alpha$ specify degee of performance improvement with scale
  - doubling parameters -> $2^{-\alpha_N} = 0.95$ smaller loss
- sizes of $D_C,C_C^{min}, D_C$ depend on vocab size and tokenization, do not have fundamental meaning
- increasing model size uinherits sublinearly increasing dataset size

## 1.3 Notation
- L = cross-entropy loss in nats
- N = number of non-embedding parameters
- $C\approx6NBS$ = total non-embedding training compute, B = Batch Size, S = number of training steps, PF-day = $10^{15}*24*3600=8.64*10^{19}$ floating point operations
- D = dataset size in tokens
- $B_{crit}$ = critical batch size with optimal compromise between time and compute efficiency
- $C_{min}$ = minimum compute required to reach a given loss
- $S_{min}$ = minimum number of steps required to reach a given loss
- $\alpha_X$ = power-law exponents for scaling loss $L(X)\propto1/X^{\alpha_X}$ 

# 2 Background and Methods
- webtext2 dataset
- bytepair encoding
- vocab size = 50257 tokens
- optimize log-likelihood (cross-entropy loss)
- primarily train decoder-only, but also LSTM and Universal Transformers

## 2.1 Paraemter and Compute Scaling of Transformers
- $N \approx 2d_{model}n_{layer}(2d_{attn}+d_{ff})$
- $= 12n_{layer}d_{model}^2$ for $d_{attn}=d_{ff}/4=d_{model}$
- $C_{forward}\approx2N+2n_{layer}n_{ctx}d_{model}$

## 2.2 Training Procedures
- Adam Optimizer with fixed steps
- batch size of 512 sequences of 1024 tokens
- Trained largest Model with Adafactor

## 2.3 Datasets
- WebText = Webscrape of outbound links from Reddit December 2017
- WebText2 includes January - October 2018
- 20.3M documents, 96GB text
- similary samples of BooksCorpus, CommonCrawl, English Wikipedia, Public-available Internet Books

# 3 Empirical Results and Basic Power Laws
- Model size 758 - 1.5billion parameters
- Dataset size 22 million - 23 billion tokens
- Shape
- context length 1024 for most runs
- Batch size $2^{19}$ for most runs

- non-dependent on layers, if embeddings are excluded (>2 layers)

## 3.1 Approximate Transformer Shape and Hyperparameter Independence
- vary $n_{layer},n_{heads}, d_{ff}$ with fixed $N$

## 3.2 Performance with Non-Embedding Parameter Count N
- trained near convergence, no overfitting observed
- suggest, embedding matrix can be made smaller without impacting performance

Comparing to LSTMs and Universal Transformers
- perform well for tokens appearing early in context
- cannotm atch performance for later tokens

Generalization Among Data Distributions
- all trained on same dataset
- generalization depends on in-distribution validation loss
- does not depend on duration of training or proximity to convergence, model depth

## 3.3 Performance with Dataset Size an Compute
- results are not truly optimal, since batch size stays fixed
- sample efficiency improves with model size

# 4 Charting the Infinite Data Limit and Overfitting
- suggest, with how much data a model with given size needs to be trained
- with very small datasets, overfitting happens early
  - reduced to $2\times10^7$ results in 40 parameter updates
- no sign of overfitting after training on 22B tokens
- dataset size may grow sub-linearly in model size to avoid overfitting

# 5 Scaling Laws with Model Size and Training Time
## 5.1 Adjustment to Training at $B_{crit}(L)$
- there is a critical batch size for training
  - increasing B to $B_{crit}$ with very minimal degradation in compute-efficiency
    - minimizes use of compute
  - increasing B beyond $B_{crit}$ leads to diminishing returns
    - minimizes training steps
## 5.2 Results for $L(N, S_{min})$ and Performance with Model Size and Compute

## 5.3 Lower Bound on Early Stopping Step
- step at which early stopping should occur

# 6 Optimal Allocation of the Compute Budget
- use of fixed batch size, that could be better ($B_{crit}$)
- adjustment for this oversight

## 6.1 Optimal Performance and Allocations
- optimal number of steps grows very slowly with compute
- negilgible increase number of serial steps
- mainly increase model size
- simultaneously scale batch size

## 6.2 Prediction from $L(N, S_{min})$
## 6.3 Contradictions and a Conjecture
- no signs of deviation from straight power-law
- but must level off since natural language as non-zero entropy
- scaling law predicts loss below possible given slow growth of training data with compute
- conjecture, this is transformer language model maximal performance
- compute-efficiency will eventually run into overfitting, even if training process never re-uses any data

- $C^* \sim 10^4$ PF-Days
- $N^* \sim 10^{12}$ parameters
- $D^* \sim 10^{12}$ tokens
- $L^* \sim 1.7$ nats/token

# 7 Related Work
# 8 Discussion 
