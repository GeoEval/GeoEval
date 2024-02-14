# coding:utf-8
# Author: Jiaxin
# Date: Dec-8-2023

"""This file provides methods to combine the "diagram_description", "text", "choice_list", etc."""

DIAGRMA_PREFIX =  "Here are the basic description of the diagram: "
CHOICE_PREFIX = "The Choices are: "

def naive_merge(diagram_description: dict, text: dict, choice_list: list=None, aug: bool=False, back: bool=False) -> str:
    """Naive merge method, just combine all together."""
    to_merge_diagram_description = ""
    to_merge_text = ""
    to_merge_choice = ""
    
    if diagram_description != None:
        if not back:
            temp = ", ".join(diagram_description["structure"]) + "\n" + ", ".join(diagram_description["semantic"])
        else:
            temp = ", ".join(diagram_description["structure"]) + "\n" + ", ".join(diagram_description["backward_semantic"])
        to_merge_diagram_description = f"{DIAGRMA_PREFIX} {temp}"
        
    if text != None:
        if not back:
            to_merge_text = text["Num_Exp"] if not aug else text["aug_problem"]
        else:
            to_merge_text = text
    
    if choice_list != None:
        choice_list = [choice for choice in choice_list if choice != None]
        temp = "[" + ", ".join(choice_list) + "]"
        to_merge_choice = f"{CHOICE_PREFIX} {temp}"
    
    return to_merge_diagram_description + "\n" + to_merge_text + "\n" + to_merge_choice