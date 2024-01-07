# coding:utf-8
# Author: Jiaxin Zhang
# Date: Dec-8-2023

import torch
from argparse import ArgumentParser
from torch.utils.data import Dataset
from transformers import AutoTokenizer

from .util import read_json
from .merge_key_val import naive_merge
from .prompt import convert_to_llama2_input_format, convert_to_general_input_format, convert_to_easy_input_format, convert_to_choice_input_format, convert_to_fewshot_input_format
from .tokenized_data import preprocess

class GeoApiEvalDataset(Dataset):
    def __init__(self, dataset_path: str, args: ArgumentParser):
        self.dataset_path = dataset_path
        self.args = args
        
        # load data from json file
        raw_datas = read_json(dataset_path)
        print(f"load {len(raw_datas)} original data")
        
        self.datas = []
        self.instances = []
        self.prob_ids = []
        for prob_id, instance in raw_datas.items():
            instance_processed = self._process_per_instance(
                instance=instance,
                merge_type=args.merge_type,
                prompt_type=args.prompt_type,
            )
            self.datas.append(instance_processed)
            self.instances.append(instance)
            self.prob_ids.append(prob_id)
        print(f"processed {len(self.datas)} data")
        
    def _process_per_instance(self, instance: dict, merge_type: str, prompt_type: str) -> dict:
        # import pdb;pdb.set_trace()
        example = naive_merge(
            diagram_description=instance["diagram_description"],
            text=instance["text"],
            choice_list=instance["choice_list"]
        )
        # wrap example with instruction
        if prompt_type == "llama2":
            example = convert_to_llama2_input_format(example)
        elif prompt_type == "general":
            example = convert_to_general_input_format(example)
        elif prompt_type == "easy":
            example = convert_to_easy_input_format(example)
        elif prompt_type == "choice":
            example = convert_to_choice_input_format(example)
        else:
            raise ValueError(f"Unknown prompt type: {prompt_type}")

        return example

    def __len__(self) -> int:
        return len(self.datas)

    def __getitem__(self, index: int) -> dict:
        model_input = self.datas[index]
        instance = self.instances[index]
        prob_id     = self.prob_ids[index]
        return model_input, prob_id, instance

    def collate_fn(self, batch: list) -> dict:
        # import pdb; pdb.set_trace()
        model_inputs = []
        prob_ids = []
        instances = []
        for sample in batch: 
            model_input, prob_id, instance = sample 
            model_inputs.append(model_input)
            instances.append(instance)
            prob_ids.append(prob_id)
        # FIXME: for llama2, there is no pad_token, since we are using bsz=1,
        # setting 0 here doesn't influence.
        return dict(model_input=model_inputs, prob_id=prob_ids, instance=instances)


class GeoEvalDataset(Dataset):
    def __init__(self, dataset_path: str, max_seq_length: int, tokenizer: AutoTokenizer, args: ArgumentParser):
        self.dataset_path = dataset_path
        self.max_seq_length = max_seq_length
        self.tokenizer = tokenizer
        self.args = args
        
        # load data from json file
        raw_datas = read_json(dataset_path)
        print(f"load {len(raw_datas)} original data")
        
        self.datas = []
        for key, instance in raw_datas.items():
            feature = self._process_per_instance(
                instance=instance,
                merge_type=args.merge_type,
                prompt_type=args.prompt_type,
            )
            feature["unique_id"] = key
            if feature != None:
                self.datas.append(feature)
        print(f"processed {len(self.datas)} data")
        
    def _process_per_instance(self, instance: dict, merge_type: str, prompt_type: str) -> dict:
        # combine description, text, choice together
        example = naive_merge(
            diagram_description=instance["diagram_description"],
            text=instance["text"],
            choice_list=instance["choice_list"]
        )
        
        # wrap example with instruction
        if prompt_type == "llama2":
            example = convert_to_llama2_input_format(example)
        elif prompt_type == "general":
            example = convert_to_general_input_format(example)
        elif prompt_type == "easy":
            example = convert_to_easy_input_format(example)
        elif prompt_type == "choice":
            example = convert_to_choice_input_format(example)
        elif prompt_type == "fewshot":
            example = convert_to_fewshot_input_format(example)
        else:
            raise ValueError(f"Unknown prompt type: {prompt_type}")

        # tokenize example
        feature = preprocess(self.tokenizer, self.max_seq_length, example)
        
        feature.update(instance)
        
        return feature

    def __len__(self) -> int:
        return len(self.datas)

    def __getitem__(self, index: int) -> dict:
        return self.datas[index]
    
    def collate_fn(self, batch: list) -> dict:
        bsz = len(batch)
        seq_len = [len(b["input_ids"]) for b in batch]
        max_seq_len = max(seq_len)

        # FIXME: for llama2, there is no pad_token, since we are using bsz=1,
        # setting 0 here doesn't influence.
        tensor_input_ids = torch.LongTensor(bsz, max_seq_len).fill_(0)
        original_len = []
        meta_data = []
        for i in range(bsz):
            tensor_input_ids[i, :seq_len[i]] = batch[i]["input_ids"]
            original_len.append(batch[i]["o_len"])
            meta_data.append(
                {key: val for key, val in batch[i].items() if key not in ["input_ids", "o_len"]}
            )
        
        outputs = {
            "input_ids": tensor_input_ids,
            "input_len": original_len,
            "meta_data": meta_data,
        }
        
        return outputs