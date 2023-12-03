from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import AutoModel
from argparse import ArgumentParser
import os

# GPTNeoXForCausalLM.generate pythia-1b
# AutoModelForCausalLM.generate CodeGen-2b StarCoder-1b
# transformers.pipleline MAmmoTH-7B CodeLlama-7b
# vLLM.LLM WizardMath-7B-V1.0	 
def create_casuallm_model_tokenizer(args):
    model = AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path=args.weight_path, device_map="auto", trust_remote_code=True).cuda()
    model.eval()
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=args.weight_path, trust_remote_code=True)
    return model, tokenizer

def create_model_tokenizer(args: ArgumentParser, from_local: bool=True) -> tuple[AutoModel, AutoTokenizer]:
    if from_local:
        assert os.path.exists(args.weight_path), f"cannot find weight path: {args.weight_path}"
        model = AutoModel.from_pretrained(
            args.weight_path, load_in_8bit=args.load_in_8bit, trust_remote_code=True)
        model.eval()
        
        tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=args.weight_path, trust_remote_code=True)
        
    else:      
        model = AutoModel.from_pretrained(
            args.model_name, load_in_8bit=False, trust_remote_code=True, local_files_only=False
        )
        model.eval()
        tokenizer = AutoTokenizer.from_pretrained(args.model_name, trust_remote_code=False)
        
    return model, tokenizer