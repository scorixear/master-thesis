```python
{
    # enables training with floating point 16 weights
    "fp16": {
        # enabled if trainer args are enabled
        "enabled": "auto",
        # defined the scaling up of the loss value
        # to improve better precision
        # 0 = dynamic scaling, starting at 65536 and decreasing if overlow happens
        # to a minimum of 1
        "loss_scale": 0,
        # the window over which to raise/lower the dynamic loss scale value
        "loss_scale_window": 1000,
        # defines the starting loss scale (2^16 here)
        "initial_scale_power": 16,
        # represent the delay shift in dynamic loss scaling
        "hysteresis": 2,
        # defines the minimum loss scale. 1 is the minimum value to be set here
        "min_loss_scale": 1
    },

    "optimizer": {
        # The optimizer used during training
        # must fit the defined optimizer in the trainer args
        "type": "AdamW",
        # configured by trainer args
        "params": {
            # learning rate
            "lr": "auto",
            # beta values (0.9, 0.95 used in llama paper)
            "betas": "auto",
            # epsilon value (1e-8 used in llama paper)
            "eps": "auto",
            # weight decay (0.01 used in llama paper)
            "weight_decay": "auto"
        }
    },
    # used for warmup steps
    "scheduler": {
        "type": "WarmupLR",
        # configured by training args
        "params": {
            # start learning rate
            "warmup_min_lr": "auto",
            # end learning rate
            "warmup_max_lr": "auto",
            # number of steps from min to max
            "warmup_num_steps": "auto"
        }
    },
    # example stage 0
    # no additional configuration needed
    "zero_optimization": {
        "stage": 0,
    }

    # example stage 1
    "zero_optimization": {
        "stage": 1,
        # number of element reduced at a time
        # Limits memory requirements for large models
        "recude_bucket_size": 5e8
    }

    # example stage 2
    "zero_optimization": {
        "stage": 2,
        # copies gradients to contiguous buffer
        # avoids memory fragmentation during backward pass
        "contiguous_gradients": True,
        # Attempts to overlap reduction of gradients with backward computation
        "overlap_comm": True,
        # Use reduce / reduce scatter instead of allreduce for gradient average
        "reduce_scatter": True,
        "reduce_bucket_size": 5e8,
        
        # if enabled, will use gather all updated parameters from gpus
        # if not, uses series of broadcast collectives
        "allgather_partitions": True,
        # number of elements algathered at a time
        # will use 5e8 * 2Bytes * 2 * 4.5 = 9GB memory
        # change to 2e8 if OOM error
        "allgather_bucket_size": 5e8,
        # enables offload optimizer state to CPU ur NVMe and optimizer computation to CPU
        # frees up GPU memory
        "offload_optimizer": {
            # device to offload to
            "device": "cpu",
            # Offload to page-locked CPU memory
            # can boost throughput at the cost of extra memory overhead
            "pin_memory": True
        }
    },

    # example stage 3
    "zero_optimization": {
        "stage": 3,
        "contiguous_gradients": True,
        # Maximum number of parameters resident per GPU before releasing
        # Smaller values use les memory, but require more communication
        "stage3_max_live_parameters": 1e9,
        # Do not release parameter if reused within this threshold of parameters
        # Smaller values use less memory, but require more communication
        "stage3_max_reuse_distance": 1e9,
        # Size of fixed buffer for prefetching parameters
        # Smaller values use less memory, but increase stalls due to communication
        "stage3_prefetch_bucket_size": 1e7,
        # Do not partition parameters smaller than this threshold
        # Smaller values use less memory, but increase greatly communication
        "stage3_param_persistence_threshold": 1e5,
        "reduce_bucket_size": 1e7,
        "sub_group_size": 1e9,
        "offload_optimizer": {
            "device": "cpu",
            "pin_memory": True
        },
        # enables offloading of model parameters to CPU or NVMe
        # Frees up GPU memory for larger models / batch sizes
        "offload_param": {
            "device": "cpu",
            "pin_memory": True
        }
    }

    # enables gradient clipping
    "gradient_clipping": 1.0,
    # print progres report every N training steps
    "steps_per_print": 2000,
    # enables timing of latency for forward/backward/update training phases
    "wall_clock_breakdown": False
}
```