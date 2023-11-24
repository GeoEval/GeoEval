from util import process_unigeo_cat
from util import process_unigeo_prove


if __name__ == '__main__':
    dataset_path = 'ICL_dataset/UniGeo/calculation_test.pk'
    output_json_file = 'LLM_eval/eval_UniGeo_Cat_test.json'
    process_unigeo_cat(dataset_path, output_json_file)

    dataset_path = 'ICL_dataset/UniGeo/proving_test.pk'
    output_json_file = 'LLM_eval/eval_UniGeo_Prove_test.json'
    process_unigeo_prove(dataset_path, output_json_file)