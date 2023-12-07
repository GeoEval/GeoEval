import torch
from tqdm import tqdm
device = "cuda" if torch.cuda.is_available() else "cpu"

def get_opensource_llm_reponse(data_loader, model, tokenizer):
    predictions = {}
    for feature in tqdm(data_loader):
        inputs = feature["input_ids"].to(device)
        # FIXME: since evaluation, we only consider batch_size=1, however, following [0] hard code tends to cause bug.
        o_len = feature["input_len"][0]
        pred = model.generate(inputs,
                        max_length=1024,
                        do_sample=True,
                        top_k=50,
                        top_p=0.5,
                        num_return_sequences=1,
                        pad_token_id=tokenizer.eos_token_id)
        return_text = tokenizer.decode(pred.cpu()[0], skip_special_tokens=True)[o_len:]
        # return_text_all = tokenizer.decode(pred.cpu()[0], skip_special_tokens=True)
        predictions[feature["id"][0]] = return_text
    return predictions