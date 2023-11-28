GeoQA_PROMPT_DICT = {
    "prompt_with_choice": (
        "You are a problem-solving bot, and now I ask you to solve a geometry problem. The problem is as follows: \n\n"
        "Provide the answer to the question and a detailed reasoning process. \n\n"
        "The question is: \n{subject}\n\nThe Choices are::\n{choices}\n\nThe Answer and the Reason Process is: \n\n"
    ),
    "prompt_without_choice": (
        "You are a problem-solving bot, and now I ask you to solve a geometry problem. The problem is as follows: \n\n"
        "Provide the answer to the question and a detailed reasoning process. \n\n"
        "The question is: \n{subject}\n\nThe Answer and the Reason Process is:"
    ),
}

Geometry3K_PROMPT_DICT = {
    "prompt_with_sem_seqs_with_choice": (
        "You are a problem-solving bot, and now I ask you to solve a geometry problem. The problem is as follows:\n\n"
        "Provide the answer to the question and a detailed reasoning process. \n\n"
        "The following statement declares the set elements in the image. \n{parsing_stru_seqs}\n\n"
        "The following statement declares the numerical and semantic relationships of the set elements in the image. \n{parsing_sem_seqs}\n\n"
        "The question is: \n{text}\n\nThe Choices are::\n{choices}\n\nThe Answer and the Reason Process is:"
    ),
    "prompt_without_sem_seqs_with_choice": (
        "You are a problem-solving bot, and now I ask you to solve a geometry problem. The problem is as follows: \n\n"
        "Provide the answer to the question and a detailed reasoning process. \n\n"
        "The following statement declares the set elements in the image. \n{parsing_stru_seqs}\n\n"
        "The question is: \n{text}\n\nThe Choices are::\n{choices}\n\nThe Answer and the Reason Process is:"
    ),
    "prompt_with_sem_seqs_without_choice": (
        "You are a problem-solving bot, and now I ask you to solve a geometry problem. The problem is as follows:\n\n"
        "Provide the answer to the question and a detailed reasoning process. \n\n"
        "The following statement declares the set elements in the image. \n{parsing_stru_seqs}\n\n"
        "The following statement declares the numerical and semantic relationships of the set elements in the image. \n{parsing_sem_seqs}\n\n"
        "The question is: \n{text}\n\nThe Answer and the Reason Process is:"
    ),
    "prompt_without_sem_seqs_without_choice": (
        "You are a problem-solving bot, and now I ask you to solve a geometry problem. The problem is as follows: \n\n"
        "Provide the answer to the question and a detailed reasoning process. \n\n"
        "The following statement declares the set elements in the image. \n{parsing_stru_seqs}\n\n"
        "The question is: \n{text}\n\nThe Answer and the Reason Process is:"
    ),
}

UniGeo_Cat_Prompt_DICT = {
    "prompt_with_choice": (
        "You are a problem-solving bot, and now I ask you to solve a geometry problem. The problem is as follows: \n\n"
        "Provide the answer to the question and a detailed reasoning process. \n\n"
        "The question is: \n{English_problem}\n\nThe Choices are::\n{choice_nums}\n\nThe Answer and the Reason Process is:"
    ),
    "prompt_without_choice": (
        "You are a problem-solving bot, and now I ask you to solve a geometry problem. The problem is as follows: \n\n"
        "Provide the answer to the question and a detailed reasoning process. \n\n"
        "The question is: \n{English_problem}\n\nThe Answer and the Reason Process is:"
    ),
}

UniGeo_Prove_Prompt_DICT = {
    "prompt_prove": (
        "You are a problem-solving bot, and now I ask you to solve a geometry problem. The problem is as follows: \n\n"
        "Provide the answer to the question and a detailed reasoning process. \n\n"
        "The following statement declares the set elements in the image. \n{statement}\n\n"
        "The question is: \n{question}\n\nThe Answer and the Reason Process is:"
    ),
}