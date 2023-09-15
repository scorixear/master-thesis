import math
import os
import sys
import logging
from dataclasses import dataclass, field
from typing import Optional

import torch

from datasets import load_dataset
import evaluate

import transformers
from transformers import (
    Trainer,
    TrainingArguments,
    default_data_collator,
    is_torch_tpu_available,
)
from transformers import (
    LlamaForCausalLM,
    LlamaTokenizer,
    LlamaConfig,
    HfArgumentParser,
    set_seed,
)
from transformers.trainer_utils import get_last_checkpoint
from transformers.utils import check_min_version
from transformers.testing_utils import CaptureLogger
from transformers.utils.versions import require_version

# check if version is on or after 4.32.0.dev0
check_min_version("4.32.0.dev0")
# check if datasets version is on or after 1.8.0
require_version(
    "datasets>=1.8.0",
    "To fix: pip install -r examples/pytorch/language-modeling/requirements.txt",
)

# initialize logger
logger = logging.getLogger(__name__)


# define arguments for this script
@dataclass
class ModelArguments:
    """
    Arguments pertaining to which model/config/tokenizer we are going to train from.
    """

    model_path: str = field(metadata={"help": "Path to pretrained model"})
    config_name: Optional[str] = field(
        default=None,
        metadata={"help": "Pretrained config path if not the same as model_name"},
    )
    tokenizer_name: Optional[str] = field(
        default=None,
        metadata={"help": "Pretrained tokenizer path if not the same as model_name"},
    )
    use_fast_tokenizer: bool = field(
        default=True,
        metadata={
            "help": "Whether to use one of the fast tokenizer (backed by the tokenizers library) or not."
        },
    )
    torch_dtype: Optional[str] = field(
        default=None,
        metadata={
            "help": (
                "Override the default `torch.dtype` and load the model under this dtype. \
                    If `auto` is passed, the "
                "dtype will be automatically derived from the model's weights."
            ),
            "choices": ["auto", "bfloat16", "float16", "float32"],
        },
    )
    low_cpu_mem_usage: bool = field(
        default=False,
        metadata={
            "help": (
                "It is an option to create the model as an empty shell, \
                    then only materialize its parameters when the pretrained weights are loaded."
                "set True will benefit LLM loading time and RAM consumption."
            )
        },
    )


@dataclass
class DataTrainingArguments:
    """
    Arguments pertaining to what data we are going to input our model for training and eval.
    """

    train_file: str = field(metadata={"help": "Path for training file"})
    max_train_samples: Optional[int] = field(
        default=None,
        metadata={
            "help": (
                "For debugging purposes or quicker training, \
                    truncate the number of training examples to this "
                "value if set."
            )
        },
    )
    max_eval_samples: Optional[int] = field(
        default=None,
        metadata={
            "help": (
                "For debugging purposes or quicker training, \
                    truncate the number of evaluation examples to this "
                "value if set."
            )
        },
    )
    block_size: Optional[int] = field(
        default=None,
        metadata={
            "help": (
                "Optional input sequence length after tokenization. "
                "The training dataset will be truncated in block of this size for training. "
                "Default to the model max input length for \
                    single sentence inputs (take into account special tokens)."
            )
        },
    )
    validation_split_percentage: Optional[int] = field(
        default=5,
        metadata={
            "help": "The percentage of the train set used as \
                validation set in case there's no validation split"
        },
    )
    preprocessing_num_workers: Optional[int] = field(
        default=None,
        metadata={"help": "The number of processes to use for the preprocessing."},
    )
    keep_linebreaks: bool = field(
        default=True,
        metadata={"help": "Whether to keep line breaks when using TXT files or not."},
    )


def main():
    # load in script arguments
    parser = HfArgumentParser(
        (ModelArguments, DataTrainingArguments, TrainingArguments)
    )  # type: ignore

    # If we pass only one argument to the script and it's the path to a json file,
    # let's parse it to get our arguments.
    if len(sys.argv) == 2 and sys.argv[1].endswith(".json"):
        model_args, data_args, training_args = parser.parse_json_file(
            json_file=os.path.abspath(sys.argv[1])
        )
    # otherwise parse into dataclasses
    else:
        model_args, data_args, training_args = parser.parse_args_into_dataclasses()

    # setup logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # set verbosity of logging to info
    if training_args.should_log:
        transformers.utils.logging.set_verbosity_info()

    log_level = training_args.get_process_log_level()
    logger.setLevel(log_level)
    transformers.utils.logging.set_verbosity(log_level)
    transformers.utils.logging.enable_default_handler()
    transformers.utils.logging.enable_explicit_format()

    # Log on each process the small summary of used args
    logger.warning(
        f"Process rank: {training_args.local_rank}, \
            device: {training_args.device}, n_gpu: {training_args.n_gpu}"
        + f" distributed training: {bool(training_args.local_rank != -1)}, \
            16-bits training: {training_args.fp16}"
    )
    logger.info(f"Training/evaluation parameters {training_args}")

    # Detecting last checkpoint.
    last_checkpoint = None
    # if output dir is already existent
    # and we do train and not overwrite the output dir
    if (
        os.path.isdir(training_args.output_dir)
        and training_args.do_train
        and not training_args.overwrite_output_dir
    ):
        # get the last checkpoint
        last_checkpoint = get_last_checkpoint(training_args.output_dir)
        # if checkpoint cannot be loaded, but something is in the output dir
        if last_checkpoint is None and len(os.listdir(training_args.output_dir)) > 0:
            # print error as we cannot overwrite output dir
            raise ValueError(
                f"Output directory ({training_args.output_dir}) already exists and is not empty. \
                    Use --overwrite_output_dir to overcome."
            )
        # if checkpoint can be loaded and training args allow resuming from checkpoint
        if last_checkpoint is not None and training_args.resume_from_checkpoint is None:
            logger.info(
                f"Checkpoint detected, resuming training at {last_checkpoint}. \
                    To avoid this behavior, change "
                "the `--output_dir` or add `--overwrite_output_dir` to train from scratch."
            )

    # set seed before initializing model
    set_seed(training_args.seed)

    # load dataset
    # load_dataset() ensures only one process can concurrently load the dataset
    data_files = {}
    dataset_args = {}
    data_files["train"] = data_args.train_file
    # as we work with text files only, the extension is set to "text"
    extension = "text"
    dataset_args["keep_linebreaks"] = data_args.keep_linebreaks
    # first load of full dataset
    raw_datasets = load_dataset(
        extension,
        data_files=data_files,
        **dataset_args,
    )
    # split into validation and training
    raw_datasets["validation"] = load_dataset(  # type: ignore
        extension,
        data_files=data_files,
        split=f"train[:{data_args.validation_split_percentage}%]",
        **dataset_args,
    )
    raw_datasets["train"] = load_dataset(  # type: ignore
        extension,
        data_files=data_files,
        split=f"train[{data_args.validation_split_percentage}%:]",
        **dataset_args,
    )

    # load pretrained model and tokenizer
    # .from_pretrained ensures only one process can concurrently load the model & vocab
    config = LlamaConfig.from_pretrained(model_args.model_path)
    tokenizer = LlamaTokenizer.from_pretrained(
        model_args.model_path, use_fast=model_args.use_fast_tokenizer
    )

    # detect defined dtype
    # for llama this is fp16
    torch_dtype = (
        model_args.torch_dtype
        if model_args.torch_dtype in ["auto", None]
        else getattr(torch, model_args.torch_dtype)
    )

    # and load the model
    model = LlamaForCausalLM.from_pretrained(
        model_args.model_path,
        config=config,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=model_args.low_cpu_mem_usage,
    )

    # resize embeddings if necessary to avoid index errors
    embedding_size = model.get_input_embeddings().weight.shape[0]  # type: ignore
    if len(tokenizer) > embedding_size:
        model.resize_token_embeddings(len(tokenizer))  # type: ignore

    # preprocess dataset
    # if we train, extract the features
    if training_args.do_train:
        column_names = list(raw_datasets["train"].features)  # type: ignore
    # otherwise extract the features from the validation set
    else:
        column_names = list(raw_datasets["validation"].features)  # type: ignore
    # if the column names contain "text", use this as text column name
    text_column_name = "text" if "text" in column_names else column_names[0]

    # get tokenizer logging
    tok_logger = transformers.utils.logging.get_logger(
        "transformers.tokenization_utils_base"
    )

    # define inner function for tokenization
    def tokenize_function(examples):
        # and add capturelogger to catch warnings
        with CaptureLogger(tok_logger) as cl:
            output = tokenizer(examples[text_column_name])
        # this warning is irrelevant for us
        # we catch it and resume training
        if "Token indices sequence length is longer than the" in cl.out:
            tok_logger.warning(
                "^^^^^^^^^^^^^^^^^^^^^^^^ Please ignore the warning above - \
                    this long input will be chunked into smaller bits"
                " before being passed to the model."
            )
        return output

    # tokenize the datasets
    with training_args.main_process_first(desc="dataset map tokenization"):
        tokenized_datasets = raw_datasets.map(
            tokenize_function,
            batched=True,
            num_proc=data_args.preprocessing_num_workers,  # type: ignore
            remove_columns=column_names,
            desc="Running tokenizer on dataset",  # type: ignore
        )
    # if block_size is not set
    if data_args.block_size is None:
        # get the maximum block size from the tokenizer
        # for llama this is 1024
        block_size = tokenizer.model_max_length
        # if the block size is above 1024
        # we limit it
        if block_size > 1024:
            logger.warning(
                "The chosen tokenizer supports a `model_max_length` \
                    that is longer than the default `block_size` value"
                " of 1024. If you would like to use a longer `block_size` up to \
                    `tokenizer.model_max_length` you can"
                " override this default with `--block_size xxx`."
            )
            block_size = 1024
    # if block_size is set
    else:
        # if block_size is larger than the maximum block_size for the model
        # we limit it
        if data_args.block_size > tokenizer.model_max_length:
            logger.warning(
                f"The block_size passed ({data_args.block_size}) \
                    is larger than the maximum length for the model"
                f"({tokenizer.model_max_length}). Using block_size={tokenizer.model_max_length}."
            )
        block_size = min(data_args.block_size, tokenizer.model_max_length)

    # Main data processing function that will concatenate
    # all texts from our dataset and generate chunks of block_size.
    def group_texts(examples):
        # concatenate all texts
        concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
        # get total length
        total_length = len(concatenated_examples[list(examples.keys())[0]])
        # if total_length < block_size, excludes batch an returns empty dict
        total_length = (total_length // block_size) * block_size  # type: ignore
        # split by chunk of max_len
        result = {
            key: [
                value[i : i + block_size]
                for i in range(0, total_length, block_size)  # type: ignore
            ]  # type: ignore
            for key, value in concatenated_examples.items()
        }
        result["labels"] = result["input_ids"].copy()
        return result

    # apply grouping into block_size to the dataset
    with training_args.main_process_first(desc="dataset map group_texts"):
        lm_datasets = tokenized_datasets.map(
            group_texts,
            batched=True,
            num_proc=data_args.preprocessing_num_workers,
            desc=f"Grouping texts in chunks of {block_size}",
        )

    # if we train, get the train dataset
    if training_args.do_train:
        if "train" not in tokenized_datasets:
            raise ValueError("--do_train requires a train dataset")
        train_dataset = lm_datasets["train"]
        # if max_train_samples is set, limit the train dataset
        if data_args.max_train_samples is not None:
            max_train_samples = min(len(train_dataset), data_args.max_train_samples)
            train_dataset = train_dataset.select(range(max_train_samples))  # type: ignore
    # if we evaluate, get the validation dataset
    if training_args.do_eval:
        if "validation" not in tokenized_datasets:
            raise ValueError("--do_eval requires a validation dataset")
        eval_dataset = lm_datasets["validation"]
        # if max_eval_samples is set, limit the validation dataset
        if data_args.max_eval_samples is not None:
            max_eval_samples = min(len(eval_dataset), data_args.max_eval_samples)
            eval_dataset = eval_dataset.select(range(max_eval_samples))  # type: ignore

        # and define logits and metrics functions for evaluation
        def preprocess_logits_for_metrics(logits, labels):
            if isinstance(logits, tuple):
                logits = logits[0]
            return logits.argmax(dim=-1)

        metric = evaluate.load("accuracy")

        def compute_metrics(eval_preds):
            preds, labels = eval_preds
            labels = labels[:, 1:].reshape(-1)
            preds = preds[:, :-1].reshape(-1)
            return metric.compute(predictions=preds, references=labels)

    # Initialize our Trainer
    trainer = Trainer(
        model=model,  # type: ignore
        args=training_args,
        train_dataset=train_dataset if training_args.do_train else None,  # type: ignore
        eval_dataset=eval_dataset if training_args.do_eval else None,  # type: ignore
        tokenizer=tokenizer,
        data_collator=default_data_collator,
        compute_metrics=compute_metrics
        if training_args.do_eval and not is_torch_tpu_available()
        else None,  # type: ignore
        preprocess_logits_for_metrics=preprocess_logits_for_metrics
        if training_args.do_eval and not is_torch_tpu_available()
        else None,
    )

    # Training
    if training_args.do_train:
        # resume from checkpoint if possible
        checkpoint = None
        if training_args.resume_from_checkpoint is not None:
            checkpoint = training_args.resume_from_checkpoint
        elif last_checkpoint is not None:
            checkpoint = last_checkpoint
        # train the model
        train_result = trainer.train(resume_from_checkpoint=checkpoint)
        # and save to location specified in training_args
        trainer.save_model()

        # calculate metrics
        metrics = train_result.metrics
        max_train_samples = (
            data_args.max_train_samples
            if data_args.max_train_samples is not None
            else len(train_dataset)
        )
        metrics["train_samples"] = min(max_train_samples, len(train_dataset))
        # and log them as well as save them
        trainer.log_metrics("train", metrics)
        trainer.save_metrics("train", metrics)
        # save the trainer state for future resume
        trainer.save_state()

    # Evaluation
    if training_args.do_eval:
        logger.info("*** Evaluate ***")
        metrics = trainer.evaluate()
        max_eval_samples = (
            data_args.max_eval_samples
            if data_args.max_eval_samples is not None
            else len(eval_dataset)
        )
        metrics["eval_samples"] = min(max_eval_samples, len(eval_dataset))
        try:
            perplexity = math.exp(metrics["eval_loss"])
        except OverflowError:
            perplexity = float("inf")
        metrics["perplexity"] = perplexity

        trainer.log_metrics("eval", metrics)
        trainer.save_metrics("eval", metrics)


# used by xla_spawn when training on TPUs
def _mp_fn(index):
    main()


if __name__ == "__main__":
    main()
