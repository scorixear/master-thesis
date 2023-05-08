# Paper
```bibtex
@misc{openai2023gpt4,
      title={GPT-4 Technical Report}, 
      author={OpenAI},
      year={2023},
      eprint={2303.08774},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

# 1 Introduction
- processes image and text
- produces text
- evaluated on variety of exams
  - bar exam gpt4 achieves top 10%
- outperforms llms and state-of-the-art systems

- not fully reliable, suffers hallucinations
- limited context window
- does not learn from experience

- system card descrbibes vulnerabilities, safety concerns, inverventions done

# 2 Scope and Limitations of this Technical Report
- pretrained on internet and third-party providers
- fine-tuned using reinformcement learning using humand feedback

# 3 Predictable Scaling
- not reasonable to do model-specific tuning
- predict erformance of optimization merthods from smaller models (1,000x - 10,000x)

## 3.1 Loss Prediction
- fitted scaling law predicted loss
- $L(C) = aC^b + c$

## 3.2 Scaling of Capabilities on HumanEval
- pass rate on HumanEval dataset (ability to synthesize python functions)
  - extrapolating models trained with 1000 less compute
- results prediciton were accurate

- inverse scaling prize and hindsight neglect problems with prediction

## 4 Capabilities
- not specifically trained on exams
- for problems seen by model, ran variant of exam with problems removed
- success in exam stems primarily from pretraining process and not rlhf
- evaluated base gpt4 with traditional benchmarks

- most benchmarks for english, translate mmlu benchmark to other languages
- prompts to gpt4 peferred over chatgpt 70.2% judged by human labelers

## 4.1 Visual Inputs
- arbitrary interlaced text and images as input possible
- similar performance to text only input

# 5 Limitations
- not fully reliable
- but still better accuracy and reduced hallucinations over a number of evaluation topics
- RLHF results in large improvements agains TruthfulQA benchmark
- resists common sayings (that are wrong), but can miss sublte details

- lacks knowledge beyond september 2021
- sometimes makes simple reasoning errors
- can be overly gullible to false statements from users
- can fail at hard problems (such as introducing security vulnerabilities into code)

- can be confidently wrong in predicitons, not double-checking their answers
- but highly alligned, confidence of model matches probability of being correct
- post-training reduces calibration

# 6 Risk & mitigations
- usage of domain experts for adversarial testing and red-teaming
- model can generate undesirable content from unsafe inputs
- model can be overly cautious on safe inputs
  - use safety-relevant rlhf training prompts and rule-based reward models
  - rule-based = zero shot gpt4 classifiers
  - three inputs: prompt, answer from policy model, human-written rubric
  - rubrics are
    - refusal in desired style
    - resual in undesired style
    - containing disallowed content
    - safe non-refusal response
  - reward model if refusing requests/non refusing requests

- tendency to respond to disallowed content reduced by 82%
- responses to sensitive requests 29%
- produces toxic generation 0.73% of time