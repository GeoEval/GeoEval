import torch
from tqdm import tqdm
device = "cuda" if torch.cuda.is_available() else "cpu"

def get_opensource_llm_reponse(data_loader, model, tokenizer, sample_number, max_seq_length):
    predictions = {}
    count_number = sample_number
    for feature in tqdm(data_loader):
        if count_number == 0:   # if sample_number == -1, it will never count down to 0.
            break
        inputs = feature["input_ids"].to(device)
        # FIXME: since evaluation, we only consider batch_size=1, however, following [0] hard code tends to cause bug.
        assert inputs.size(0) == 1, print(f"Only support batch size equal to, however, get {inputs.size(0)}")
        o_len = feature["input_len"][0]
        pred = model.generate(inputs,
                        max_length=max_seq_length,
                        do_sample=True,
                        top_k=50,
                        top_p=0.5,
                        num_return_sequences=1,
                        pad_token_id=tokenizer.eos_token_id)
        return_text = tokenizer.decode(pred.cpu()[0], skip_special_tokens=True)[o_len:]
        return_text_all = tokenizer.decode(pred.cpu()[0], skip_special_tokens=True)

        meta_data = feature["meta_data"][0]
        data_id = meta_data["unique_id"]

        predictions[data_id] = {
                "Problem": meta_data["sentence"],
                "Response": return_text,
                "Response_all": return_text_all,
                "answer_value": meta_data["answer_value"],
                "choice_list": meta_data["choice_list"],
                "choice_id": meta_data["choice_id"],
                }
        
        for key, val in meta_data.items():
            if key not in predictions[data_id]:
                predictions[data_id][key] = val

        count_number -=1
    return predictions