# GPT-4 System Card

# 1 Introduction
- finished training in August 2022

## 1.1 Overview of findings and mitigations
- analyze two version: earlier finetuned on instruction following; version fine-tuned for increased helpfulness and harmlessness
- can generate harmful content (planning attacks, hate speech)
- presents societal biases and worldviews
- generate compromised or vulnerable code
- identify private indivisuals
- lower cost of cyberattacks (social engineering, enhaning security tools)
- currently not able to self-replicate

- reduced prevlance to content that violates usage policy
- reduces tendency to hallucinate
- reduced surface area of adversarial prompting

- examples are not zero-shot, cherry picked

# 2 GPT-4 Observerd Safety Challenges
- specific risks:
  - Hallucinations, Harmful content, Harms of representation, allocation, and quality of service
  - Disinformation and influcence operations, Proliferation of conventional and unconventional weapons
  - Privacy, Cybersecurity, Potential for risky emergent behaviors, INteractions with other systems
  - Economic impacts, Acceleration, Overreliance


## 2.1 Evaluation Approach
### 2.1.1 Qualitative Evaluation
- external experts for qualitatively probe, adversarial testing and general feedback
- included stress testing, boundary testing and red teaming
- red team iteratively, hypothesis area - test - adjust - repeat
- expertises: fairness, alignment research, economics, human-computer interaction, law, education, healthcare, industry trust and safety, dis/misinformation, chemisty, biorisk, cybersecurity, nuclear risks
    - selected due to prior observed risks, increased user interest
    - experts reflect bias towards specific educational and professional backgrounds
    - bias towards english-speaking, western countries

### 2.1.2 Quantitative Evaluation
- against hate speech, self-harm advice, illicit advice
- measure likelihood to generate harmful content
- classified using human analysis and classifiers
- during training on different checkpoints evaluated

## 2.2 Hallucinations
- hallucinations become more dangerous the more truthfull the model is
- if truth present in area user is familiar, more likely to trust hallucinations
- measured closed & open domain context hallucinations
  - closed domain: automatic evaluation using GPT-4 as zero-shot classifier and human evaluation
  - open domain: create factual set of data flagged as not factual
    - assess model generation, facilitate human evaluations

- 19% points higher than GPT-3.5 for open domain
- 29% higher for closed domain

## 2.3 Harmful Content
- content that violates policies, may pose harm to individuals, groups or society
- not accounts for context of usage
- gpt4 early can generate harmful content
- gpt4 launch better

## 2.4 Harms of Representation, Allocation, and Quality of Service
- amplify biases and stereotypes
- has potential to reinforce and reproduce specific biases and worldviews
  - example: should woman be allowed to vote
- policies say no use of gpt for high risk government decision making, offering legal or health advice
- some biases mitigrated by training for refusal
  - can exacerbate issues by refusing for specific demographic groups

## 2.5 Disinformation and Influence Operations
- can generate plausible disinformation
  - changing narrative of topic
- can rival human propagandists in many domains
- produce plausible suggestions to create propaganda
- can generate content favourable to autocratic governments

## 2.6 Proliferation of Conventional and Unconventional Weapons
- gpt4 insufficient condition for proliferation
- but can alter information available to proliferators
  - time to research completion shorter with gpt4
- specificly usefull for actors without formal scientific training
- but weeknesses present: too vague to be usable, impractical solutions, prone to making factual errors

## 2.7 Privacy
- may have knowledge about people with significant presence on the public internet
- can complete basic tasks for personal and geographic information
- can be uesed to identify individuals
- mitigations:
  - finetuning to reject requests
  - removing personal information from training data
  - automated model evaluation/monitoring to respond to user attempts

## 2.8 Cybersecurity
- useful for social engineering, summarization of data, parsing audit logs
- has significant limitations due to hallucinations


## 2.9 Potential for Risky Emergent Behaviors
- with bigger models come risks for bevahiours such as long-term planning, power-seeking and agentic
  - agentic = accomplish goals not concretely specified with long-term planning
- power-seeking action often optimal for reward function, and usefull instrumental goal
- aic access to early models without finetuning
  - found ineffective to replicate, acquiring resources, avoiding shutdown
  - not tested on final version (next step)

## 2.10 Interactions with Other Systems
- gpt4 in combination with other tools to achieve adversarial goals
  - example: find replacements for checmicals

## 2.11 Economic Impacts
- may lead to automation of certain jobs
- previous models more augmentation of human workers
- historically automation leads to inequality, disparate impacts on different groups

## 2.12 Acceleration
- risk of racing dynamics leading to decline in safety standards
- 6 months spent on safety research, risk assessment and iteration prior to launch

## 2.13 Overreliance
- more believable on wrong facts than previous gpt models
- previous mitigations: documentation and hedging language within the model
- developers using gpt4 should clearly state capabilities and limitations
- better refusal -> user should not disregard refusal

# 3 Deployment Preparation
## 3.1 Model Mitigations
- filter dataset for inappropriate erotic text content
- usage of rlh. Trained RM on what labelers prefer, use model to fine-tune GPT4 SFT (PPO algorithm) -> refuse certain topics

- still undesired behavoirs for instructions not presented to labelers
- rulebased reward models: gpt4 classifier
- rewrite edgecase prompts into boundary prompts
- improve robustness by ranking data from labelers trying to circumvent

# 4 System Safety
## 4.1 Usage Policies and Monitoring
- suite of machine learning and rule-based classifier detections
- if detected multiple times, warning, temporary suspension, permanent suspension

## 4.2 Content Classifier Development
- moderation classifiers
- use of gpt4 to accelerate development
  - create robust, unambiguous taxonomies
    - classifying test sets
  - labeling of training data

# 5 Conclusion and Next Steps
- still vulnerable for adversarial attacks, exploits and jailbreaks
- adopt layers of mitigation throughout the model system
- build evaluations, mitigations and approach deployment with real-world usage
- ensure that safety assessments cover emergent risks
- be cognizant of, and plan for, capability jumps "in the wild"