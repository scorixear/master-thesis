# Paper
```bibtex
@article{10.1093/bioinformatics/btz682,
    author = {Lee, Jinhyuk and Yoon, Wonjin and Kim, Sungdong and Kim, Donghyeon and Kim, Sunkyu and So, Chan Ho and Kang, Jaewoo},
    title = "{BioBERT: a pre-trained biomedical language representation model for biomedical text mining}",
    journal = {Bioinformatics},
    volume = {36},
    number = {4},
    pages = {1234-1240},
    year = {2019},
    issn = {1367-4803},
    doi = {10.1093/bioinformatics/btz682}
}
```

# Abstract
- biomedical text minim increasinly important as number of documents rapidly grow
- retrieve information from documents
- vocabulary does not match biomedical corpora

- biomedical named entity recognition, biomedical relation extraction, biomedcial question answering

# 1 Introduction
- named entity recognition improved by LSTM and CRF
- relation extraction, question answering
- recent models rely on adapted versions of word representation
- BERT cannot achieve high-performance, because not pretrained on domain-specific corpora

# 2 Approach
- BioBERT for biomedical domain
- pretrained BERT, continued pretraining on biomedical domain corpora, fine-tuned  for specific tasks
- 23 days, 8 NVIDIA V100 GPUs
- improved on every f1 score for tasks
- can do multiple tasks from biomedical text mining

# 3 Materials and methods
- bidirectional ecnoding for better understanding of natural language
- hypothesize this is a requirement for biomedical terms
- BERT uses masked language modeling

## Pre-Training BioBERT
- BERT pretrained on english wikipedia and book corpus
- continued pretraining on pubmed abstracts and full-text articles
- wordpiece tokenization, mitigates out-of-vocabulary problem by dividing into subword units

## Fine-tuning BioBert
- Named entity recognition: recognize numerous proper nouns in biomedical corpus
- Relation extraction: classify relations of named entities (true or false statements)
- question answering: predict start and end position in given passage

# 4 Results
## Datasets
- 10-fold cross-validaton on datasets with no separate test sets
## Experimental setups
- 1M BERT steps
- 470K BioBert v1.0 steps
- 1M BioBert v1.1 steps
- Naver Smart Machine Learning (used for training large-scale on multiple GPUs)
- Sequence Length 512, mini-batch 192
- fine-tuning on single gpu, 20 epochs, 10-64 batch size, 5e-5 - 1e-5 learning rate

## Experimental results
- BioBert outperforms on 6 out of 9 datsets

# 5 Discussion
- performance changes in relation to size of pubmed corpus
- effectiveness is evident

# 6 Conclusion
- 