# Paper
```bibtex
@INPROCEEDINGS{7780459,
  author={He, Kaiming and Zhang, Xiangyu and Ren, Shaoqing and Sun, Jian},
  booktitle={2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR)}, 
  title={Deep Residual Learning for Image Recognition}, 
  year={2016},
  volume={},
  number={},
  pages={770-778},
  doi={10.1109/CVPR.2016.90}}
```

# 1 Introduction
- levels of features enriched by number of stacked layers
- problems: vanishing/exploding gradients
  - addressed by normalied initialization
  - intermediate normalization layers
- degradation problem: accuracy gets saturated and then degrades rapidly
  - not caused by overfitting
  - not solved by adding more layers with identity mapping
  - proposed solution residual learning
- feed-foward networks with shortcut connections
  - skipping one or more layers
  - performs identity mapping
  - outputs added to stacked layer outputs
  - network can be trained end-to-end by SGD with backpropagation

# 2 Related Work
Residual Representation
Shortcut Connections

# 3 Deep Residual Learning
## 3.1 Residual Learning
- $H(x)$ = underlying mapping = few stacked layers
- $x$ = input into first layer
- $H(X) - x$ = residual function
- $F(x) = H(x) - x$ = layers should predict residuals
- Original Function $F(x) + x$

## 3.2 Identity Mapping by Shortcuts
- adopt to residual learning for every few stacked layers
- $y = F(X, \{W_i\})+x$ = building block
- $x, y$ = input and output
- $F(X, \{W_i\})$ = residual function to be learned
  - eg. $F = W_2\sigma(W_1x)$
  - $\sigma$ = ReLU
  - bias ommited for simplification
- $F + x$ achieved by adding shortcut connection, elementwise addition
- if input and output not same size, apply linear projection to $x$
- no observed advantages for single layers

## 3.3 Network Architectures
- Plain Network
  - not important
- Residual Network
  - also not important
## 3.4 Implementation
- random horizontal flipping
- batch normalization after each convolution and before activation

# 4 Experiments
## 4.1 ImageNet Classification
- 1000 classes
- 1.28m training images
- 50k validation images
- Plain Network
  - deep plain network has higher validation error than shallow
  - due to degradation problem
  - not due to vanishing gradients due to batch normalization
  - conjecture: exponentially low convergence rates
- Residual Networks
  - situation reversed
  - deep residual network has lower training error than deep plain network
  - shallow residual network is comparable to shallow plain network
- Identity vs Projection Shortcuts
  - zero-padding for increasing dimensions, projection shortcuts for increasing dimensions, all shortcuts are projection
  - considerably better than plain
  - C marginally better than B slightly better than A
  - not essential for addressing degradation problem
- Deeper Bottleneck Architectures
  - more layers result in better accuracy, no degradation problem found

## 4.2 CIFAR-10 and Analysis
- deep plain networks suffer from increased depth
- residual networks do not suffer from increased depth but benefit
Analysis of Layer Responses
- response strength of residual functions
- generally smaller responses than plain networks
- residual function generally closer to zero
- with more layers, individual layers modify signal less
Exploring Over 1000 Layers
- no optimization difficulty
- very low training error
- but testing result worse than 110 alyer network
- argue that this is because of overfitting