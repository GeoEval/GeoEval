# coding:utf-8
# Author: Jiaxin
# Date: Dec-8-2023

"""This file provides methods to combine the "diagram_description", "text", "choice_list", etc."""

DIAGRMA_PREFIX =  "Here are the basic description of the diagram: "
CHOICE_PREFIX = "The Choices are: "

def naive_merge(diagram_description: dict, text: dict, choice_list: list) -> str:
    """Naive merge method, just combine all together."""
    to_merge_diagram_description = ""
    to_merge_text = ""
    to_merge_choice = ""
    
    if diagram_description != None:
        temp = ", ".join(diagram_description["structure"]) + ", ".join(diagram_description["semantic"])
        to_merge_diagram_description = f"{DIAGRMA_PREFIX} {temp}"
        
    if text != None:
        to_merge_text = text["Num_Exp"]
    
    if choice_list != None:
        temp = "[" + ", ".join(choice_list) + "]"
        to_merge_choice = f"{CHOICE_PREFIX} {temp}"
    
    return to_merge_diagram_description + to_merge_text + to_merge_choice