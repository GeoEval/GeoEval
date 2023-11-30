# coding:utf-8
# Author: Jiaxin
# Date: Nov-30-2023

import os
import sys
import json
import codecs

from argparse import ArgumentParser
from pathlib import Path

MAIN_PATH = Path(__file__).absolute().parent.parent
sys.path.insert(0, str(MAIN_PATH))

from argparse import ArgumentParser, Namespace
from tool import read_yaml

def merge_single_json(data_dir: str, save_path: str) -> list:
    """For Math/geometry only, merge each json file from one directory to a list."""
    assert os.path.exists(data_dir), f"{data_dir} doesn't exist."
    all_example_names = os.listdir(data_dir)
    
    examples = []
    for name in all_example_names:
        with codecs.open(os.path.join(data_dir, name), "r", "utf-8") as file:
            example = json.load(file)
            example["id"] = name
            examples.append(example)

    print(f"processed {len(examples)} examples.")
    with codecs.open(save_path, "w", "utf-8") as file:
        json.dump(examples, file, indent=2)

if __name__ == "__main__":
    # name the yaml config path
    parser = ArgumentParser()
    parser.add_argument("--yaml_config", type=str, default="./convert_to_py.yaml")
    args = parser.parse_args()
    
    # read config from yaml file
    config = read_yaml(args.yaml_config)
    args = vars(args)
    
    # move config to the args
    for config_name, configs in config.items():
        if config_name == "MATH":
            for key, val in configs.items():
                args[key] = val
    args = Namespace(**args)
    
    # train
    merge_single_json(os.path.join(MAIN_PATH, args.ori_data_dir, "train/geometry"), os.path.join(MAIN_PATH, args.ori_save_dir, "train.json"))
    # test
    merge_single_json(os.path.join(MAIN_PATH, args.ori_data_dir, "test/geometry"), os.path.join(MAIN_PATH, args.ori_save_dir, "test.json"))