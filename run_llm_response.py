import re
import json
from tool.gpt_tool import get_chat_reponse
from tool.opensource_llm_tool import get_opensource_llm_reponse
from tool.util import read_json, save_json
from model import create_model_with_tokenizer
from tqdm import tqdm
import argparse 
import os



dataset_list = ['Geometry3K','PGPS9K', 'UniGeo_Cat', 'UniGeo_Prove']
type_list = ['api_model', 'opensource_model']
model_list = ['gpt35', '']

def eval(args, dataset_path, output_json_file):
    data_load = read_json(dataset_path)

    if args.model_type == 'api_model':
        eval_api_model(dataset_path, output_json_file)
    if args.model_type == 'opensource_model':
        eval_opensource_model(args, dataset_path, output_json_file)

def eval_opensource_model(args, dataset_path, output_json_file):
    
    data_load = read_json(dataset_path)
    answer_dict = {}
    model, tokenizer = create_model_with_tokenizer(args)
    
    for data_k, question in tqdm(data_load.items()):
        answer_result = get_opensource_llm_reponse(question, model, tokenizer)
        answer_dict[data_k] =  answer_result

    save_json(answer_dict, output_json_file)
    return model, tokenizer

def eval_api_model(dataset_path, output_json_file):
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
    parser.add_argument('--model_type', type=str, choices=type_list, default='api_model')
    parser.add_argument('--model_name', type=str, choices=model_list, default='gpt35', default='gpt35')
    parser.add_argument('--eval_dataset_path', type=str, default='LLM_eval/')
    parser.add_argument('--input_file', type=str, default='eval_{dataset}_test.json')
    parser.add_argument('--output_dir', type=str, default='{model_name}')
    parser.add_argument('--output_file', type=str, default='eval_{dataset}_result.json')
    # for model_path input
    parser.add_argument('--weight_path', type=str, default='./')
    args = parser.parse_args()
    
    dataset_path = os.path.join(args.eval_dataset_path, args.input_file.format_map(dict(dataset=args.dataset)))
    output_json_dir = args.output_dir.format_map(dict(model_name=args.model_name))
    output_json_file = args.output_file.format_map(dict(dataset=args.dataset))
    output_json_file = os.path.join('./result', output_json_dir, output_json_file)
    eval(args, dataset_path, output_json_file)