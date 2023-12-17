from util import process_geometry3k_pgps9k_json_file
if __name__ == '__main__':
    dataset_path = 'ICL_dataset/PGPS9K_all/Geometry3K/new-test.json'
    output_json_file = 'LLM_eval/eval_Geometry3k_test.json'
    process_geometry3k_pgps9k_json_file(dataset_path, output_json_file)
    
    dataset_path = 'ICL_dataset/PGPS9K_all/PGPS9K/new-test.json'
    output_json_file = 'LLM_eval/eval_PGPS9K_test.json'
    process_geometry3k_pgps9k_json_file(dataset_path, output_json_file)