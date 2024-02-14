import json
import os
input_path = 'backaug_result/wizardmath70b/eval_GeoEval_result.json'
output_path = 'backaug_result/wizardmath70b/eval_GeoEval_result.json'
model_name = "wizardmath70b"

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

data = read_json(input_path)
new_data_dict = {}

for prob_id, data in data.items():
     predictions = data["solution"]["wizardmath"]
     del data["solution"]["wizardmath"]
     data["solution"][model_name] = predictions 
     new_data_dict[prob_id] = data
save_json(new_data_dict, output_path)




    