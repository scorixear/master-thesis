# Paper
```bibtex
@inproceedings{pfeiffer-etal-2020-adapterhub,
    title = "{A}dapter{H}ub: A Framework for Adapting Transformers",
    author = {Pfeiffer, Jonas  and
      R{\"u}ckl{\'e}, Andreas  and
      Poth, Clifton  and
      Kamath, Aishwarya  and
      Vuli{\'c}, Ivan  and
      Ruder, Sebastian  and
      Cho, Kyunghyun  and
      Gurevych, Iryna},
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations",
    month = oct,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2020.emnlp-demos.7",
    doi = "10.18653/v1/2020.emnlp-demos.7",
    pages = "46--54",
}
```

# Abstract
- current way is downloading, finetuning models
- storing and sharing models is expensive, slow, time-consuming
- adapter = learnt bottle-neck layers inserted within each layer
  - avoiding full fine-tuning
  - sharing adapters not straight-forward
- Adapterhub = framework for stitching adapters with models

# 1 Introduction
- transformers reach sota with fine-tuning
- models performance scales with size
- sharing/training on multiple tasks often prohibitive
- adapters = alternative lightweight fine-tuning strategy
  - additional newly initialized weights at every layer
  - extra weights trained during fine-tuning, pre-trained weights frozen
  - adapters are model, task, language dependent
- adapterhub mitigates problems
  - built upon huggingface transformers
  - provides easy access, sharing, installation, training of adapters


- easy-to-use and extensible adapter training
- incorporated into huggingface transformers
- automatic extraction of adapter weights
- open-source framework and website for sharing adapters
- incorporate adapter composition, adapter stacking

# 2 Adapters
## 2.1 Adapter Architecture
- additional newly introduced parameters
- new parameters trained on target task, while model parameters frozen
- predominantly focus on adapter per task
- each transformer layers gets adapter parameters introduced
- two-layer feed-forward nn with bottleneck works well (TODO: link)
- placement & new layernorms vary in literature
- architecture can be defined dynamically

## 2.2 Why Adapters?
- scalability, modularity, composition

Task-specific Layer-wise Representation Learning
- same performance, but no fine-tuning required

Small, Scalable, Shareable
- require as little as 0.9MB storage space
- 2 Fully finetuned bert models = 125 models with adapters
- make adapters comptuationally, ecologically viable

Modularity of Representations
- since other weights fixed
- adapter learns output representation compatible with subsequent layer
- adapters can be stacked

Non-Interfering Composition of Information
- multi-task learning suffers from catastrophic forgetting
  - early stages of training are overwritten
- catastrophic interference
  - performance deterioates with adding new tasks
- intricate task weighting
- adapter per task, combine with attention
- no need for sampling heuristics, since adapters trained independently

# 3 AdapterHub
- library on top of huggingface transformers
- website for filtering and analysis of pre-trained adapters

- lifecycle tasks of adapters
  - introducing adapter weights into transformer
  - training adapter weights while keeping model weights frozen
  - extraction of adapter weights and open-sourcing the adapters
  - visualization of adapter with configuration filters
  - on-the-fly downloading/caching of pretrained adapters
  - performing inference with adapter transformer models

## 3.1 Adapter in Transformer Layers
- two lines required
- pre-configuration files for common architectures
- configurable placements of weights, residual connections, layernorm layers

## 3.2 Training Adapters
- same as normal fine-tuning
- pre-trained weights frozen
- adapter weights and prediction head are trained

## 3.3 Extracting and Open-Sourcing Adapters
- only adapter weights and prediction heads need to be stored
- reduces storage requirements
- upload zip with meta, automatic tests, available on adapterhub immediately

## 3.4 Finding Pre-Trained Adapters
- adapters sorted by task or language
- separted into data sets / higher-level tasks / languages
- separated into individual datasets
- adapters are not compatible among multiple models

## 3.5 Stitching-In Pre-Trained Adapters

## 3.6 Inference with Adapters

# 4 Conclusion and Future Work
- 