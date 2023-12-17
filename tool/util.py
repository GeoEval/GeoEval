import os
import json
import pickle
import yaml
import codecs
from .prompt.dataset_prompt import GeoQA_PROMPT_DICT, Geometry3K_PROMPT_DICT, UniGeo_Cat_Prompt_DICT, UniGeo_Prove_Prompt_DICT
from .prompt.translate_prompt import trans_prompt
from .gpt_tool import get_chat_reponse
from tqdm import tqdm

def translate_timu(input_string):
    def create_test_prompt(demo_prompt, context):
        demo_prompt = demo_prompt.strip()
        full_prompt = f"{demo_prompt}\n\n{context}\n\nThe Translated Result is: "
        return full_prompt

    output_string = None
    try:
        output_string = get_chat_reponse(create_test_prompt(trans_prompt, input_string))
    except:
        output_string = "No Reponse from GPT3.5"

    return output_string

def process_geoqa_plus(file_path, output_file_path):
    timu_dict = {}    
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
        for test_id, test_data in tqdm(enumerate(data)):
            subject = translate_timu(test_data["subject"])
            timu_dict[test_data['id']] = GeoQA_PROMPT_DICT["prompt_with_choice"].format_map(dict(subject=subject, choices=test_data["choices"]))
            # 处理 JSON 数据的代码
    save_json(timu_dict, output_file_path)

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
            timu_dict[test_data['id']] = UniGeo_Cat_Prompt_DICT["prompt_with_choice"].format_map(dict(English_problem=test_data["English_problem"], choice_nums=test_data["choice_nums"], numbers=test_data["numbers"]))

    save_json(timu_dict, output_file_path)

def process_unigeo_prove(file_path, output_file_path):
    timu_dict = {}
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
        for test_id, test_data in enumerate(data):
            timu_dict[test_data['id']] = UniGeo_Prove_Prompt_DICT["prompt_prove"].format_map(dict(statement=test_data["statement"], question=test_data["question"]))
    
    save_json(timu_dict, output_file_path)

def read_json(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data

def save_json(data, output_file, indent=None):
    # get the dir path
    directory = os.path.dirname(output_file)
    # if the dir path don't exit, mkdir the dir
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(output_file, 'w', encoding="utf-8") as wr_file:
        if not indent:
            json.dump(data, wr_file, ensure_ascii=False)
        else:
            json.dump(data, wr_file, indent=2, ensure_ascii=False)

def read_pickle(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

def read_yaml(yaml_path: str) -> dict:
    # @Jiaxin: this file is used for loading configurations from yaml.
    with codecs.open(yaml_path, "r", "utf-8") as file:
        config = yaml.safe_load(file)
    return config