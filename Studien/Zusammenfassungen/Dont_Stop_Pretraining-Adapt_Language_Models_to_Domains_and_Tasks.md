# Paper

```bibtex
@inproceedings{gururangan-etal-2020-dont,
    title = "Don{'}t Stop Pretraining: Adapt Language Models to Domains and Tasks",
    author = "Gururangan, Suchin  and
      Marasovi{\'c}, Ana  and
      Swayamdipta, Swabha  and
      Lo, Kyle  and
      Beltagy, Iz  and
      Downey, Doug  and
      Smith, Noah A.",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2020.acl-main.740",
    doi = "10.18653/v1/2020.acl-main.740",
    pages = "8342--8360",
}
```

# Abstract
- is it still helpful to tailor pretrained models to domain tasks
- leads to performance gains when domain-adaptive pretraining
- task-adaptive pretraining is more effective than domain-adaptive

# 1. Introduction
- language models trained on massive heterogeneous corpora achieve strong performance across many tasks
- is task textual domain still relevant?
- cite shows that continued pretraining on domain-specific unlabeled data shows benefitg (TODO:)
  - considers only single domain
  - might be dependend on size of data and proximity to original pretraining corpus

- consider four domains (biomedical, computer science, news, reviews)
- eight classification tasks (two per domain)
- if domain not already part of RoBERTa, consistently improved performance
- task-adaptive pretrainig = task-relevant corpus shows largest gains

- paper contains
  - analysis of domain and task adaptation
  - transferability of adapted LMs to domains and tasks
  - highlight of importance of pretraining human-curated datasets
  - data selection strategy to automatically approach this performance

# 2. Background: Pretraining
- normally two stages: training LM on unlabeled corpus
- then supervised training for downstream task
- RoBERTa such pretrained LM
- continue training to large corpora of domain-specific text
- or available unlabeled data associated with given task

# 3. Domain-Adaptive Pretraining
- continue training on large corpus of unlabeled domain-specific text

## 3.1 Analyzing Domain Similarity
- quantify domain similarity
- by comparing unigram occurences in vocabulary
- news and reviews similar, while biomedical and cs are more distinct


## 3.2 Experiments
- results to four domain-adapted LMs

Baseline
- off the shelf basemodel
- supervised fine-tuning for each classification task

Classification Architecture
- final layer token to task-specific feed-forward layer

Results
- dapts improves in all domains
- consistens accross high and low resource settings
- benefits in HYPERPARTISAN suggests even benefitial for closely related domains

## 3.3 Domain Relevance for DAPT
- compared DAPT to LM adapted outside of domain of interest
- exposes if simply exposure to more data is beneficial
- significantly outperforms adapting to irrelevant domains

## 3.4 Domain Overlap
- task data assigned to specific domains (eg helpfullness to amazon reviews)
- gradiation between domains show fuzzy boundaries
- qualitatively overlapping douments in domains
- pretraining beyond conventional domain boundaries is beneficial

# 4. Task-Adaptive Pretraining
- task datasets tend to cover subset of domain
- hypothesize that pretraining on task dataset might be helpful

- tapt is unlabeled training for task
- uses far smaller pretraining corpus, but much more task-relevant

## 4.1 Experiments
- second phase of pretraining roberta
- dapt 12.5k steps, tapt 100 epochs
- augment dataset by masking different words (prob of 0.15)

- consistently improves baseline
- dapt more resource intensive, but tapt matches performance

combined dapt and tapt
- dapt then tapt
- achieve best performance
- tapt then dapt might be susceptivle to forgetting task-relevant corpus

Cross-Task Transfer
- adapting to one task transfer to other tasks?
- answer: no

# 5. Augmenting Training Data for Task-Adaptive Pretraining
- human curated larger unlabeled corpus
- or in-domain unlabeled corpus (where human-curated not available)

## 5.1 Human Curated-TAPT
- Dataset creation often from large unlabeled corpus
- involves collection annotations
- why not use this corpus

Data
- simulate by downsampling to 500 examples (out of 180k)
- use 5k for curated-tapt, and original low-resource for fine-tuning

Results
- almost as good as dapt+tapt, with only 0.3% of data

## 5.2 Automated Data Selection for TAPT
- no access to large amounts of unlabeled data
- absence of computational resources for DAPT
- find task-relevant data from domain by embedding text from both task and domain
- use VAMPIRE to obtain embeddings from task and domain samples
- select k candidates with nearest neighbour

Results
- outperforms tapt
- approaches dapt

## 5.3 Computational Requirements
- tapt 60x faster than dapt
- storage 5.8M times bigger for dapt
- but resue of dapt lm for training on multiple tasks
- 