import os

from aitextgen.TokenDataset import TokenDataset
from aitextgen.tokenizers import train_tokenizer
from aitextgen.utils import GPT2ConfigCPU
from aitextgen import aitextgen


def main():
    file_name = "./books/bb_konrad.txt"
    #model_folder = "./aitextgen"
    tokenizer_file = "aitextgen.tokenizer.json"
    train_tokenizer(file_name)
    config = GPT2ConfigCPU()

    ai = aitextgen(tokenizer_file=tokenizer_file, config=config)

    data = TokenDataset(file_name, tokenizer_file=tokenizer_file, block_size=64)

    ai.train(data,
             batch_size=8,
             num_steps=50000,
             generate_every=5000,
             save_every=5000)
    ai.generate(prompt="Alfred Winter is")

if __name__ == "__main__":
    main()