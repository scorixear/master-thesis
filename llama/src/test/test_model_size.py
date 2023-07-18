from transformers import LlamaForCausalLM
from deepspeed.runtime.zero.stage_1_and_2 import estimate_zero2_model_states_mem_needs_all_live

model = LlamaForCausalLM.from_pretrained("llama_models/7B", local_files_only=True, low_cpu_mem_usage=True)
print("Model loaded")
estimate_zero2_model_states_mem_needs_all_live(model, num_gpus_per_node=4, num_nodes=1)