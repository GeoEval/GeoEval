# coding:utf-8
# Author: Jiaxin
# Date: Dec-1-2023

"""This file tokenizes the data and prepares them as input for the model."""

import os
import torch
from argparse import ArgumentParser
from transformers import AutoTokenizer, AutoModel, AutoConfig
from tqdm import tqdm
from typing import Generator
from .util import read_json
from .prompt import convert_to_llama2_input_format, convert_to_general_input_format, convert_to_easy_input_format, convert_to_choice_input_format
from .merge_key_val import naive_merge

def load_tokenizer(path_or_name: str, from_local: bool = False) -> AutoTokenizer:
    if from_local:
        assert os.path.exists(path_or_name), f"local weights not exist: {path_or_name}"
    return AutoTokenizer.from_pretrained(path_or_name, trust_remote_code=True)

def load_config(path_or_name: str, from_local: bool = False) -> AutoConfig:
    if from_local:
        assert os.path.exists(path_or_name), f"local weights not exist: {path_or_name}"
    return AutoConfig.from_pretrained(path_or_name, trust_remote_code=True)    

def preprocess(tokenizer: AutoTokenizer, 
               max_seq_len: int, 
               sentence: str) -> dict:
    input_ids = tokenizer(sentence, max_length=max_seq_len, truncation=True, return_tensors="pt").input_ids
    # [[]] -> []
    if len(input_ids.size()) == 2:
        input_ids = input_ids.squeeze(0)
    return {"input_ids": input_ids, "o_len": len(sentence), "sentence": sentence}

# NOTE legacy
def __read_jsonl(path: str, max_seq_length: int, tokenizer: AutoTokenizer, args: ArgumentParser) -> Generator[dict, None, None]:    
    """This is used for loading the merge data."""
    datas = read_json(path)
    print(datas)
    for _, instance in datas.items():     
        example = naive_merge(
            diagram_description=instance["diagram_description"],
            text=instance["text"],
            choice_list=instance["choice_list"]
        )
        
        if args.prompt_type == "llama2":
            example = convert_to_llama2_input_format(example)
        elif args.prompt_type == "general":
            example = convert_to_general_input_format(example)
        elif args.prompt_type == "easy":
            example = convert_to_easy_input_format(example)
        elif args.prompt_type == "choice":
            example = convert_to_choice_input_format(example)
        else:
            raise ValueError(f"Unknown prompt type: {args.prompt_type}")

        feature = preprocess(tokenizer, max_seq_length, example)
        # print(feature)
        if feature == None:
            continue
        
        # print(feature)
        
        # feature["dataset_name"] = instance["dataset_name"]    
        feature["dataset_id"] = instance["dataset_id"]
        # feature["dataset_split"] = instance["dataset_split"] 
        # feature["diagram_name"] = instance["diagram_name"] if instance["diagram_name"] != None else ""
        # feature["num_dict"] = instance["num_dict"] if instance["num_dict"] != None else ""
        # feature["equation"] = instance["solution"]["equation"] if instance["solution"]["equation"] != None else ""
        # feature["program"] = instance["solution"]["program"] if instance["solution"]["program"] != None else ""
        # feature["cot"] = instance["solution"]["cot"] if instance["solution"]["cot"] != None else ""
        # feature["python"] = instance["solution"]["python"] if instance["solution"]["python"] != None else ""
        # feature["answer_value"] = instance["answer_value"] if instance["answer_value"] != None else ""
        # feature["choice_id"] = instance["choice_id"] if instance["choice_id"] != None else ""
        # feature["kowledge_point"] = instance["kowledge_point"] if instance["kowledge_point"] != None else ""

        yield feature

# NOTE legacy
def __collate_fn(features: list):
    input_ids_len = [len(feature["input_ids"]) for feature in features]
    
    # [1, o_len] FIXME: only support batch_size = 1
    input_ids = None
    input_len = []
    input_id_ = []
    input_sentence = []
    meta_data = []
    for i_len, feature in sorted(zip(input_ids_len, features), key=lambda x: -x[0]):
        print(feature)
        
        # FIXME: @Jiaxin very weird bug, the feature["input_ids"] will be [seq_len] when use "llama2"
        #   will be [1, seq_len] when use "general"
        if len(feature["input_ids"]) == 1:
            ids = torch.LongTensor(feature["input_ids"])
        else:
            ids = torch.LongTensor([feature["input_ids"]])
        id_ = feature["dataset_id"]
        o_len = feature["o_len"]
        
        input_ids = ids
        input_len.append(o_len)
        input_id_.append(id_)
        input_sentence.append(feature["sentence"])
        
        meta_data.append(
            {key: val for key, val in feature.items() if key not in ["input_ids", "o_len",]}
        )
    
    return {
        "input_ids": input_ids,
        "input_len": input_len,
        "id": input_id_,
        "input_sentence": input_sentence,
        "meda_data": meta_data,
    }