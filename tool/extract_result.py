import os
import re
import time
import argparse

from tqdm import tqdm

from util import read_json
from util import save_json
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
    parser.add_argument('--output_dir', type=str, default='result/gpt35')
    parser.add_argument('--output_file', type=str, default='eval_UniGeo_Cat_result.json')
    # model
    parser.add_argument('--quick_extract', action='store_true', default=True, help='use rules to extract answer for some problems')
    args = parser.parse_args()
    # args
    result_file = os.path.join(args.output_dir, args.output_file)
    # read results
    print(f"Reading {result_file}...")
    results = read_json(result_file)

    results_with_extraction = {}
    # tqdm, enumerate results
    for problem_id, response in tqdm(results.items()):
        extraction  = extract_answer(response, args.quick_extract)
        # import pdb; pdb.set_trace()
        results_with_extraction[problem_id] = dict(response=response,extraction=extraction)

    print(f"Saving results to {result_file}...")
    save_json(results_with_extraction, result_file)
    print(f"Results saved.")