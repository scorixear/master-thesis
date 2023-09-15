# Paper
only arxiv publish
```bibtex
@misc{dai2022knowledge,
      title={Knowledge Neurons in Pretrained Transformers}, 
      author={Damai Dai and Li Dong and Yaru Hao and Zhifang Sui and Baobao Chang and Furu Wei},
      year={2022},
      eprint={2104.08696},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

# Abstract
- llms good at recalling factual knowledge
- present how factual knowledge stored in transfomers
- propose knowledge attribute method
- edit specific factual knowledge without fine-tuning

# 1 Introduction
- evaluation show transfomers have strong ability to recall factual knowledge (TODO: link)
- knowledge attribution method to identify neurons -> express relational act
- feed-forward network = key-value memories (TODO: link)
  - computing contribution of neuron to knowledge prediction

- surpressing/amplifying neurons affects expression of knowledge
- more effected by knowledge expressing promptys


- preliminary studies:
  - updating facts
  - erasing relations
- shows promising results, don't affect other knowledge

# 2 Background: Transformer
- tranformer encoder = L identical blocks stacked
  - self-attention module
  - feed-forward network
  - $Q_h=XW_h^Q$, $K_h=XW_h^K$, $V_h=XW_h^V$
  - $\text{Self-Att}_h(X)=softmax(Q_hK_h^T)V_h$
  - $FFN(H)=gelu(HW_1)W_2$
  - Self attention module computes attention head, H is projection of concatenation of all heads

Connections Between Self-Attention and FFN
- self-attention similar to ffn
- softmax = gelu, key & value = weights (TODO: link)

# 3 Identifying Knowledge Neurons
- factual knowledge stored in FFN

## 3.1 Knowledge Assessing Task
- fill-in-blank cloze task
- triplet hrt, h = head entity, t = tail entity, r = relation
- given fact, models answers cloze query x
- = knowledge-expressing prompt

## 3.2 Knowledge Attribution
- based on integrated gradients
- examine FFN intermediate neurons for masked token
- model output probability of correct answer
  - $P_x(\^{w}_i^{(l)})=p(y^*|x,w_i^{(l)}=\^{w}_i^{(l)})$
  - $y^*$ correct answer
  - $w_i^{(l)}$ i-th neuron in l-th layer
  - $\^{w}_i^{(l)}$ given constant assigned to $w_i^{(l)}$
- attribute Score $Attr(w_i^{(l)})$ gradually change $w_i^{(l)}$ from 0 to $\bar{w}_i^{(l)}$ (original value)
- integrate gradients, $Attr()$ accumlates output probability change caused by chaning $w$
- if influence is great, gradient is salient, integration is large
- use Rieman approximation with 20 approximation steps instead of calculating continuous integrals

## 3.3 Knowledge Neuron Refining
- may contain false-positive neurons, that represent other information
  - syntaic information
  - lexical information
- refining to filter these out
- different prompts have same knowledge neurons
- do not share false-positive

- produce n diverse prompts
- for each prompt, calculate knowledge attribution score
- for each prompts, retain neurons with score > threshold t
- consider all sets of neurons, choose neurons with >p% prompts

# 4 Experiments
## 4.1 Expreimental Settings
- BERT-base-cased
- 12 transformer blocks, 768 hidden size, 3072 ffn size
- easily generalized to other models
- attribution threshold t = 0.2x max(Attr(w))
- refining threshold p = 0.7, de/increased by 0.05
- v100 GPUs
- avg. 13.3s to identify knowledge neurons (9 Prompts)

## 4.2 Dataset
- fill-in-the-blank cloze task
- ParaRel dataset
  - prompt templates for 28 relations from T-REx
  - filter out relations with <4 prompt templates
  - 34 relations, 8.63 prompt templates
  - 253k knowledge expressing prompts
  - 27k relational facts

## 4.3 Attribution Baseline
- neuron activation value = attribution score
- choose hyperparameters t, p% to have [2,5] knowledge neurons per relation

## 4.4 Statistics of Knowledge Neurons
- most fact-related neuron in topmost layers
- 4.13 knowledge neurons avg
- baseline identifies knowledge neurons mostly shared by intra-relation fact and often in common for inter-relation facts
- proposed method identifies exclusive knowledge neurons

## 4.5 Knowledge Neurons Affect Knowledge Expression
- surpress by setting activation to 0
  - 29.03% decrease in correct probability
  - base-line negligible influence
- amplify by doubling activation
  - 31.17% increase in correct probability
  - base-line decrease by 1.27%
- if knowledge neurons are distributed more widely, need to manipulate more top-k neurons

## 4.6 Knowledge Neurons are Activated by Knowledge-Expressing Prompts
- BingRel Dataset
  - crawling bing search engine for new prompts
  - for ParaRel facts, get up to 10 text containing head and tail
  - get upt to 10 texts containing only head
  - surpressed tails for first 10 to get knowledge expressing prompts
  - surpressed random words for second 10 to get control group
  - random sampled prompts as third control group
- knowledge neurons significantly activated by knowledge-expressing prompts
- baseline cannot distinguish prompts

# 5 Case Studies
## 5.1 Updating Facts
Methods
- identify knowledge neurons for <h, r, t>
- retain neurons shared <10% in intra-relation facts
- modify value slot: $FFN_i^{(val)}=FFN_i^{(val)}-\lambda_1t+\lambda_2t'$
- $t$, $t'$ = word embeddings of t and t'
- $\lambda_1$, $\lambda_2$ = 1 and 8

Setup
- on ParaRel
- sample ten facts
- choose random different entity t' for <h, r, t> of same type
- manipulate four top knowledge neurons

Evaluation Metrics
- change rate t is modified to t'
- success rate t' becomes top prediction
- influence on other neurons intra-relation PPL (increase of perplexity for prompts with same relation r)
- inter-relation PPL (increase of perplexity for prompts with different relations)

Results
- non-trivial success rate for knowledge neurons
- insufficient for random neurons
- little negative influence on other neurons
- improve success rate by including more top knowledge neurons


## 5.2 Erasing Relations
Methods
- given relation r, identify knowledge neurons for all relational facts with r
- retain 20 knowledge neurons, that appear most frequently
- set $FFN^{(val)}$ to 0

Results
- erasing operation results in increased perplexity
- provides promising way to erase undesired knowledge

# Limitations
- fill-in-blank cloze task for knowledge expression -> could be more implicit expressed
- un-answered for generalized tasks such as reasoning
- only focused on factual knowledge
- used single-word blank
- multilingual pre-trained models not explored