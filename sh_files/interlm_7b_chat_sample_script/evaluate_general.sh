#!/usr/bin/env bash

# set -xe

MAIN_DIR=../..
CONFIG_YAML="sh_files/interlm_7b_chat_sample_script/eval_config.yaml"

ARGS1="--config_yaml ${CONFIG_YAML} --prompt_type llama2"
ARGS2="--config_yaml ${CONFIG_YAML} --prompt_type general"
ARGS3="--config_yaml ${CONFIG_YAML} --prompt_type easy"
ARGS4="--config_yaml ${CONFIG_YAML} --prompt_type choice"

python ${MAIN_DIR}/run_llm_response.py ${ARGS1}
python ${MAIN_DIR}/run_llm_response.py ${ARGS2}
python ${MAIN_DIR}/run_llm_response.py ${ARGS3}
python ${MAIN_DIR}/run_llm_response.py ${ARGS4}

