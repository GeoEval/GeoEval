import json
import os
multi_modal_prob_path = "result/llava/llava-v1.5-7b.json"
text_prob_path = "result/llava/llava-v1.5-7b-test.json"
output_prob_path = "result/llava/eval_GeoEval_result.json"
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

multi_modal_data_dict = read_json(multi_modal_prob_path)
text_data_dict = read_json(text_prob_path)
assert len(text_data_dict)+len(multi_modal_data_dict)==2000
merge_data = {**multi_modal_data_dict, **text_data_dict}
save_json(merge_data, output_prob_path)