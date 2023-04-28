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
