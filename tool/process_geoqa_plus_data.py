from util import process_geoqa_plus

if __name__ == '__main__':
    dataset_path = 'ICL_dataset/GeoQA+/new-test.pk'
    output_json_file = 'LLM_eval/eval_GeoQA_plus_test.json'
    process_geoqa_plus(dataset_path, output_json_file)