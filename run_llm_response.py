from tool.gpt_tool import get_chat_reponse
from tool.opensource_llm_tool import get_opensource_llm_reponse
from tool import save_json, read_json
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

from tool.data_loader import GeoEvalDataset, GeoApiEvalDataset

dataset_list = ['Geometry3K','PGPS9K', 'UniGeo_Cat', 'UniGeo_Prove']
type_list = ['api_model', 'opensource_model']
model_list = ['gpt35']

def eval(args, dataset_path, output_json_file):
    if args.model_type == 'api_model':
        eval_api_model(args, dataset_path, output_json_file)
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

def eval_api_model(args, dataset_path, output_json_file):
    # import pdb; pdb.set_trace()
    dataset = GeoApiEvalDataset(
        dataset_path=dataset_path,
        args=args,
    )
    data_loader = DataLoader(dataset, batch_size=1, collate_fn=dataset.collate_fn)
    answer_dict = {}
    times = 0
    for data_iter in tqdm(data_loader):
        # if times>=3:
        #    break
        model_input = data_iter["model_input"]
        instance_id = data_iter['prob_id']
        instance    = data_iter['instance']
        for i in range(args.bsz):
<<<<<<< HEAD
            # import pdb; pdb.set_trace()
=======
>>>>>>> a8f2a3d230bcc3fa5f6b27c1703b0978584fafe2
            answer_result = get_chat_reponse(model_input[i])
            instance[i]["solution"][args.model_name] = answer_result
            answer_dict[instance_id[i]] = instance[i]
        times +=1

    save_json(answer_dict, output_json_file)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt_type", default="llama2", choices=["llama2", "general", "easy", "choice", "general_choice"], type=str) # prompt_type
    parser.add_argument("--backward_reason", action="store_true", help="Description of backward_reason argument")
    parser.add_argument("--aug_reason", action="store_true", help="Description of aug_reason argument")
    parser.add_argument("--solid_reason", action="store_true", help="Description of aug_reason argument")
    parser.add_argument("--output_type", default="", type=str)
    parser.add_argument("--config_yaml", type=str)

    args = parser.parse_args()
    config = read_yaml(os.path.join(MAIN_PATH, args.config_yaml))
    
    args = vars(args)  # args提供支持最简单的方法
    for config_name, configs in config.items():
        if config_name == "General":
            for key, val in configs.items():
                args[key] = val
    args = Namespace(**args)
    # import pdb;pdb.set_trace()
    if args.output_type == "aug_result": args.input_file = "dataset_merge/aug.json"
    if args.output_type == "backaug_result": args.input_file = "dataset_merge/backward_aug.json"
    # import pdb; pdb.set_trace()
    dataset_path = os.path.join(MAIN_PATH, args.eval_dataset_path, args.input_file)
    output_json_dir = os.path.join(MAIN_PATH, args.output_dir.format_map(dict(model_name=args.model_name, output_dir=args.output_type)))
    # now_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    output_json_file = os.path.join(output_json_dir, f"eval_{args.dataset}_result.json")

    eval(args, dataset_path, output_json_file)