# Paper
```bibtex
@InProceedings{pmlr-v97-houlsby19a,
  title = 	 {Parameter-Efficient Transfer Learning for {NLP}},
  author =       {Houlsby, Neil and Giurgiu, Andrei and Jastrzebski, Stanislaw and Morrone, Bruna and De Laroussilhe, Quentin and Gesmundo, Andrea and Attariyan, Mona and Gelly, Sylvain},
  booktitle = 	 {Proceedings of the 36th International Conference on Machine Learning},
  pages = 	 {2790--2799},
  year = 	 {2019},
  editor = 	 {Chaudhuri, Kamalika and Salakhutdinov, Ruslan},
  volume = 	 {97},
  series = 	 {Proceedings of Machine Learning Research},
  month = 	 {09--15 Jun},
  publisher =    {PMLR},
  url = 	 {https://proceedings.mlr.press/v97/houlsby19a.html},
}
```

# Abstract
- finetuning pretrained models is efficient transfer mechanism
- fine-tuning for many downstream tasks is inefficient (models for each task)
- adapter modules add few trainable parameters per task
- new tasks added without revisiting previous ones
- demonstrate by transfering BERT to 26 diverse text classification tasks
- attain 0.4% performance, adding 3.6% parameters (finetuning 100% paramerters)

# 1 Introduction
- bert achieved sota for text classification and extractive question answering

- goal: model that performs well on tasks, but without training entire new models for every new task
- compact models: solve many tasks using small number of additional parameters
- extensible models: trained incrementally to solve new tasks without forgetting previous ones

- most common transfer learning techniques
  - feature based transfer
    - pre-training real-valued embedding vectors
    - fed to custom downstream models
  - fine-tuning
    - copying weights from pretrained
    - tuning on downstream task
    - often better performance than feature-based
- alternative
  - adapter modules
  - requires two orders of magnitude fewer parameters with similar performance

- adapter = new modules between layers
- given nn with parameters $w$: $\phi_w(x)$
- feature based with new function $\chi_v$: $\chi_v(\phi_w(x))$
- fine-tuning = adjust all $w$
- adapter tuning: new function $\psi_{w,v}(x)$
  - initial paramters $v_0$ are set to be $\psi_{w,v_0}(x) \approx \phi_w(x)$
  - only $v$ are tuned
  - if $|v| \ll |w|$, then model requires $\sim |w|$ parameters for many tasks

- adapter tuning relates to multi-task, continual learning
- multi-task requires simultaneous access to all tasks
- continual learning forgets previous tasks afer re-training
- since parameters are frozen, memory gets not lost with adapters

- bottleneck architecture
- similar results on 17 public text datsets

# 2 Adapter tuning for NLP
- three key properties
  - attain good performance
  - permit training on tasks sequentially
  - add small number of parameters per task

- injecting new adapter layers, intialized randomnly
- train only new parameters

- near identity initialization
- adapter modules need to be small compared to original layers
- adapter modules may be ignored if not required
- if initialization fails to be identity, training fails

## 2.1 Instantiation for Transformer Networks
- simple design that attains good performance
- more complex designs perform as well as any other

- sub-layers attention and feed-forward followed by adapter layer
- then skip-connection, then layer normalization

- limit parameters, project d-dimensional feature to m smaller dimension, apply nonlinearity, then project back to d
- added parameters: $2md + d + m$
- if $m \ll d$, then in practice around 0.5 - 8% parameters
- skip-connection in adapter, if parameters initialized to near-zero, module approximates identity function

- also retrain new layer normalization parameters per task
- training only layer normalization is insufficient

# 3 Experiments
- glue benchmark: 0.4% performance, 3% parameters
- confirm with  17 public classification tasks and SQuAD question answering

## 3.1 Experimental Settings
- base model BERT
- first token is classification token
- attach linear layer to embedding of this token to predict class label

## 3.2 GLUE Benchmark
- $BERT_{LARGE}$, 24 layers, 330m parameters
- parameter sweep (3*10^-5, 10^-4, 10^-3)
- epochs (3, 20)
- fixed adapter size, best size for tasks (8,64,256)
- re-run 5 times, select best model (training instability)
- MNLI 256 adapter size, RTE 8 adapter size
- always restricting to 64 results in small decrease in accuracy
- fine-tuning requires 9x parameters, adapter require 1.3x

# 3.3 Additional Classification Tasks
- 900 - 330k training examples
- 2 - 157 classes
- batch size 32
- 20, 50, 100 epochs
- fine-tuning with sweep of n top layers (BERT_base with 12 layers)

# 3.4 Parameter/Performance Trade-off
- on glue, performance decreases dramatically with fewer layers fine-tuned
- additional tasks performance decays much less
- similar results for MNLI and CoLA

# 3.5 SQuAD Extractive Question Answering
- question and wikipedia paragraph
- 64 adapter size best f1 score

## 3.6 Analysis and Discussion
- ablation by removing trained adapters and reevaluating
- removing single layers small impact
- all adapters removed, significantly perfomance drop
- lower layers smaler impact than higher layers
  - lower layers for general lower-level features across tasks
- adapter robust for standard deviation of 10^-2
- performance degrades if initialization is too large
- stable performance across few orders of magnitude
- extensions to adapter architecture do not yield significant boost

# 4 Related Work
- 