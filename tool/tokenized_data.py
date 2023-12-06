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
from .prompt import convert_to_llama2_input_format, convert_to_general_input_format

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
    input_ids = tokenizer.encode(sentence, max_length=max_seq_len, truncation=True)
    return {"input_ids": input_ids, "o_len": len(sentence)}

def read_jsonl(path: str, max_seq_length: int, tokenizer: AutoTokenizer, args: ArgumentParser) -> Generator[dict, None, None]:    
    datas = read_json(path)
    for id_, example in datas.items():
        if args.prompt_type == "llama2":
            example = convert_to_llama2_input_format(example)
        elif args.prompt_type == "general":
            example = convert_to_general_input_format(example)
        else:
            raise ValueError(f"Unknown prompt type: {args.prompt_type}")
        feature = preprocess(tokenizer, max_seq_length, example)
        if feature == None:
            continue
        feature["id"] = id_
        yield feature

def collate_fn(features: list):
    input_ids_len = [len(feature["input_ids"]) for feature in features]
    
    input_ids = []
    input_len = []
    input_id_ = []
    for i_len, feature in sorted(zip(input_ids_len, features), key=lambda x: -x[0]):
        ids = feature["input_ids"]
        id_ = feature["id"]
        o_len = feature["o_len"]
        
        input_ids.append(torch.LongTensor(ids))
        input_len.append(o_len)
        input_id_.append(id_)
    
    input_ids = torch.stack(input_ids)
    
    return {
        "input_ids": input_ids,
        "input_len": input_len,
        "id": input_id_,
    }
        