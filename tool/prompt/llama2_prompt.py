# coding:utf-8
# Author: Jiaxin
# Date: Dec-6-2023

"""This file converts the math problem to the target format accepted by the Llama-2-chat as described:
    https://github.com/facebookresearch/llama/issues/435 

    Example:
       1. ### Human: {prompt}\n\n{instruction}.\n### Assistant: 
       2. <s>[INST] Translate the English text "Hello! How are you?" to Spanish. [/INST] {model_response}</s>
    @Jiaxin: For 2. no need to add <s> and </s> because they will be added by the tokenizer.encoder().
        Also, I don't think "{model_response}" should be added.
"""

import re

INST_TAG = "[INST]"
INST_TAG_B = "[/INST]"

INSTRUCTION_BEGIN = "You are a problem-solving bot, and now I ask you to solve a geometry problem, please solve it. The problem is as follows:\n\n"
INSTRUCTION_END = "\n\nThe Answer and the Reason Process is:" 

OLD_FORMAT_BEGIN = r"You are a problem-solving bot, and now I ask you to solve a geometry problem. The problem is as follows:"
OLD_FORMAT_END = r"The Answer and the Reason Process is:"

def clean_format(example: str):
    """For cleaning the original format."""
    example = re.sub(OLD_FORMAT_BEGIN, example, "")
    example = re.sub(OLD_FORMAT_END, example, "")
    return example.strip()
    
def convert_to_llama2_input_format(example: str) -> str:
    """
        Input:
            - example: str. example should be raw problem without any additional CoT and Instruction.
        Output Format:
            [INST] {INSTRUCTION_END} {example} {INSTRUCTION_END} [/INST]
    """
    return f"{INST_TAG} {INSTRUCTION_BEGIN} {example} {INSTRUCTION_END} {INST_TAG_B}"

def convert_to_general_input_format(example: str) -> str:
    """
        Input:
            - example: str. example should be raw problem without any additional CoT and Instruction.
        Output Format:
            ### Human: {INSTRUCTION_BEGIN}\n\n{example}.\n### Problem-solving Bot:
    """
    return f"### Human: {INSTRUCTION_BEGIN}\n\n{example}\n### Problem-solving Bot:"