CONFIG_YAML="sh_files/wizardmath/eval_config.yaml"

ARGS="--config_yaml ${CONFIG_YAML} --prompt_type general"
python3 run_llm_response.py ${ARGS}