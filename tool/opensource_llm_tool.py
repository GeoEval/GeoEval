def get_opensource_llm_reponse(question, model, tokenizer):
    inputs = tokenizer(question, return_tensors='pt')
    inputs = inputs.to('cuda')
    pred = model.generate(**inputs,
                          max_new_tokens=1024,
                          do_sample=True,
                          top_k=50,
                          top_p=0.5,
                          num_return_sequences=1)
    return_text = tokenizer.decode(pred.cpu()[0], skip_special_tokens=True)[len(question):]
    return return_text