```python
{
    "fp16": {
        # enabled if trainer args are enabled
        "enabled": "auto",
        # figure out values here!!!
        "loss_scale": 0,
        "loss_scale_window": 1000,
        "initial_scale_power": 16,
        "hysteresis": 2,
        "min_loss_scale": 1
    },

    "optimizer": {
        # check if correct optimizer is used
        "type": "AdamW",
        "params": {
            # configured by trainer args
            "lr": "auto",
            "betas": "auto",
            "eps": "auto",
            "weight_decay": "auto"
        }
    },

    "scheduler": { # possibly no warmup here
        "type": "WarmupLR",
        # otherwise configured by trainer args
        "params": {
            "warmup_min_lr": "auto",
            "warmup_max_lr": "auto",
            "warmup_num_steps": "auto"
        }
    },
    # stage 2 for best performance
    "zero_optimization": {
        "stage": 2,
        # CHECK THE VALUES HERE
        "allgather_partitions": True,
        # will use 5e8 * 2Bytes * 2 * 4.5 = 9GB memory
        # change to 2e8 if OOM error
        "allgather_bucket_size": 5e8,
        "overlap_comm": True,
        "reduce_scatter": True,
        # this was calculated from model_hidden_size
        "reduce_bucket_size": 5e8,
        # what is this?
        "contiguous_gradients": True,
        
    },
    # as by the paper
    "gradient_clipping": 1.0,
    # debug output
    "steps_per_print": 2000,
    "wall_clock_breakdown": False
}
```