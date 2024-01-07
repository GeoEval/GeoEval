#!/usr/bin/env bash

# set -xe

MAIN_DIR=../..
YOUR_CREATE_DIR=codegen
CONFIG_YAML="sh_files/${YOUR_CREATE_DIR}/eval_config.yaml"

ARGS="--config_yaml ${CONFIG_YAML}"


# sh_files/llama2_7b_jiaxin_sample_script/../../run_llm_response.py",
# cpu
python ${MAIN_DIR}/run_llm_response.py ${ARGS}

# # single gpu
# CUDA_VISIBLE_DEVICES=0 python main.py ${ARGS}

# two gpus on one node
# torchrun --nproc_per_node=2 main.py ${ARGS}

# python -m torch.distributed.launch --nproc_per_node=2 --use_env main.py ${ARGS}