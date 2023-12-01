#!/usr/bin/env bash

# set -xe

SH_FILES_DIR=./sh_files/
MAIN_DIR=../..

CONFIG_YAML=${SH_FILES_DIR}/"eval_config.yaml"

ARGS="--config_yam ${CONFIG_YAML}"

# cpu
python ${MAIN_DIR}/run_llm_response.py ${ARGS}

# # single gpu
# CUDA_VISIBLE_DEVICES=0 python main.py ${ARGS}

# two gpus on one node
# torchrun --nproc_per_node=2 main.py ${ARGS}

# python -m torch.distributed.launch --nproc_per_node=2 --use_env main.py ${ARGS}