from tool.gpt_tool import get_chat_reponse
from tool.opensource_llm_tool import get_opensource_llm_reponse
from tool.util import read_json, save_json
from model import create_model_tokenizer
from tqdm import tqdm
import argparse 
import os
from tool import read_yaml
from pathlib import Path
from argparse import Namespace
from datetime import datetime
from datasets import Dataset
from torch.utils.data import DataLoader
MAIN_PATH = Path(__file__).absolute().parent

from tool.data_loader import GeoEvalDataset

dataset_list = ['Geometry3K','PGPS9K', 'UniGeo_Cat', 'UniGeo_Prove']
type_list = ['api_model', 'opensource_model']
model_list = ['gpt35', '']

def eval(args, dataset_path, output_json_file):
    if args.model_type == 'api_model':
        eval_api_model(dataset_path, output_json_file)
    if args.model_type == 'opensource_model':
        eval_opensource_model(args, dataset_path, output_json_file)

def eval_opensource_model(args, dataset_path, output_json_file):
    # create model, tokenizer
    model, tokenizer, config = create_model_tokenizer(args, from_local=args.from_local)
    
    dataset = GeoEvalDataset(
        dataset_path=dataset_path,
        max_seq_length=args.max_seq_length,
        tokenizer=tokenizer,
        args=args,
    )
        
    data_loader = DataLoader(dataset, batch_size=args.bsz, collate_fn=dataset.collate_fn)

    answer_result = get_opensource_llm_reponse(data_loader, model, tokenizer, args.sample_number)

    save_json(answer_result, output_json_file, indent=2)

def eval_api_model(dataset_path, output_json_file):
    data_load = read_json(dataset_path)

    answer_dict = {}
    for data_k, question in tqdm(data_load.items()):
        answer_result = get_chat_reponse(question)
        answer_dict[data_k] =  answer_result

    save_json(answer_dict, output_json_file)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_yaml", type=str)
    args = parser.parse_args()
    config = read_yaml(os.path.join(MAIN_PATH, args.config_yaml))
    
    args = vars(args)
    for config_name, configs in config.items():
        if config_name == "General":
            for key, val in configs.items():
                args[key] = val
    args = Namespace(**args)

    dataset_path = os.path.join(MAIN_PATH, args.eval_dataset_path, args.input_file)
    output_json_dir = os.path.join(MAIN_PATH, args.output_dir)
    now_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    output_json_file = os.path.join(output_json_dir, f"{args.dataset}_{args.model_name}_{now_time}.json")
    args.cached_dir = os.path.join(MAIN_PATH, args.cached_dir)
    os.makedirs(args.cached_dir, exist_ok=True)

    eval(args, dataset_path, output_json_file)