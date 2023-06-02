# Paper
```bibtex
@inproceedings{jiang-etal-2020-x,
    title = "{X}-{FACTR}: Multilingual Factual Knowledge Retrieval from Pretrained Language Models",
    author = "Jiang, Zhengbao  and
      Anastasopoulos, Antonios  and
      Araki, Jun  and
      Ding, Haibo  and
      Neubig, Graham",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    doi = "10.18653/v1/2020.emnlp-main.479",
    pages = "5943--5959",
}
```

# Abstract
- lm proven successful at capturing factual knowledge
- assess factual knowledge retireval in different languages
- multilingual cloze-style benchmark
- multi-word entities prediciton
- code-switching-bsed method, to improve lms

# 1 Introduction
- most cloze-style prompts written in english
- multilingual lms better at recalling facts in other languages
- new benchmark: Cross-lingual FACTual Retrieval benchmark (X-FACTR)
- similar formulation as LAMA
  - if LM can predict blank for each relation after filling in subject
  - 23 Languages, morphology-sensitive annotation (e.g. gender)

- expand setting to include multi-token (e.g. "United States")
- how & why does performane vary across languages
- can multilingual training improve over monolingual
- how much does knowledge capture over lap in languages

- performance relatively low, better with high-resource languages
- 50% of facts recalled in only 1 language

- code-switching: replace entities in sentence with counterparts from other languages
- results show, this can improve knowledge retrieval

# 2 Retrieving Facts from LMs
- subject-relation-object triples from TREx
- manually set subject, expect object

# 3 Multilingual Multi-token Factual Retrieval Benchmark
## 3.1 Languages
- subset as diverse as possible
- 32 languages
- 11 language families
- 10 different scripts

## 3.2 Facts
- 46 relations, 1000 subject-object pairs each
- some entities might not have all language translations

## 3.3 Prompts
- named entities inflect for case
- verb aggrees with subject/object (person, gender, number)
- retrieve sex_or_gender from wikidata for subjects/objects
- 88% prompts juged as natural an gramatically correct (juged by native speakers)

## 3.4 Evaluation
- jugde predicition if one of valid objects (alias, true mulitple answers)

# 4 Multi-token Decoding
- problem with multi-token entities
- Left-to-right lms easy (autoregressivly decode)
- masked LMs (BERT) remain open problem
- multiple masks

## 4.1 Initial Prediction and Refinement
- predict indepenently (masked in parallel)
- order-based (left-to-right)
- confidence-based (highest confidence first)

## 4.2 Final Prediction
- generate 1..M mask tokens, chooose final prediction by confidence

## 4.3 Additional Components

# 5 X-FACTR Benchmark Performance
- M-BERT, XLM, XLM-R = multilingual
- BERT, CamemBERT, BERTje, BETO, RuBERT, Chinese BERT, BERTurk, GreekBERT = monolingual
- maximal tokens = 5 for english, french, dutch, spanish
- maximal token = 10 for others

## 5.1 Experimental Results
- in most favourable settings, multilingual models less than 15%-5%
- baselines results on 13 languages

- high-resource languages better
- more data during pretraining
- low-resources have fact, but lack of model capacity and forgetting

- M-BERt outperforms XLM, XLM-R on high-resource
- similar on low-resource
- M-BERT outperforms mono-lingual


- possible, that correct prediction of M masks has lower confidence
- performance increases 75% if searched for, but still < 20%

- prominent error
  - repeating subjects
  - wrong entities (29%)
  - non-informative (greek 27%)
  - type errors (8% english)
  - related concepts (7% english)
  - non-existent words (5% english)
  - false negatives 3%
  - inflection 1%

- confidence decoding best for mid-low resource
- hurts high-resource
- improves multi-token, hurts single-token
- performance dependent on language (lots of multi-lingual or not)

# 6 Improving Multilingual LM Retrieval
- 50% of correct facts in single language
- 3% in more than 5 languages
- becasue facts only mentioned in single language

## 6.1 Methods
- 30% probability of switching

# 6.2 Experimental Results
- code-switched fine-tuning allows M-Bert to retrieve facts in English
- english better to learn, since data abundance

# 7 Related Work
- 