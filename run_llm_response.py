import re
import json
from tool.gpt_tool import get_chat_reponse
from tool.util import read_json, save_json
from tqdm import tqdm
import argparse 
import os

dataset_list = ['Geometry3K','PGPS9K', 'UniGeo_Cat', 'UniGeo_Prove']

def eval(dataset_path, output_json_file):
    data_load = read_json(dataset_path)

    answer_dict = {}
    for data_k, question in tqdm(data_load.items()):
        answer_result = get_chat_reponse(question)
        answer_dict[data_k] =  answer_result

    save_json(answer_dict, output_json_file)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # input
    parser.add_argument('--dataset', type=str, choices=dataset_list, default='PGPS9K')
    parser.add_argument('--model_name', type=str, default='gpt35')
    parser.add_argument('--eval_dataset_path', type=str, default='LLM_eval/')
    parser.add_argument('--input_file', type=str, default='eval_{dataset}_test.json')
    parser.add_argument('--output_dir', type=str, default='{model_name}')
    parser.add_argument('--output_file', type=str, default='eval_{dataset}_result.json')
    args = parser.parse_args()
    
    dataset_path = os.path.join(args.eval_dataset_path, args.input_file.format_map(dict(dataset=args.dataset)))
    output_json_dir = args.output_dir.format_map(dict(model_name=args.model_name))
    output_json_file = args.output_file.format_map(dict(dataset=args.dataset))
    output_json_file = os.path.join('./result', output_json_dir, output_json_file)
    eval(dataset_path, output_json_file)