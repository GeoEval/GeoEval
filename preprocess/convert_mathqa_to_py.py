# coding:utf-8
# Author: Jiaxin
# Date: Nov-30-2023

"""This file is mainly from:
    https://github.com/google/trax/blob/master/trax/examples/MathQA_Python_generation_notebook.ipynb

    Install following packages first:
        pip install --upgrade pip
        pip install --upgrade jax jaxlib
        pip install trax
"""


from trax import data
import json
import numpy as np
import os
import tensorflow as tf

import os
import sys
from pathlib import Path

MAIN_PATH = Path(__file__).absolute().parent.parent
sys.path.insert(0, str(MAIN_PATH))

import codecs
from argparse import ArgumentParser, Namespace
from tool import read_yaml

def read_all_problems(mathqa_gen):
  problems = []
  questions = set()
  index = 0
  while True:
    problem = next(mathqa_gen)
    problem_dict = {}
    if problem[0] in questions:
      break
    else:
      problem_dict['text'] = problem[0]
      problem_dict['code'] = problem[1]
      problem_dict['dsl_code'] = problem[2]
      problem_dict['reasoning'] = problem[3].strip('\"').strip("\'")
      problem_dict['answer'] = data.tf_inputs.execute_mathqa_program(problem[0], problem[1].split('\n'))
      problem_dict['task_id'] = index
      np.testing.assert_almost_equal(problem_dict['answer'], data.tf_inputs.execute_mathqa_dsl_program(problem[0], [problem[2]]))
      problems.append(problem_dict)
      questions.add(problem[0])
      index += 1
  return problems

def save_to_json(data: list, path: str) -> None:
    with codecs.open(path, "w", "utf-8") as file:
        json.dump(data, file, indent=2)

def main(data_dir, save_dir):
    # train
    mathqa_train_gen = data.CreateMathQAInputs(dataset_path=data_dir, cumulative=False, python_code=True, full_dict=True, train=True, test=False)()
    train_problems = read_all_problems(mathqa_train_gen)
    save_to_json(train_problems, os.path.join(save_dir, "mathqa_python_train.json")) 

    # val
    mathqa_val_gen = data.CreateMathQAInputs(dataset_path=data_dir, cumulative=False, python_code=True, full_dict=True, train=False, test=False)()
    val_problems = read_all_problems(mathqa_val_gen)
    save_to_json(val_problems, os.path.join(save_dir, "mathqa_python_val.json")) 

    # test
    mathqa_test_gen = data.CreateMathQAInputs(dataset_path=data_dir, cumulative=False, python_code=True, full_dict=True, train=False, test=True)()
    test_problems = read_all_problems(mathqa_test_gen)
    save_to_json(test_problems, os.path.join(save_dir, "mathqa_python_test.json"))

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--yaml_config", type=str, default="./convert_to_py.yaml")
    args = parser.parse_args()
    
    config = read_yaml(args.yaml_config)
    args = vars(args)
    
    for config_name, configs in config.items():
        if config_name == "MathQA":
            for key, val in configs.items():
                args[key] = val
    args = Namespace(**args)
   
    args.data_dir = os.path.join(MAIN_PATH, args.data_dir)
    args.save_dir = os.path.join(MAIN_PATH, args.save_dir)
    main(args.data_dir, args.save_dir)