# Paper
arxiv publish
2020
```bibtex
@article{DBLP:journals/corr/abs-1909-08593,
  publtype={informal},
  author={Daniel M. Ziegler and Nisan Stiennon and Jeffrey Wu and Tom B. Brown and Alec Radford and Dario Amodei and Paul F. Christiano and Geoffrey Irving},
  title={Fine-Tuning Language Models from Human Preferences},
  year={2019},
  cdate={1546300800000},
  journal={CoRR},
  volume={abs/1909.08593},
  url={http://arxiv.org/abs/1909.08593}
}

```

# Abstract
- build generative pretraining of languag models applying reward learning

# 1. Introduction
- reinforcment learning for complex tasks, that are only defined by human judgment
- result is good or bad by asking humans

- only recently been applied to deep learning, any olny to simple environments
- goals are likely to involve and require natural language


- nlp successfully done with unsupervised pre-training and supervised fine-tuning
- outperforms supervised dataset from scratch
- in some cases fine-tuning not required (#TODO: check this https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)

- reinforcement learning uses algorithmically defined reward functions (BLEU for translation, ROUGE for summarization, music theory-based rewards, event detectors for story generation)

- in this paper fine-tune pretrained model with reinforcement learning
- use model trained from human preferences
- apply to two tasks: continuing text, summarize text
- results: 86% more prefered vs zero shot; 77% more prefered vs supervised fine-tuning
- copying behavour emerged naturally from data collection and training process


# 2. Methods
- $\Sigma$ = vocabulary
- $p$ = language model
- $p(x_0\dots x_{n-1} = \prod\limits_{0\leq k<n} p(x_k | x_0 \dots x_{k-1})$
- X = input space
- Y = output space
- Expected Reward $\mathbb{E}_{\pi}[r] = \mathbb{E}_{x\thicksim\mathcal{D},y\thicksim\pi(\cdot|x)}[r(x,y)]$
  - $\pi$ = policy, initially $p$, then fine-tuned
  - $\mathcal{D}$ = distribution over inputs
  - $r: X \times Y \rightarrow \mathbb{R}$ = reward function
- humans choose best option out of 4
  - $S: \{x,y_0,y_1,y_2,y_3,b\}$ = dataset tuples
  - $loss(r) = \mathbb{E}_{(x,\{y_i\}_i,b)\thicksim S}[\log \frac{e^{r(x,y_b)}}{\sum_i e^{r(x,y_i)}}]$ = loss function for reward model


overall trainig process
- gather samples $(x,y_0,y_1,y_2,y_3,b)$, ask humans to pick bet $y_i$
- initialize $r$ to $p$, using random initialization, train $r$ using loss and human samples
- Train $\pi$ via Proximal Policy Optimization
- continue data collection and periodically retraing $r$

## 2.1. Pretraining details
- GPT-2 774M model
- Supervised fine-tuing using BookCorpus prior to RL-finetuning

## 2.2. Fine-tuning details
- Adam optimizer with loss
- batch size 8 for style task, 32 for summarization
- learning rate 1.77e-5
- single epoch to avoid overfitting

## 2.3. Online data collection
- if $\pi$ very different to $p$, then reward model suffers large distributional shift
- to prevent. continue retraining $r$

## 2.4. Humnan labeling
- usage of scale ai to collect labels
- problem: no unambiguous ground truth
- authors agreed 60% on labels authors vs scale

# 3. Experiments
- first compare approach to mock labeler
- then show stylistic continuation task with little data
- then fine-tuning on CNN TL;DR dataset

## 3.1. Stylistic continuation task
- excerpt from BookCorpus presented, continuation of text
- 32 or 64 token length, 24 tokens generated
- Temperature of 0.7

### 3.1.1. Mock sentiment task
- optimize known reward function $r_s$
- $r_s$ constructed by training classifier on Amazon review datasets
- predicts if positive or negative sentiment
- simulate human by always choosing higher reward of $r_s$

### 3.1.2 Human evaluations of continuations
- tasks: sentiment = reward positive and happy; descriptiveness = reward vividly descriptive
- excertps that start and end with period
- rejection sampling = period between 16 and 24, truncate to period
  - penalized if no period

- performance with 5k, 10k and 20k is similar => litte data required for human fine-tuning
- sentiment classifier performs 77% poorly vs human feedback

## 3.2 Summarization
- CNN/DailyMail dataset
- TL;DR dataset
- 500 tokens, respond with 75 tokens
- T = 0.5 and 0.7

- truncated to last new line
- rejection sampling = new line betwwen 55 and 75

- significant returns to data volume up to 60k
- reliably bets zero-shot model
- mostly copies sentences
- online model beats ground truth 96% and 84%

### 3.2.1 What our models copy
- goal is to be abstractive rather than extractive
- RL fine-tuning leads to copy more consistently
- no significant better performance compared to zero-shot
- zero-shot accurate only 20% of the time
- since labeler do not penalize copying, results are more copying, but at least no lying


# 4. Challenges
## 4.1 Online dat collection is hard
- each label comes from up-to-date collection
- software complexity due to data gatheing, reward model training and rl fine-tuning very high and prune to bugs
- machine learning complexity
- quality control issues hard to detect

- better to train online in batches

## 4.2. Sharing parameters between reward model and policy causes overfitting
- best to have join reward and policy model
- would help prevent policy to exploit reward model
- improve computationyl efficiency
- but policy trained on 2M, while reward on 60k
  - would result in more epochs for reward => overfitting

## 4.3. Ambigous tasks make labeling hard
- labeler have to choose between two slightly wrong summaries => subjective
- often "noise" in labeling then since disagreements between labeler
- better option could be to describe what problems the summarization has

# 4.4. Bugs can optimize for bad behavior
- flipping reward and KL penalty results in profane text

# 5. Conclusion
- continuation tasks good results compared to zero-shot with few samples
- summarization tasks results in only smart copiers