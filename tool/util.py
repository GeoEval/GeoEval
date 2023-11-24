import os
import json
import pickle

from tool.prompt.dataset_prompt import GeoQA_PROMPT_DICT, Geometry3K_PROMPT_DICT, UniGeo_Cat_Prompt_DICT, UniGeo_Prove_Prompt_DICT


def process_geoqa_pk_file(file_path, output_file_path='ICL_dataset/GeoQA/LLM_eval/eval_input.json'):
    # 在这里添加处理 JSON 文件的代码
    timu_dict = {}
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
        for test_id, test_data in enumerate(data):
            timu_dict[test_id] = GeoQA_PROMPT_DICT["prompt_with_choice"].format_map(dict(subject=test_data["subject"], choices=test_data["choices"]))
            # 处理 JSON 数据的代码
    save_json(timu_dict, output_file_path)

def process_geometry3k_pgps9k_json_file(file_path, output_file_path):
    timu_dict = {}
    geo3k_data = read_json(file_path)
    for prob_id, prob_data in geo3k_data.items():
        if prob_data["parsing_sem_seqs"]!=[]:
            timu_dict[prob_id] = Geometry3K_PROMPT_DICT["prompt_with_sem_seqs_with_choice"].format_map(dict(parsing_stru_seqs=",".join(prob_data["parsing_stru_seqs"]), parsing_sem_seqs=",".join(prob_data["parsing_sem_seqs"]), \
                                                                                             text=prob_data["text"], choices=prob_data["choices"]))
        else:
            timu_dict[prob_id] = Geometry3K_PROMPT_DICT["prompt_without_sem_seqs_with_choice"].format_map(dict(parsing_stru_seqs=",".join(prob_data["parsing_stru_seqs"]), \
                                                                                            text=prob_data["text"], choices=prob_data["choices"]))
    save_json(timu_dict, output_file_path)

def process_unigeo_cat(file_path, output_file_path):
    timu_dict = {}
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
        for test_id, test_data in enumerate(data):
            timu_dict[test_data['id']] = UniGeo_Cat_Prompt_DICT["prompt_with_choice"].format_map(dict(English_problem=test_data["English_problem"], choice_nums=test_data["choice_nums"]))

    save_json(timu_dict, output_file_path)

def process_unigeo_prove(file_path, output_file_path):
    timu_dict = {}
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
        import pdb; pdb.set_trace()
        for test_id, test_data in enumerate(data):
            timu_dict[test_data['id']] = UniGeo_Prove_Prompt_DICT["prompt_prove"].format_map(dict(statement=test_data["statement"], question=test_data["question"]))
    
    save_json(timu_dict, output_file_path)

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_json(data, output_file):
    import pdb; pdb.set_trace()
    # get the dir path
    directory = os.path.dirname(output_file)
    # if the dir path don't exit, mkdir the dir
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(output_file, 'w') as wr_file:
        json.dump(data, wr_file)

def read_pickle(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data