# Paper
```bibtex	
@inproceedings{petroni-etal-2019-language,
    title = "Language Models as Knowledge Bases?",
    author = {Petroni, Fabio  and
      Rockt{\"a}schel, Tim  and
      Riedel, Sebastian  and
      Lewis, Patrick  and
      Bakhtin, Anton  and
      Wu, Yuxiang  and
      Miller, Alexander},
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)",
    month = nov,
    year = "2019",
    address = "Hong Kong, China",
    publisher = "Association for Computational Linguistics",
    doi = "10.18653/v1/D19-1250",
    pages = "2463--2473",
}
```

# Abstract
- improvements in downstream tasks
- lm not only contain linguistic knowledge, also storing relation knowledge
- may answer fill-in-the-blank questions
- in-depth analysis of knowledge present without fine-tuning
- show potential as unsupervised open-domain QA systems

# 1 Introduction
- ELMo and BERT
  - optimized for prediction of next word or masked word
- accessed by conditioning on latent context or fine-tuning on tasks


- knowledge bases, enable queries of relational data
- in reality, often need to extract relational data from text to populate knowledge bases
- need a lot of nlp tasks, errors can easily propagate
- lm require no schema engineering, no human annotation, support open set of queries

- how much relation knowledge already present in off-the-shelf lms
- do facts differ (relation, common sense, general question answering)

- present Language model Analysis (LAMA)
- knows fact, if it can predict masked objects in (subject, relation, object)
- Wikidata, ConceptNet, SQuAD

- BERT-large caputes relation knowledge comparable to knowledge base oft relation extractor
- for some relations (n-to-m) performance very poor
- BERT-large consistently outperforms other lms

# 2 Background
## 2.1 Unidirectional Language Models
- sequence of tokens, assign probability to next token given previous ones
- mainly computed by $softmax(Wh_t+b)$
  - $h_t$ leanred parameter matrix
  - models differ how compute $h_t$
    - multi-layer perceptron
    - convolutional layers
    - recurrent neural networks
    - self-attention mechanisms

## 2.2 Bidirectional Language Models
- sequence of tokens, assign probability to token between given tokens
- ELMo: foward and backward LSTM
- BERT: sample positions randomly, predict masked positions

# 3 Related Work
- not included gptv2, since open-source version achieves 1% of natural questions

# 4 LAMA Probe
- knowledge sources of a corpus of facts
- subject-relation-object triples
- question-answer pairs

## 4.1 Knowledge Sources
- Google-RE (Wikipedia facts)
- T-REx (Expanded Wikipedia facts)
- ConceptNet (OMCS sentences)
- SQuAD (question answering)

# 4.2 Models
- fairseq-fconv
- Transformer-XL large
- ELMo original, 5.5B
- BERT base, large

##  4.3 Baselines
- Freq: upper bound performance for model, that precits same word for same objective
- RE: naive entity linking, oracle for entity linking
- DrQA: TF/IDF finds top k articles, reading comprehension to extract answer

## 4.4 Metrics

## 4.5 Considerations
- Manualy Defined Templates
  - worse and better queries
  - therefore measuring lower bound
- Single Token
  - multi-token obscures knowledge cause of more hyperparameters
- Object Slots
- Intersection of Vocabularies
  - only rank for joint vocabulary to not give edge to larger models

# 5 Results
- Google-RE
  - BERT-large outperforms all other models
- T-REx
  - BERT close to relation extraction system
  - High for 1-1, low for N-M
  - high-confidence often means correct answer
- ConceptNet
  - BERT-large outperforms all other models
  - similar to to factual knowledge
- SQuAD
  - remakably small gap between DrQA and BERT-large

# 6 Discussion and Conclusion
- BERT might have advanage due to large amount of data processed
- assessing multi-token answers remains open challenge