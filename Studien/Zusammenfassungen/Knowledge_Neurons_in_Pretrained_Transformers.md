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
- 