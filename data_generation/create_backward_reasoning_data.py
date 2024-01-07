# coding:utf-8
# Author: Knight
# Date: Dec-18-2023

import sys
from pathlib import Path
MAIN_PATH = Path(__file__).absolute().parent.parent
sys.path.insert(0, str(MAIN_PATH))

import re
import copy
import random

from typing import Tuple
from tqdm import tqdm

from argparse import ArgumentParser
from tool.util import read_json, save_json

string_number_dict = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                      "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
                      "eleven": 11, "twelve": 12, "fifth": 5,
                      "sixteen": 16, "half": "50%"}
 
class BackwardReasoningdDateset:
    
    def __init__(self, args: ArgumentParser) -> None:
        self.datas = read_json(args.data_path)
        self.unknown_var = "x"

    def create_backward_example(self) -> None:
        self.backward_datas = {}
        total_examples = 0
        for data_id, example in tqdm(self.datas.items()):
            if example["dataset_name"] in ["Geometry3K", "PGPS9K"]:
                total_examples +=1
                backward_example = self._process_pgps9k_geometry3k(example)
                if backward_example != None:
                    self.backward_datas[data_id] = backward_example
            elif example["dataset_name"] in ["UniGeo"]:
                total_examples +=1
                backward_example = self._process_unigeo(example)
                if backward_example != None:
                    self.backward_datas[data_id] = backward_example
        
        print(f"In total: {len(self.backward_datas)}. {len(self.backward_datas) / total_examples * 100:.2f}% has been converted into backward reasoning examples.")

        save_json(self.backward_datas, args.save_path, indent=2)

    def _process_pgps9k_geometry3k(self, example: dict) -> Tuple[dict, None]:
        semantic = example["diagram_description"]["semantic"]
        program = example["solution"]["program"]
        answer = example["answer_value"]
        text = example["text"]["Num_Exp"]
    
        semantic_number_indices = {}
        semantic_number_order = {}
        order = 0
        for idx, sema in enumerate(semantic):
            number_indices = self._number_index_extract(sema)
            if len(number_indices) > 0:
                semantic_number_indices[idx] = number_indices
                order_list = []
                for _ in number_indices:
                    order_list.append(f"N{order}")
                    order +=1
                semantic_number_order[idx] = order_list
                
        semantic_copy = copy.deepcopy(semantic)
        c = 0
        backward_answer = None
        if len(semantic_number_indices) > 0:  # can create
            while True and (c < 30):
                seleted_semantic_idx = random.choice(list(semantic_number_indices.keys()))
                selected_sema_split = semantic[seleted_semantic_idx].strip().split(" ")
                selected_num_idx = random.choice(range(len(semantic_number_indices[seleted_semantic_idx])))

                selected_num_in_passage_idx = semantic_number_indices[seleted_semantic_idx][selected_num_idx]
                selected_num_order = semantic_number_order[seleted_semantic_idx][selected_num_idx]

                if self.check_num_in_solution(selected_num_order, program):
                    backward_answer = selected_sema_split[selected_num_in_passage_idx]
                    selected_sema_split[selected_num_in_passage_idx] = self.replace_number_x(selected_sema_split[selected_num_in_passage_idx])
                    semantic_copy[seleted_semantic_idx] = " ".join(selected_sema_split)
                    break
                c +=1
        
        if backward_answer != None:
            text_copy = copy.deepcopy(text)
            text_copy += f" The correct answer is {answer}. Now please answer what is the value of x?"
            example["diagram_description"]["backward_semantic"] = semantic_copy
            example["backward_text"] = text_copy
            example["backward_answer_value"] = backward_answer
            
            return example
        
        else:
            return None
    
    def _process_unigeo(self, example: dict):
        program = example["solution"]["program"]
        answer = example["answer_value"]
        text = example["text"]["Num_Exp"]
        
        text_number_indices = self._number_index_extract(text)
        
        text_copy = copy.deepcopy(text)
        backward_answer = None
        c = 0
        if len(text_number_indices) > 0:
            text_copy_split = text_copy.split(" ")
            while True and (c < 10):
                selected_num_idx = random.choice(range(len(text_number_indices)))
                if self.check_num_in_solution(f"N_{selected_num_idx}", program):
                    backward_answer = text_copy_split[text_number_indices[selected_num_idx]]
                    text_copy_split[text_number_indices[selected_num_idx]] = self.replace_number_x(text_copy_split[text_number_indices[selected_num_idx]])
                    break
                c +=1
        
        if backward_answer != None:
            example["backward_text"] = " ".join(text_copy_split) + f". The correct answer is {answer}. Now please answer what is the value of x?"
            example["backward_answer_value"] = backward_answer

            return example

        else:
            return None
    
    def _number_index_extract(self, string: str) -> list:
        string_split = string.strip().split(" ")
        number_indices = []
        for idx, token in enumerate(string_split):
            if token in string_number_dict:
                number_indices.append(idx)
            if re.search("[\d]", token) is not None:
                if re.search('[a-zA-Z]', token) or re.search('[\\n:\(\)-*\"+–-]', token):
                    continue
                else:
                    number_indices.append(idx)
        return number_indices

    def replace_number_x(self, token: str) -> str:
        if token in string_number_dict:
            token = str(string_number_dict[token])
        if token[-1] in (",", ".", "?", ";", "”", "'", "!", "\"", "%"):
            try:
                mo = re.match('.*([0-9])[^0-9]*$', token)
                return self.unknown_var + token[mo.end(1):]
            except:
                print(f"the string is {token}")
        elif token[0] in ("$"):
            return "$" + self.unknown_var
        else:
            return self.unknown_var
    
    def check_num_in_solution(self, num_order: int, solution: str) -> bool:
        if num_order in solution:
            return True
        return False

def main(args):
    backward_dataset = BackwardReasoningdDateset(args)
    backward_dataset.create_backward_example()    

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--data_path", type=str)
    parser.add_argument("--save_path", type=str)
    
    args = parser.parse_args()
    args.data_path = MAIN_PATH / "LLM_eval/dataset_merge/select.json"
    args.save_path = MAIN_PATH / "LLM_eval/dataset_merge/backward_reasoning_select.json"
    
    main(args)