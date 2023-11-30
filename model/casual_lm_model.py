from transformers import AutoModelForCausalLM, AutoTokenizer

# GPTNeoXForCausalLM.generate pythia-1b
# AutoModelForCausalLM.generate CodeGen-2b StarCoder-1b
# transformers.pipleline MAmmoTH-7B CodeLlama-7b
# vLLM.LLM WizardMath-7B-V1.0	 
def create_casuallm_model_tokenizer(args):
    model = AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path=args.weight_path, device_map="auto", trust_remote_code=True).cuda()
    model.eval()
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=args.weight_path, trust_remote_code=True)
    return model, tokenizer