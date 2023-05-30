# Paper
```bibtex
@inproceedings{sennrich-etal-2016-neural,
    title = "Neural Machine Translation of Rare Words with Subword Units",
    author = "Sennrich, Rico  and
      Haddow, Barry  and
      Birch, Alexandra",
    booktitle = "Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = aug,
    year = "2016",
    address = "Berlin, Germany",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/P16-1162",
    doi = "10.18653/v1/P16-1162",
    pages = "1715--1725",
}
```

# Abstract
- normal neural machine translation has fixed vocabulary
- translation is open-vocabulary problem
- previous work with backoff to dictionary
- now divide into subword units
  - names via character coyping / transliteration
  - compounds via compositional translation
  - cognates/loanwords via phonological/morphological transformations
- suitability of different word segmentation techniques
  - byte pair encoding
  - character n-gram moidels
- empirically show tha bpe outperforms back-off dictionary

# 1 Introduction
- vocab typically 30k - 50k words
- especially hard for languages with compunding/agglutination
- word-level NMT solved by backoff to dictionary lookup
  - does not always work (no equivalent word in dictionary)
- copying unkown words works for names, but not much else
- goal: no backoff to dictionary
- additional: has better performance
- contributions
  - encode rare words by subword units
    - architecture is simpler and moreeffective
  - adapt byte pair encoding to word segmentation task

# 2 Neural Machine Translation
- approach moddeled after nmt architecture from 2015
- but not specific to it
- = encoder-decoder network with RNN ( recurrent neural networks)

- encoder = bidirectional neural network gated with recurrent units
- input -> forward sequence of hidden states, backward sequence of hidden states
- hidden states concatenated to obtain annotation vector

- decoder = recurrent neural network
- predicts target sequence
- each word predicated based on recurrent hidden state, previous predicted word, context vector
- context vector = weighted sum of annotation vector
- weight of each annotation computed via alignment model
  - models probability that predicted word is aligned to input word
  - = single-layer feed-foward NN
  - learned jointly via backpropagation

# 3 Subword Translation
- based on assumption: words can be translated if word is novel to translator, but based on subword units
- named entities
  - copied from source to target
  - transcription/ transliteration for different alphabets
- cognates / loanwords
  - common origin, differ in regular ways
  - character-level translation sufficient
- morphologically complex words
  - compounding, affication, inflection
  - translate morphemes separately

- analysis of german rare tokens in dataset, majority translatable via subword units

## 3.1 Related Work
- statistical machine translation
- large portion are names (require only transliteration)
- character-based translation investigated with phrase-bassed models
- segmentation of morphologicaly complex words widely used for SMT
  - commonly used for phrase-based SMT
  - conservative in their splitting decisions
  - here aim for aggressive segmentation

- best choice may be task-specific
  - speech recognition: phone-level lm
  - subword lm: syllable segmentation
  - multilingual: other algorithms

- fixed-length continuous word vectors
  - techniques for NMT show no significant improvement over word-based
- expect attention mechanism benefiting from variable-length representation

- for nmt insentive: minimize vocab size to increase time/space efficiency
- but also compact text representation (increased text length recudes efficiency)
- compromise: list of short words, subword only for rare words
- alternative: byte pair encoding - good compression rate

## 3.2 Byte Pair Encoding
- iteratively replaces most frequent pair of bytes with unused byte
- adapt to merge characters/character sequences

- initialize with character vocab + end-of-word symbol
- every word is sequence of characters
- iteratively count each symbol pairs, replace most frequent with new symbol
- each new symbol represent character n-gram
- frequent n-grams merges into single symbol
- final symbol vocab size = initial vocab size + number of merge operations

- do not consider cross-word boundaries
- dictionary with weighted words (frequency)
- main difference: symbols are still subword units

- issues if all occurences merged into large symbols => unkown symbol
- solution: recursively reversing merges

- evaluate two methods
  - two independent encodings (source, target)
  - union of two vocabularies

- names segmented differently depending on language
- solution: transliterate into latin alphabet, bpe, transliterate back

# Evaluation
- can translation of rare/unseen words be improved
- which segmentation performs best

- english-german (4.2 million sentence pairs)
- english-russian (2.6 million sentence pairs)
- results reported with BLEU, CHRF3, and others

- hidden layer size of 1000
- embedding layer size of 620
- 7 day training, last 4 saved models (12h timespan)
- continue training with fixed embedding layer


## 4.1 Subword statistics
- translation quality empirically verified
- efficient training and decoding statistics
- n-gram tradeoff between sequence length and vocabulary size
- reduce sequence length by leaving short list of k most frequent word types
- unigram representation performed poorly
- bigram unable to represent some tokens

- bpe meets goals
- produces no unknown symbols
- more compact representation allows for shorter sequences

## 4.2 Translation experiments
- base line WDict = word-level model with backoff dictionary
- WUnk = no backoff dictionary, replaces unknown words with UNK

- small improvements with backoff
- often unable for english-> russian (no transliteration)
- best improvement of bpe when alphabets differ

- learning from vocab union is more effective than separate vocabularies
- but all methods perform better than baseline

- suspect underestimation of rare words in BLEU und CHRF3 score
- since words often hold essential information

- good performance with e->d
- but slightly worse than newstest2015 (used dropout)

- performance highly differ between models
- future research to control randomness

# 5 Analysis
## 5.1 Unigram acccuracy
- main claim: translation of rare words is poor in word-level nmt models
- 
