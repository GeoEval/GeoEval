CONFIG_YAML="sh_files/gpt35/eval_solid_config.yaml"

ARGS="--config_yaml ${CONFIG_YAML} --prompt_type general_choice --output_type solid_result"
python3 run_llm_response.py ${ARGS}

