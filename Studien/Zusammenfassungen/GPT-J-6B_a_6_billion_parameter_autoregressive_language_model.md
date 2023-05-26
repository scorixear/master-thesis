# Paper
Blog Publish
https://arankomatsuzaki.wordpress.com/2021/06/04/gpt-j/

```bibtex	
@misc{mesh-transformer-jax,
  author = {Wang, Ben},
  title = {{Mesh-Transformer-JAX: Model-Parallel Implementation of Transformer Language Model with JAX}},
  howpublished = {\url{https://github.com/kingoflolz/mesh-transformer-jax}},
  year = 2021,
  month = May
}
```

# Summary
- JAX based Mesh Transformer LM
- nearly on-par with GPT-3 6.7B zero-shot

# Why does this project matter?
- best-performing publicly available transformer lm (zero shot performance)
- requires less person-hours due to jax + xmap + tpus

# Model design
- follow gpt3 design
- The Pile 800GB dataset
- no efficient attention used for simplicity (also no significantly improved throughput)
- attention head dimension is 256 (double of gpt3)
- rotary embedding for slightly better performance
- attention layer and feedforward layer in parallel for decreased communication

# Performance
- groughly on par with gpt-3
- throughput 125% of gpt-neo
- achieves 60% of theoretical maximum throughput
- 5 weeks training on TPU v3 256

Arithmetic
- can perform subtraction and addition perfectly

Theorme proving
- imitates style, but huge cap with human-level accuracy

Natural Language Understanding
- nucleus sampling hallucinates
- greedy sampling is concisely and reasonably

Coding
- doesn't know precise mechanism of attention