# Paper
```bibtex
@inproceedings{black-etal-2022-gpt,
    title = "{GPT}-{N}eo{X}-20{B}: An Open-Source Autoregressive Language Model",
    author = "Black, Sidney  and
      Biderman, Stella  and
      Hallahan, Eric  and
      Anthony, Quentin  and
      Gao, Leo  and
      Golding, Laurence  and
      He, Horace  and
      Leahy, Connor  and
      McDonell, Kyle  and
      Phang, Jason  and
      Pieler, Michael  and
      Prashanth, Usvsn Sai  and
      Purohit, Shivanshu  and
      Reynolds, Laria  and
      Tow, Jonathan  and
      Wang, Ben  and
      Weinbach, Samuel",
    booktitle = "Proceedings of BigScience Episode {\#}5 -- Workshop on Challenges {\&} Perspectives in Creating Large Language Models",
    month = may,
    year = "2022",
    publisher = "Association for Computational Linguistics",
    doi = "10.18653/v1/2022.bigscience-1.9",
    pages = "95--136",
}
```

# 1 Introduction
- performance scales with number of parameters
- width/depth ratio have minimal impact on performance
- most large models (two order larger than GPT-2) under restricted access
- GPT-Neo, GPT-J, Megatron, Pangu-$\alpha$, FairSeq freely available
- most interesting capabilities emerge above certain number of parameters

# 2 Model Design and Implementation
- autoregressive transformer decoder model
- largely follows GPT3
- 20 billion parameters, 19.9 billion non-embedding
- 44 layers, dimension size 6144, 64 heads

## 2.1 Model Architecture
- choose gpt3, since no canonical published refernce for gpt-j, but almost identical to gpt-j

Rotary Positional Embeddings
- learned positional embeddings
- rotary embeddings = static relative positional embeddings
- twist embeddings space, such that attention between token m and n are linearly dependent on $m - n$
- modified multi-head attention equation to include diagonal matrix, that performs 2D rotation
- not aplied to every embedding vector, but only first 25% of dimensions
- strikes best balance between performance and computational efficiency

Parallel Attention + FF Layers
- attention and ff layers computed in parallel, summed at the end
- residual addition requires one all-reduce, this now locally reduced
- 15% throughput increase
- apply two inpedentend layer norms for attn and ff, due to oversight
- makes no difference in performance

Initialization
- ff output layer initialization scheme, that prevents activations from grwoing with increasing depth
- for all other layers small init scheme

All Dense Layers
- used al dense layers to reduce implementation complexity

## 2.2 Software Libraries
- code based on Megatron and DeepSpeed
- PyTorch 1.10 with CUDA 11.1, bunbled with NCCL 2.10 for distributed communications

## 2.3 Hardware
- 12 servers, each 8 GPUs (40GB), two CPUs

# 3 Training
- used values of GPT3 to guide choice
- interpolate learning rates in correlation to model size
- based on smaller scale experiments, weight decay = 0.01
- batch size 2048, for 1538 contexts
- 150.000 steps, decaying learning rate cosine to 10%
- AdamW optimizer, extended with ZeRO optikmizer (recuded memory consumption)
- Tensor parallelism scheme, combined wit hipieline parallelism to distributed across GPUS (does not fit on one gpu)
  - tensor parallel size = 2, pipeline parallel size = 4
- 117 teraflops per gpus

## 3.1 Training Data
- Pile dataset, from 22 datasources, curated, designed for training llms
- more diverce than gpt3
- StackExchange preprocessed into Q/A form

## 3.2 Tokenization
- bpe-based, similar to gpt2, 50257 tokens
- tokenizer trained  on pile
- consistent space delimitation regardless if start of string
- repeated spaces tokens, to better encode program source code

## 3.3 Data Duplication
- more commonly to train for one epoch
- better results wit deduplication
- opted to use Pile as is
- no validation loss crossing 1 epoch boundary
- no replication possible for deduplicated code (since weights no released)
- but still benefits such as prefention of leakage of training data

# 4 Performance Evaluation
- eleuther ai languag emodel evaluation harness
- compared to english models >10B parameters
- gpt3, fairseq, gptj, not T5 (not autoregressive), not megatron (code non-functional)

## 4.1 Tasks Evaluated
- natural language tasks
- mathematical tasks
- advanced knowledge-based tasks
  - subject areas: humanities, social sciences, stem, miscellaneous

# 5 Discussion
## 5.1 Performance Results
Natural Language Tasks
- outperforms FairSeq on some (22), underperforms on other tasks (4)
- similar with gpt-j, non-explicable

Mathematics
- consistently outperform gpt3 and fairseq

Advanced Knowledge-Based Tasks
- gpt3 in zero-shot close to gpt-neox-20b
- in 5 shot gpt-neox-20b outperforms gpt3

## 5.2 Powerful Few-Shot Learning
- benefit substantially more from few-shot evaluations

## 5.3 Limitations
Optimal Training
- hyperparameter tuning often infeasible for full scale multi-billion parameter models
- potentially hyperparameters not optimal / never were
Lack of Coding Evaluations
- unable to evaluate coding benchmarks due to difficulty and cost
Data Duplication
- not present, might have large effect on perplexity
## 5.2 Releasing a 20B Parameter LLM
- reason to not release: harms that public access to llms would purportedly cause
- providing access to ethics and alignment researches will prevent harm
- limiting access to governments and corporations will not prevent harm
  - large companies can do more harm
  - hardware requirements are too high to do anything significant without needed infrastructure

# 6 Summary

