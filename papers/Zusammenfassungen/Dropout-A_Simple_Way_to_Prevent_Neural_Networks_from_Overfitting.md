# Paper
```bibtex
@article{JMLR:v15:srivastava14a,
  author  = {Nitish Srivastava and Geoffrey Hinton and Alex Krizhevsky and Ilya Sutskever and Ruslan Salakhutdinov},
  title   = {Dropout: A Simple Way to Prevent Neural Networks from Overfitting},
  journal = {Journal of Machine Learning Research},
  year    = {2014},
  volume  = {15},
  number  = {56},
  pages   = {1929--1958},
  url     = {http://jmlr.org/papers/v15/srivastava14a.html}
}
```

<style>
    p,li {
        white-space: initial;
    }
</style>

# 1 Introduction
- sampling noise existent (in training set, but not in test dataset)
- leads to overfitting, solutions
  - stopping as soon as performance on validation gets worse
  - introducin weight penalities
  - L1 and L2 regularization
  - soft weight sharing

- best approach with unlimited computation
  - average predictions of all possible settings of parameters
  - weighting each setting by its posterior probability
- approximate this by using equally weighted geometric mean

- model combination most effective when models are different
  - different architectures
  - trained on different data
- problems for big networks
  - computationally too expensive
  - not enough training data existent

- solution: dropout
- prevents overfitting
- provised approximately combinig exponentially many different neuronal network architectures efficiently
- drop out hidden and visible units = temporarily removing from network (including connections)
- choice is random, independent from other units, 0.5 seems close to optimal
- for input units, optimal closer to 1

- = sampling thinned network
- $2^n$ thinned networks possible, total number of parameters in $O(n^2)$
- at test time, use single neuronal network without dropout
- output of units are scaled by probability
- leads to lower generalization error

# 2 Motivation
- comes from sexual reproduction
- asexual reproduction: offspring is slightly modified copy of parent
- sexual reproduction: offspring is combination of two parents, breaks of co-adaptations
- but: makes them more robust, since can work with set or other random genes
- similarity
  - neuronal network hidden unit must learn to work with randomly chosen sample of other units
  - makes unit more robust, drives it to learn more robust features, without relying on other units
  - robust to dropout = replication of units
  - but poor solution to the problem

# 3 Related Work
- interpreted as adding noise to hidden layers
  - Denoising Autoencoders
- stochastic regularization technique

# 4 Model Description
- L hidden layers, $l$ index of hidden layer
- $z^{(l)}$ input vector into layer $l$
- $y^{(l)}$ output vector from layer $l$; $y^{(0)} = x$ = input
- $W^{(l)}$ weight matrix for layer $l$
- $b^{(l)}$ bias vector for layer $l$
- $f$ activation function; e.g. $f(x) = 1/(1+exp(-x))$ for sigmoid

- $z_i^{(l+1)} = w_i^{(l+1)}y^{(l)} + b_i^{(l+1)}$  
- $y_i^{(l+1)} = f(z_i^{(l+1)})$

- for dropout, new formulas
- $r_j^{(l)} \thicksim \text{Bernoulli}(p)$
- $\tilde{y}^{(l)} = r^{(l)} * y^{(l)}$
- $z_i^{(l+1)} = w_i^{(l+1)}\tilde{y}^{(l)} + b_i^{(l+1)}$
- $y_i^{(l+1)} = f(z_i^{(l+1)})$ 

# 5 Learning Dropout Nets
## 5.1 Backpropagation
- using stochastic gradient descent
- for each mini-batch, sample thinned network
- forward and backward done for thinned network
- norm of incoming weight upper bounded by fixed constant = max-norm regularization
- using max-norm regularization, large decaying learning rates, high momentum results in significant boost over only dropout

## 5.2 Unsupervised Pretraining
- used for fine-tuning
- weights scaled up by factor 1/p
- with smaller learning rates, no wipeout of prelearned data

# 6 Experimental Results
- MNIST, TIMIT, CIFAR-10, CIFAR-100, SVHN, ImageNet, Reuters-RCV1, Alternative Splicing

## 6.1 Results on ImageData SEts
- better performance, no early stopping required with bigger networks for MNIST
- better performance for google street view
- same for CIFAR
- same for ImageNet, TIMIT, TextDataSet
- dropout better than other models, but not better than bayesian neural networks

# 7 Salient Features
- hidden layers may fix problems from other layers
- co-adaptation, solved by dropout
- better effect on feature extraction
- more sparse activation
- results of p around 0.5 best
- sweet spot of p for dataset size
- weight scaling is in standard deviation of monte carlo approximation

# 8 Dropout Restricted Boltzman Machines
- not important

# 9 Marginalizing Dropout
- deterministic approach of dropping out units

the rest is not relevant
