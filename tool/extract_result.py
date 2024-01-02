import os
import re
import time
import argparse

from tqdm import tqdm

import sys
sys.path.append('../GeoEval')
from tool.util import read_json
from tool.util import save_json
# load demo 
from prompt.ext_prompt import ext_prompt
from gpt_tool import get_chat_reponse


def create_test_prompt(demo_prompt, response):
    demo_prompt = demo_prompt.strip()
    full_prompt = f"{demo_prompt}\n\n{response}\n\nExtracted answer: "
    return full_prompt

def extract_answer(response, quick_extract=False):
    # quick extraction
    if quick_extract: # if quick can get answer, use quick
        print("Quickly extracting answer...")
        # The answer is "text". -> "text"
        try:
            result = re.search(r'The answer is "(.*)"\.', response)
            if result:
                extraction = result.group(1)
                return extraction
        except:
            pass

    # general extraction
    try:
        full_prompt = create_test_prompt(ext_prompt, response)
        extraction = get_chat_reponse(full_prompt)
        return extraction
    except Exception as e:
        print(e)
        print(f"Error in extracting answer for {response}")

    return ""

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # input
    parser.add_argument('--model_name', type=str, default='mplug_owl2')
    parser.add_argument('--dataset_name', type=str, default='GeoEval')
    parser.add_argument('--output_dir', type=str, default='result/{model_name}')
    parser.add_argument('--output_file', type=str, default='eval_{dataset_name}_result.json')
    # model
    parser.add_argument('--quick_extract', action='store_true', default=True, help='use rules to extract answer for some problems')
    args = parser.parse_args()
    # args
    args.output_dir = args.output_dir.format_map(dict(model_name=args.model_name))
    # 
    result_file = os.path.join(args.output_dir, args.output_file.format_map(dict(dataset_name=args.dataset_name)))
    # read results
    print(f"Reading {result_file}...")
    #import pdb; pdb.set_trace()
    results = read_json(result_file)

    results_with_extraction = {}
    # tqdm, enumerate results
    for problem_id, data_item in tqdm(results.items()):
        try:
            extraction  = extract_answer(data_item["solution"][args.model_name], args.quick_extract)
            # import pdb; pdb.set_trace()
            response = data_item["solution"][args.model_name]
            data_item["solution"][args.model_name] = dict(response=response,extraction=extraction)
        except:
            pass
        results_with_extraction[problem_id] = data_item

    print(f"Saving results to {result_file}...")
    save_json(results_with_extraction, result_file)
    print(f"Results saved.")