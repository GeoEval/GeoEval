#!/bin/bash
from transformers import AutoModelForCausalLM, AutoTokenizer
import logging
import torch

# Configure the logger
logging.basicConfig(filename='check.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



def check_model_complete(model_name, model_path, except_dict):
    try:
        model = AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path=model_path, device_map="auto", trust_remote_code=True).cuda()
        model.eval()
        tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=model_path, trust_remote_code=True)
    except Exception as e:
        logger.error(f"Error loading model {model_name}: {str(e)}")
        except_dict[model_name] = model_path

# List of Hugging Face models
general_models = [
    "lmsys/vicuna-7b-v1.5",
    "lmsys/vicuna-13b-v1.5",
    "EleutherAI/pythia-1b",
    "EleutherAI/pythia-2.8b",
    "EleutherAI/pythia-6.9b",
    "EleutherAI/pythia-12b",
    "internlm/internlm-7b",
    "internlm/internlm-20b",
    "Qwen/Qwen-7B",
    "Qwen/Qwen-14B",
    "baichuan-inc/Baichuan2-7B-Base",
    "baichuan-inc/Baichuan2-13B-Base",
    "meta-llama/Llama-2-7b-hf"
]

# List of Hugging Face models for Math
math_models = [
    "facebook/galactica-1.3b",
    "facebook/galactica-6.7b",
    "EleutherAI/llemma_7b",
    "meta-math/MetaMath-Mistral-7B",
    "meta-math/MetaMath-Llemma-7B",
    "meta-math/MetaMath-7B-V1.0",
    "WizardLM/WizardMath-13B-V1.0",
    "WizardLM/WizardMath-7B-V1.0",
    "TIGER-Lab/MAmmoTH-7B",
    "TIGER-Lab/MAmmoTH-13B",
]

# code_model
code_models = [
    "codellama/CodeLlama-7b-hf",
]

# vlm_model
vlm_model = [
    "THUDM/visualglm-6b",
    "cooelf/mm-cot",
    "liuhaotian/llava-v1.5-7b",
    "winglian/llama-adapter-7b",
    "Qwen/Qwen-VL"
]

file_paths = [
    "/home/kas/checkpoint/LayoutNUWA/download_llama/EleutherAI/llemma_7b",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/EleutherAI/pythia-12b",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/EleutherAI/pythia-1b",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/EleutherAI/pythia-2.8b",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/EleutherAI/pythia-6.9b",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/Qwen/Qwen-14B",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/Qwen/Qwen-7B",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/Qwen/Qwen-VL",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/THUDM/visualglm-6b",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/TIGER-Lab/MAmmoTH-13B",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/TIGER-Lab/MAmmoTH-7B",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/WizardLM/WizardMath-13B-V1.0",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/WizardLM/WizardMath-7B-V1.0",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/baichuan-inc/Baichuan2-13B-Base",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/baichuan-inc/Baichuan2-7B-Base",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/codellama/CodeLlama-7b-hf",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/cooelf/mm-cot",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/facebook/galactica-1.3b",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/facebook/galactica-6.7b",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/internlm/internlm-20b",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/internlm/internlm-7b",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/liuhaotian/llava-v1.5-7b",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/lmsys/vicuna-13b-v1.5",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/lmsys/vicuna-7b-v1.5",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/meta-llama/Llama-2-7b/hf",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/meta-math/MetaMath-7B-V1.0",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/meta-math/MetaMath-Llemma-7B",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/meta-math/MetaMath-Mistral-7B",
    "/home/kas/checkpoint/LayoutNUWA/download_llama/winglian/llama-adapter-7b"
]

general_models_dict = {model: '' for model in general_models}
math_models_dict = {model: '' for model in math_models}

model_dict = {}
model_dict.update(general_models_dict)
model_dict.update(math_models_dict)


for model_name in model_dict:
    for file_path in file_paths:
        if file_path.endswith(model_name):
            model_dict[model_name] = file_path
            break

except_dict = {}
for model_name, model_path in model_dict.items():
    torch.cuda.empty_cache()
    check_model_complete(model_name, model_path, except_dict)
