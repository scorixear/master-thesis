# Paper
arxiv publish
journal publish: https://proceedings.neurips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html
```bibtex
@inproceedings{NIPS2017_3f5ee243,
 author = {Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N and Kaiser, \L ukasz and Polosukhin, Illia},
 booktitle = {Advances in Neural Information Processing Systems},
 editor = {I. Guyon and U. Von Luxburg and S. Bengio and H. Wallach and R. Fergus and S. Vishwanathan and R. Garnett},
 pages = {},
 publisher = {Curran Associates, Inc.},
 title = {Attention is All you Need},
 url = {https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf},
 volume = {30},
 year = {2017}
}
```

# Abstract
- dominant sequence transduction models are based on complex recurrent or convolutional neural networks
- include encoder and decoder connected through attention mechanism
- Transformer, only attention mechanism, no reccurence and convolutions
- BLEU score of 41.8, 3.5 Days Training, 8 GPUs

# 1. Introduction
- recurrent models factor computation along symbol positions of input and output sequences
- generate hidden states $h_t$ as a function of previous hidden states $h_{t-1}$ and the input for position $t$
- attention mechanisms are integral parts, allowing modeling of dependencies without regard to their distance in the input or output sequences
- transfomers eschewing reccurence and rely entirely on an attention mechanism
- global dependencies between input and output
- significantly more parallelizable

# 2. Background
- Extended Neuronal GPU, ByteNet, ConvS2S have goal of reducing sequential computation
- use convolutional neuronal networks for computing hidden representations in parallel
- number of operations required to relate signal of two inputs/outputs grows in distance (linear for ConvS2S, logarithmic for ByteNet)
- more difficult to learn dependencies between distant positions
- transformers reduce this to constant number of operations
- recudes effective resolution due to averaging attention-weighted positions

- Self-Attention is a mechanism that relates different positions of a single sequence to compute a representation
- used successfully in a variety of tasks (readin comprehension, abstractive summarization, textual entailment)

- End-to-end memory networks are based on recurrent attention mechanisms instead of sequence-aligned recurrence

- transformers first transduction model that relies entirely on self-attention without using sequence-aligned RNNs or convolution

# 3. Model Architecture
- mostly encoder.decoder architecture
- encoder maps input sequence to sequence of continuous representations
- decoder generates output sequence
- model is auto-regressive, takes previously generated symbols as additional input

- transformer uses stacked self-attention and point-wise, fully connected layers for both the encoder and decoder

## 3.1 Encoder and Decoder Stacks
Encoder
- stack of $N=6$ identical layers
- two sublayers
    - first is multi-head self-attention mechanism
    - second is simple, position-wise fully connected feed-forward network
    - residual connnection around each sublayer
    - output of sublayer is LayerNorm(x + Sublayer(x))
    - facilitate residual connections, all output dimensions are 512

Decoder
- stack of $N=6$ identical layers
- three sublayers
    - multi-head attentionl over output of encoder stack
    - modify self-attention sublayer, to prevent positions from attending to subsequent positions
    - masking + output embeddings offset by one position => prediction of i relies on positions less then i

## 3.2 Attention
- is a mapping of a query and a set of key-value pairs to an output (all vectors)
- output = weighted sum of values
- weight = compatibility function of query and key

### 3.2.1 Scaled Dot-Product Attention
- input = queries and keys ($d_k$ and $d_v$ dimensional vectors)
- dot-product of query and key
- divide by $\sqrt{d_k}$
- apply softmax
- = weights on values

- in practice set of queries simultaneously, packed into matricies
- $Attention(Q,K,V) = softmax(\frac{QK^T}{\sqrt{d_k}})V$

- most common attention masks are additive and dot-product
- dot-product identical except for scaling
- additive = feed-forward network with single hidden layer
- dot-product much faster and space-efficient
- additive outperforms without scaling for larker $d_k$ => scale by $\sqrt{d_k}$

### 3.2.2 Multi-Head Attention
- linearly project queries, key and values h times
- different, learned projections to $d_k$, $d_k$ and $d_v$ dimensions
- on each projection, apply attention function in parallel
- concatenate and project again
- allows to attend to information from different representation subspaces at different positions
- 8 parallel attention layers
- $d_k = d_v = d_{model}/h = 64$

### 3.2.3 Applications of Attention in our Model
- encoder-decoder attention layers
    - queries = previous decoder layer
    - keys and values = output of encoder
    - allows every position in decoder to attend over all positions in input sequence
- endoder self-attention layers
    - queries, keys and values = output of previous layer in encoder
- decoder self-attention layers
    - queries, keys and values = output of previous layer in decoder
    - prevent leftward information flow in decode via masking out all values in input of softmax that have illegal connections

## 3.3 Position-wise Feed-Forward Networks
- each layer has fully connected feed-forward network
- two linear tranformations with ReLU activation
- $FFN(x) = max(0, xW_1 + b_1)W_2 + b_2$
- different parameters from layer to layer
- dimensionality input & output = $d_{model} = 512$
- inner layer = $d_{ff} = 2048$

## 3.4 Embeddings and Softmax
- learned embeddings, converts input & output tokens to vectors of dimension $d_{model}$
- learned linear transformation and softmax to convert decoder output to predicted next-token probabilities
- share weights between two embedding layers and pre-softmax linear transformation

## 3.5 Positional Encoding
- add positional encodings to input embeddings at the bottom of encoder and decoder stacks
- sine and cosine function $PE_{(pos,2i)} = sin(pos/10000^{2i/d_{model}})$ $PE_{(pos,2i+1)} = cos(pos/10000^{2i/d_{model}})$
- easily learn to attend by relative positions, for any fixed offset $k$, $PE_{pos+k}$ can be represented as linear function of $PE_{pos}$

- learned positional embeddings produce identical results, but functions may allow model to extrapolate to sequences longer than those encountered during training


# 4. Why Self-Attention
- compare self-attention to recurrent and convolutional layers
- used for mapping variable-length sequence to another sequence of equal length
- three desiderata
  - total computational complexity per layer
    - self-attention contstant number of sequentially executed operations
    - reccurent requires $O(n)$
    - self-attention faster if sequence length $n$ is smaller than feature dimensionality $d$
    - improve computational performance for very long sequences, consider only neighborhood of size $r$ around each position
  - amount of computation that can be parallelized
    - convolutional layer requires stack of $O(n/k)$ layers (contiguous kernels), $O(log_k(n))$ layers (dilated convolutions)
    - convolutional layer more expensiv than recurrent layers by factor $k$
    - Separable convolutions reducce complexity to $O(k*n*d+n*d^2)$ but still equal to self-attention and point-wise feed-forward layer
  - path lenth between long-range dependencies
    - key factor: length of paths forward and backward signals have to traverse
    - shorter these paths, easier to learn long-range
    - => maximum path length between any two input and output positions in different layer types
- self-attention yields more interpretable models
- individual attention heads learn to perform different tasks
- relate to syntactic and semantic structure

# 5. Training
## 5.1 Training Data and Batching
- English-German dataset from WMT 2014
  - 4.5M sentence pairs
  - encoded using byte-pair encoding
  - 37000 token vocabulary
- English-French dataset from WMT 2014
  - 36M sentence pairs
  - 32000 token vocabulary
- batches with approximate sequence length
  - set of sentence pairs, 25000 source tokens, 25000 target tokens

## 5.2 Hardware and Schedule
- 8 NVidia P100 GPUs
- each training step took 0.4s
- 100.000 Steps for 12 hours
- for big models, step time was 1.0s
  - 300.000 steps for 3.5 days
  
## 5.3 Optimizer
- Adam optimizer with $\beta_1 = 0.9$, $\beta_2 = 0.98$ and $\epsilon = 10^{-9}$
- learning rate varied over course of training
  - $lrate = d_{model}^{-0.5} * min(step\_num^{-0.5}, step\_num * warmup\_steps^{-1.5})$
- increases learning rate linearly for first warmup_steps
- then decreases proportionally to inverse square root of step number
- warmup_steps = 4000

## 5.4 Regularization
- Residual Dropout
  - to output of each sub-layer before added to input of next sub-layer and normalized
  - for sum of embeddings
  - for positional encodings in encoder and decoder stacks
  - rate = 0.1

- label smoothing
  - $\epsilon_{ls} = 0.1$
  - hurts perplexity, model learns to be more unsure
  - improves accuracy

# 6. Results
## 6.1 Machine Translation
- big model 28.4 (English-German), 41.0 (English-French) better BLEU score
- even base-model outperforms, with fraction of training cost

## 6.2 Model Variations
- less and too many heads results in worse results
- reducing attention key size hurts model quality
  - more sophisticated compatibility function than dot-product may be beneficial
- bigger models are better
- drop-out helps in avoiding over-fitting

## 6.3 English Constituency Parsing
- not important

# 7. Conclusion
