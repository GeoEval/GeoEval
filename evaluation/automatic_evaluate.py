# coding:utf-8

import re
import sys
import json

from pathlib import Path
from typing import Any
MAIN_PATH = Path(__file__).absolute().parent.parent
sys.path.insert(0, str(MAIN_PATH))
print(sys.path)

from argparse import ArgumentParser

from evaluation.help_func import AverageMeter, safe_equal

def count(args):
    with open(args.path, mode="r", encoding="utf-8") as file:
        predictions = json.load(file)
    
    formal_knowledge_point = {"other": 0}
    knowledge_point = {"other": 0}
    geometry = {"other": 0}
    problem_length = {20: 0, 40: 0, 60: 0, 80: 0, 100: 0, 200: 0}
    for prob_id, instance in predictions.items():
        if instance["formal_knowledge_point"] != None:
            for f_k_p in instance["formal_knowledge_point"]:
                if f_k_p not in formal_knowledge_point:
                    formal_knowledge_point[f_k_p] = 1
                else:
                    formal_knowledge_point[f_k_p] += 1
        else:
            formal_knowledge_point["other"] += 1
            
        if instance["knowledge_point"] != None:
            if type(instance["knowledge_point"]) != list:
                k_p = instance["knowledge_point"] 
            else:
                try:
                    k_p = instance["knowledge_point"][0]
                except Exception as e:
                    k_p = "other"
            if k_p not in knowledge_point:
                knowledge_point[k_p] = 1
            else:
                knowledge_point[k_p] += 1
        else:
            knowledge_point["other"] +=1
                    
        if instance["geometry_shape"] != None:
            if instance["geometry_shape"] not in geometry:
                geometry[instance["geometry_shape"]] = 1
            else:
                geometry[instance["geometry_shape"]] += 1
        else:
            geometry["other"] +=1
        
        prob_len = len(instance["text"]["Num_Exp"].split(" "))
        if prob_len <= 20:
            problem_length[20] +=1
        elif prob_len <= 40:
            problem_length[40] +=1
        elif prob_len <= 60:
            problem_length[60] +=1
        elif prob_len <= 80:
            problem_length[80] += 1
        elif prob_len <= 100:
            problem_length[100] +=1
        else:
            problem_length[200] +=1
            
        # if prob_len not in problem_length:
        #     problem_length[prob_len] = 1
        # else:
        #     problem_length[prob_len] +=1
            
    # print(formal_knowledge_point, end="\n\n")
    # print(knowledge_point, end="\n\n")
    # print(geometry)
    print(sorted(problem_length.items(), key=lambda x: x[0]))

class AutomaticMetrics:
    
    def __init__(self, path, model_key, tag):
        
        with open(path, mode="r", encoding="utf-8") as file:
            self.predictions = json.load(file)
        
        self.model_key = model_key
        self.tag = tag
        
    def _initialize(self, tag):
        if tag == "subjects":
            return {
                "Other": AverageMeter(),
                "Angle": AverageMeter(),
                "Triangle": AverageMeter(),
                "Length": AverageMeter(),
                "Line": AverageMeter(),
                "Quad": AverageMeter(),
                "Circle": AverageMeter(),
                "Area": AverageMeter(),
                "Ratio": AverageMeter(),
                "Cone": AverageMeter(),
                "Sphere": AverageMeter(),
                "Prism": AverageMeter(),
                "Cylinder": AverageMeter(),
                "Cube": AverageMeter(),
                "Cuboid": AverageMeter()
            }
        elif tag == "semantic":
            return {
                "formal_language": AverageMeter(),
                "natural_language": AverageMeter()
            }
        elif tag == "external_knowledge":
            return {
                "require": AverageMeter(),
                "no_require": AverageMeter()
            }
        elif tag == "problem_length":
            return {
                "<=20": AverageMeter(),
                "<=40": AverageMeter(),
                "<=60": AverageMeter(),
                "<=80": AverageMeter(),
                "<=100": AverageMeter(),
                # "<=120": AverageMeter(),
                # "<=140": AverageMeter(),
                # "<=160": AverageMeter(),
                ">100": AverageMeter(),
            }, {
                "<=40": AverageMeter(),
                "<=80": AverageMeter(),
                "<=120": AverageMeter(),
                "<=160": AverageMeter(),
                ">160": AverageMeter(),
            }
    
    def get_golden_pred_val(self, instance):
        extract = instance["solution"][self.model_key]["extraction"]
        answer_value = instance["answer_value"]
        
        return answer_value, extract
        
    def calculate_formal_knowledge_point(self, predictions):
        subject_metrics = self._initialize("subjects")
        for prob_id, instance in predictions.items():
            answer_value, extract = self.get_golden_pred_val(instance)
            subject = instance["formal_knowledge_point"]
            subject_2 = instance["geometry_shape"]
            
            val = 1 if safe_equal(extract, answer_value) else 0
            
            if subject == None:
                subject_metrics["Other"].update(val)
            else:
                for sub in subject:
                    subject_metrics[sub].update(val)
                
            if subject != subject_2:
                subject_metrics[subject_2].update(val)
            
        return subject_metrics

    def calculate_semantic_formal(self, predictions):
        semantic_metrics = self._initialize("semantic")
        for prob_id, instance in predictions.items():
            answer_value, extract = self.get_golden_pred_val(instance)
            
            val = 1 if safe_equal(extract, answer_value) else 0
            
            if instance["diagram_description"] == None:
                semantic_metrics["formal_language"].update(val)
            else:
                semantic_metrics["natural_language"].update(val)
        
        return semantic_metrics

    def calculate_external_knowledge(self, predictions):
        regex_1 = re.compile(r"C\d+")
        regex_2 = re.compile(r"C_\d+")
        regex_3 = re.compile(r"3.14")
        
        external_metrics = self._initialize("external_knowledge")
        for prob_id, instance in predictions.items():
            answer_val, extract = self.get_golden_pred_val(instance)
            
            val = 1 if safe_equal(extract, answer_val) else 0
            if instance["solution"]["program"] != None:
                if re.search(regex_1, instance["solution"]["program"]) or re.search(regex_2, instance["solution"]["program"]):
                    external_metrics["require"].update(val)
                else:
                    external_metrics["no_require"].update(val)
            else:
                if instance["dataset_name"] == "GeometryQA":
                    if re.search(regex_3, instance["solution"]["equation"]):
                        external_metrics["require"].update(val)
                    else:
                        external_metrics["no_require"].update(val)
                elif instance["dataset_name"] == "MATH-Geometry":
                    if re.search(regex_3, instance["solution"]["cot"]):
                        external_metrics["require"].update(val)
                    else:
                        external_metrics["no_require"].update(val)
        
        return external_metrics

    def calculate_problem_diagram_length(self, predictions):
        problem_length_metircs, diagram_length_metrics = self._initialize("problem_length")
        for prob_id, instance in predictions.items():
            answer_val, extract = self.get_golden_pred_val(instance)
            
            val = 1 if safe_equal(extract, answer_val) else 0
            
            prob_len = len(instance["text"]["Num_Exp"].split(" "))
            if instance["diagram_description"] != None:
                diagram_len = len(
                    (" ".join(instance["diagram_description"]["structure"])).split(" ")
                    ) + len(
                        (" ".join(instance["diagram_description"]["semantic"]).split(" "))
                    )
        
            if prob_len <= 20:
                problem_length_metircs["<=20"].update(val)
            elif prob_len <= 40:
                problem_length_metircs["<=40"].update(val)
            elif prob_len <= 60:
                problem_length_metircs["<=60"].update(val)
            elif prob_len <= 80:
                problem_length_metircs["<=80"].update(val)
            elif prob_len <= 100:
                problem_length_metircs["<=100"].update(val)
            # elif prob_len <= 120:
            #     problem_length_metircs["<=120"].update(val)
            # elif prob_len <= 140:
            #     problem_length_metircs["<=140"].update(val)
            # elif prob_len <= 160:
            #     problem_length_metircs["<=160"].update(val)
            else:
                problem_length_metircs[">100"].update(val)

            if diagram_len <= 40:
                diagram_length_metrics["<=40"].update(val)
            elif diagram_len <= 80:
                diagram_length_metrics["<=80"].update(val)
            elif diagram_len <= 120:
                diagram_length_metrics["<=120"].update(val)
            elif diagram_len <= 160:
                diagram_length_metrics["<=160"].update(val)
            else:
                diagram_length_metrics[">160"].update(val)
    
        return problem_length_metircs, diagram_length_metrics
 
    def __call__(self):
        res = {}
        if "subjects" in self.tag:
            res["subjects"] = self.calculate_formal_knowledge_point(self.predictions)
        
        if "semantic" in self.tag:
            res["semantic"] = self.calculate_semantic_formal(self.predictions)
        
        if "external_knowledge" in self.tag:
            res["external_knowledge"] = self.calculate_external_knowledge(self.predictions)
        
        if "problem_length" in self.tag:
            res["problem_length"], res["diagram_length"] = self.calculate_problem_diagram_length(self.predictions)
        
        self.output(res)

    def output(self, res):
        for tag, results in res.items():
            print("\n", f"Tag: {tag}")
            for key, metric_fn in results.items():
                print(f"\t{key}: {metric_fn.get_avg():.2f}")
            print("\n", "*"*50)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--path", type=str)
    args = parser.parse_args()
    args.path = "/Users/knight/Code/1_PHD_CODE/1_Important/ACL-2024-Collaboration/GeoEval/datas/results/eval_GeoEval_result_demo.json"
    
    # count(args)
    
    evaluate = AutomaticMetrics(args.path, "gpt35-turbo", ["subjects", "semantic", "external_knowledge", "problem_length"])
    evaluate()