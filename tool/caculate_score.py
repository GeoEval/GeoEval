import os
import re
import argparse
from tqdm import tqdm

import sys
sys.path.append('../GeoEval')
# !pip install python-Levenshtein
from tool.util import read_json, save_json, read_pickle

ID_2_TARGET_DICT = {}


def caculate_score_on_geoeval(args):
    # args
    read_file = os.path.join(args.output_dir, args.output_file)
    # read result json with answer extract and problem file
    print(f"Reading {read_file}...")
    results = read_json(read_file)
    ## [1] Evaluate if the prediction is true or false
    print("\nEvaluating the predictions...")
    multi_modal_correct = 0
    text_correct = 0
    text_count = 0
    multi_modal_count = 0
    for problem_id, reason_with_answer in tqdm(results.items()):
        if reason_with_answer["diagram_name"]!=None:
            answer = reason_with_answer["answer_value"]
            extraction = reason_with_answer["solution"][args.model_name]["extraction"]
            # normalize the extracted answer to match the answer type
            prediction = normalize_extracted_answer(extraction)
            # verify the prediction is true or false
            true_false = safe_equal(prediction, answer)
            multi_modal_count += 1
            if true_false:
                multi_modal_correct += 1
        else:
            try:
                answer = reason_with_answer["answer_value"]
                extraction = reason_with_answer["solution"][args.model_name]["extraction"]
                # normalize the extracted answer to match the answer type
                prediction = normalize_extracted_answer(extraction)
                # verify the prediction is true or false
                true_false = safe_equal(prediction, answer)
                if true_false:
                    text_correct += 1
            except:
                pass
            text_count += 1

    # import pdb; pdb.set_trace()
    assert (text_count+multi_modal_count)==2000

    scores = {"average": {"multi_modal_accuracy": multi_modal_correct/multi_modal_count, 
                          "text_accuracy": text_correct/text_count, 
                          "multi_modal_correct": multi_modal_correct, "text_correct":text_correct, "total": 2000}}
    # save the scores
    # import pdb; pdb.set_trace()
    scores_file = os.path.join(args.output_dir, args.score_file)
    save_json(scores, scores_file)
    return 

def build_id_target_dict(problem_data):
    for prob_item in problem_data:
        ID_2_TARGET_DICT[prob_item['id']] = prob_item['target_number']

def caculate_score_on_UniGeo(args):
    # args
    read_file = os.path.join(args.output_dir, args.output_file)
    problem_file = os.path.join(args.problem_path, args.problem_file)  
    

    # read result json with answer extract and problem file
    print(f"Reading Problem File {problem_file}...")
    problem_data  = read_pickle(problem_file)
    print(f"Reading {read_file}...")
    results = read_json(read_file)
    import pdb; pdb.set_trace()
    ## [1] Evaluate if the prediction is true or false
    print("\nEvaluating the predictions...")

    build_id_target_dict(problem_data)
    correct = 0
    count = 0
    for problem_id, reason_with_answer in tqdm(results.items()):
        answer = ID_2_TARGET_DICT[int(problem_id)]
        extraction = reason_with_answer["extraction"]
        # normalize the extracted answer to match the answer type
        prediction = normalize_extracted_answer(extraction)

        # verify the prediction is true or false
        true_false = safe_equal(prediction, answer)
        count += 1
        if true_false:
            correct += 1

    scores = {"average": {"accuracy": correct/count, "correct": correct, "total": count}}
    # save the scores
    scores_file = os.path.join(args.output_dir, args.score_file)
    print(f"\nSaving {scores_file}...")
    save_json(scores, scores_file)
    print("\nDone!") 

def caculate_score_on_Geo3K_PGPS9K(args):
    # args
    read_file = os.path.join(args.output_dir, args.output_file)
    problem_file = os.path.join(args.problem_path, args.problem_file)  
    

    # read result json with answer extract and problem file
    print(f"Reading Problem File {problem_file}...")
    problem_data  = read_json(problem_file)
    print(f"Reading {read_file}...")
    results = read_json(read_file)
    
    ## [1] Evaluate if the prediction is true or false
    print("\nEvaluating the predictions...")

    correct = 0
    count = 0
    for problem_id, reason_with_answer in tqdm(results.items()):
        answer = problem_data[problem_id]['answer']
        extraction = reason_with_answer["extraction"]
        # normalize the extracted answer to match the answer type
        prediction = normalize_extracted_answer(extraction)

        # verify the prediction is true or false
        true_false = safe_equal(prediction, answer)
        count += 1
        if true_false:
            correct += 1

    scores = {"average": {"accuracy": correct/count, "correct": correct, "total": count}}
    # save the scores
    scores_file = os.path.join(args.output_dir, args.score_file)
    print(f"\nSaving {scores_file}...")
    save_json(scores, scores_file)
    print("\nDone!")

def normalize_extracted_answer(extraction, question_mode="completion"):
    """
    Normalize the extracted answer to match the answer type
    """
    if question_mode == 'multi_choice':
        # make sure the extraction is a string
        pass

    if question_mode == 'completion':
        try:
            extraction = str(float(extraction))
        except:
            extraction = None

    return extraction
    
def safe_equal(prediction, answer):
    """
    Check if the prediction is equal to the answer, even if they are of different types
    """
    try:
        if float(prediction)-float(answer)<1e-3:
            return True
        return False
    except Exception as e:
        print(e)
        return False
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', type=str, default='result/{model_name}')
    parser.add_argument('--model_name', type=str, default='mplug_owl2')
    parser.add_argument('--dataset_name', type=str, default='GeoEval')
    parser.add_argument('--output_file', type=str, default='eval_{dataset_name}_result.json')

    parser.add_argument('--problem_path', type=str, default='LLM_eval/')
    parser.add_argument('--problem_file', type=str, default='test.json')

    parser.add_argument('--score_file', type=str, default='eval_{dataset_name}_result_score.json')
    args = parser.parse_args()

    args.output_file = args.output_file.format_map(dict(dataset_name=args.dataset_name))
    args.output_dir = args.output_dir.format_map(dict(model_name=args.model_name))
    args.score_file  = args.score_file.format_map(dict(dataset_name=args.dataset_name))
    if args.dataset_name == "GeoEval": 
        args.problem_path = os.path.join(args.problem_path, 'dataset_merge')
        args.problem_file = 'select.json'
        caculate_score_on_geoeval(args)
