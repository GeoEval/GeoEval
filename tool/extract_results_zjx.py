# coding:utf-8

import re
import json
import codecs

from argparse import ArgumentParser

def extract_codegen2(instance):
    prediction = instance["Response"]

def extract_instructblip(instance):
    extraction = instance["predictions"]
    instance["extraction"] = extraction
    return instance

def extract_llava(instance):
    prediction = instance["predictions"]
    
    # basic search: the answer is xxx 10.0
    p_match_1 = re.search(r"the (?:correct)?.?answer is.*(\d+(?:.\d+)?)", prediction, re.IGNORECASE)
    if p_match_1 != None:
        return p_match_1.group(1)    

    num_exp = instance["text"]["Num_Exp"]
    target_name = re.search(r"Find ([A-Za-z]+)", num_exp, re.IGNORECASE)
    if target_name != None:
        target_name = target_name.group(1)
        p_match_2 = re.search(f"{target_name} = (\d+(?:.\d+)?)", prediction)
        
        if p_match_2 != None:
            return p_match_2.group(1)

        p_match_2 = re.search(f"{target_name} is (?:approximately)? (\d+(?:.\d+)?)", prediction)
        if p_match_2 != None:
            return p_match_2.group(1)

    target_name = re.search(r"[what|find] is the value of ([A-Za-z]+)", num_exp, re.IGNORECASE)
    if target_name != None:
        target_name = target_name.group(1)
        p_match_2 = re.search(f"{target_name} = (\d+(?:.\d+)?)", prediction)
        
        if p_match_2 != None:
            return p_match_2.group(1)

        p_match_2 = re.search(f"{target_name} is [(equal to)?|(?:approximately)?] (\d+(?:.\d+)?)", prediction)
        if p_match_2 != None:
            return p_match_2.group(1)

    target_name = re.search(r"what is ([A-Za-z]+)", num_exp, re.IGNORECASE)
    if target_name != None:
        target_name = target_name.group(1)
        p_match_2 = re.search(f"{target_name} = (\d+(?:.\d+)?)", prediction)
        
        if p_match_2 != None:
            return p_match_2.group(1)

        p_match_2 = re.search(f"{target_name} is [(equal to)?|(?:approximately)?] (\d+(?:.\d+)?)", prediction)
        if p_match_2 != None:
            return p_match_2.group(1)

    target_name = re.search(r"Solve for ([A-Za-z]+)", num_exp, re.IGNORECASE)
    if target_name != None:
        target_name = target_name.group(1)
        p_match_2 = re.search(f"{target_name} = (\d+(?:.\d+)?)", prediction)
        
        if p_match_2 != None:
            return p_match_2.group(1)

        p_match_2 = re.search(f"{target_name} is [(equal to)?|(?:approximately)?] (\d+(?:.\d+)?)", prediction)
        if p_match_2 != None:
            return p_match_2.group(1)
        
        target_name_alias = re.search(f'{target_name} "([a-z])"', prediction)
        if target_name_alias != None:
            target_name_alias = target_name_alias.group(1)
            p_match_2 = re.search(f"{target_name_alias} is [(equal to)?|(?:approximately)?] (\d+(?:.\d+)?)", prediction)
            if p_match_2 != None:
                return p_match_2.group(1)

    target_name_2 = re.search(r"([A-Z]{2,3}) is \(\)", num_exp)
    if target_name_2 != None:
        
        if len(target_name_2.group(1)) == 2:
            l1 = target_name_2.group(1)[0]
            l2 = target_name_2.group(1)[1]
   
            p_match_3 = re.search(f"{l1}{l2} is (\d+(?:.\d+)?)", prediction)
            if p_match_3 != None:
                return p_match_3.group(1)
            
        else:
            p_match_4 = re.search(f"{target_name_2.group(1)} is (\d+(?:.\d+)?)", prediction)
            if p_match_4 != None:
                return p_match_4.group(1)
    
    target_name_3 = re.search(r"find the [value|length] of ([A-Za-z]{1,3})", num_exp, re.IGNORECASE)
    if target_name_3 != None:
        p_match_5 = re.search(f"{target_name_3.group(1)} [is|=] (?:approximately)? (\d+(?:.\d+)?)", prediction)
        if p_match_5 != None:
            return p_match_5.group(1)
    
    target_name_4 = re.search(r"Find the measure of \\angle (\d+)", num_exp, re.IGNORECASE)
    if target_name_4 != None:
        p_match_6 = re.search(f"The measure of angle {target_name_4.group(1)} .* (\d+(?:.\d+)?) degrees", prediction)
        if p_match_6 != None:
            return p_match_6.group(1)

    target_name_5 = re.search(r"What is (?:the measure of)? ([a-z] \\angle [A-Z]+)", num_exp, re.IGNORECASE)
    if target_name_5 != None:
        target_name_5_temp = target_name_5.group(1).replace("\\", "\\\\")
        p_match_7 = re.search(f"{target_name_5_temp} .* [is|=] .* (\d+(?:.\d+)?) (degrees)?", prediction)
        if p_match_7 != None:
            return p_match_7.group(1) 

        target_name_5_temp = target_name_5.group(1).replace("\\", "")
        p_match_7 = re.search(f"{target_name_5_temp} .* [is|=] .* (\d+(?:.\d+)?) (degrees)?", prediction)
        if p_match_7 != None:
            return p_match_7.group(1) 

    target_name_6 = re.search(r"[What is|Determine] (?:the measure of)? ([A-Za-z]+)", num_exp, re.IGNORECASE)
    if target_name_6 != None:
        p_match_8 = re.search(f"{target_name_6.group(1)} .* [is|=] .* (\d+(?:.\d+)?) cm", prediction)
        if p_match_8 != None:
            return p_match_8.group(1) 

    # print(num_exp)
    # print("*"*10)
    # print(prediction)
    # print()
    # print("-"*10)
    # print()
    # input()
    return None
            
def extract_answer(instance, model_name):
    if model_name == "codegen2":
        pass
    
    elif model_name == "instructblip":
        pass
    
    elif model_name == "llava":
        return extract_llava(instance)
    
    else:
        raise NotImplementedError(f"Not support: {model_name}")

def main(args):
    with codecs.open(args.predict_file, "r", "utf-8") as file:
        instances = json.load(file)
    
    c = 0
    for key, instance in instances.items():
        extraction = extract_answer(instance, model_name=args.model_name)
        if extraction != None:
            c +=1
        instance["extration"] = extraction
    
    with codecs.open(args.save_file, "w", "utf-8") as file:
        json.dump(instances, file, indent=2, ensure_ascii=False)
    
    print(c / len(instances))

if __name__ == "__main__":
    parser = ArgumentParser()
    
    parser.add_argument("--predict_file", type=str)
    parser.add_argument("--model_name", type=str)
    
    args = parser.parse_args()
    args.predict_file = "../datas/results/llava-v1.5-7b.json"
    args.save_file = "../datas/results/llava-v1.5-7b-extracted.json"
    args.model_name = "llava"
    main(args)