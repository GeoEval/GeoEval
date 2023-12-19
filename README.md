# GeoEval
This is the Repository for Geometry Problem Solving Method Evaluation



## Overview

This project comprises a systematic evaluation of Geometry Problem Solving methods and the construction of synthetic datasets. The aim is to advance the field of solving geometry problems. The project is focused on the construction of datasets in the field of geometry problem solving and to provide a comprehensive evaluation of current large language models.

## Table of Contents

1. [Data Preparation](#data-preparation)
   - [Download Initial Dataset](#download-initial-dataset)
   - [Preprocess Data](#preprocess-data)
   
2. [Model Evaluation](#model-evaluation)


## Data Preparation

### Download Initial Dataset

To get started with this project, you need to download the initial dataset Contrain Geometry3K, PGPS9K, UniGeo from Google Cloud Drive[Dataset Collection](https://drive.google.com/file/d/13xWRtt_C4jpA3F8NZ3deR089I3s17_WK/view?usp=drive_link). GeoQA+ can be download from this dataset [link](https://drive.google.com/file/d/1KL4_wIzr3p8XSKMkkLgYcYwCbb0TzZ9O/view?usp=drive_link).  

In addition to that, there are also some text-based datasets, including [MathQA](https://drive.google.com/file/d/11E3ALsQxEtOPVtjKxrAwN99MIhtWl4No/view?usp=drive_link), [GeometryQA](https://github.com/DoubleBite/Sequence-to-General-tree/blob/master/data/geometryQA/geometry1398.json), and the [MATH](https://drive.google.com/file/d/1t4X03JIVXl6X_GNXl8R70W_rExJ_m_xD/view?usp=sharing) dataset, for geometry portion, please download here [MATH-Geometry](https://drive.google.com/file/d/1NaSMxlHM7zyBxW7cHV8ZSXeWLeDEpTIG/view?usp=sharing). These questions require a thorough understanding of geometric concepts and knowledge to solve.
```
ICL_Dataset
├── GeoQA
│   ├── GeoQA3
│   └── ...
├── GeoQA_Plus
│   ├── *.pk
├── PGPS9K_all
│   ├── Geometry3K
│   │   ├── train.json
│   │   └── test.json
│   ├── PGPS9K
│   │   ├── train.json
│   │   └── test.json
└── UniGeo
    ├── *.pk
```

The subsequent preprocessing steps need to be addressed, and below is the dataset provided in preprocessed [JSON format](https://drive.google.com/file/d/1ie8HJC5qdlY1pxn4H0peoV6A3TgHAbTx/view?usp=drive_link).


```

#### Download the Data Converted to Python by us

- [GeometryQA-Python (from MathQA)](https://drive.google.com/file/d/1xe8sE4s38RVHMOGgqnAztdtYCnXcRLF8/view?usp=sharing)

## Model Evaluation

Run the scripts under sh_files/{dataset} to achieve inference responsiveness, result extraction, and metric calculation for large models.

```bash
# PGPS9K Pipeline Example
bash pgps9k/get_response.sh
bash pgps9k/ext_result.sh
bash pgps9k/ext_result
```

## Caculation Prolem Results(Pure-Text Large Laugage Model)

### Mode with Multiple-Choice Questions Hint.
| Model Name             | Geometry3K | PGPS9K | UniGeo Caculation(GeoQA English) |
|:----------------------:|:----------:|:------:|:-------------------------------:|
| **Common Models**      |            |        |                                 |
| GPT3.5-turbo           | 0.55       |  ---   | 0.34                            |
| internlm-7b            | ---        | ---    | ---                             |
| internlm-20b           | ---        | ---    | ---                             |
| Qwen-7B                | ---        | ---    | ---                             |
| Qwen-14B               | ---        | ---    | ---                             |
| Baichuan2-7B-Base      | ---        | ---    | ---                             |
| Baichuan2-13B-Base     | ---        | ---    | ---                             |
| vicuna-7b              | ---        | ---    | ---                             |
| vicuna-13b             | ---        | ---    | ---                             |
| **Code Models**        |            |        |                                 |
| CodeLlama-7b           | ---        | ---    | ---                             |
| CodeLlama-13b          | ---        | ---    | ---                             |
| CodeGen-2b             | ---        | ---    | ---                             |
| CodeGen-6b             | ---        | ---    | ---                             |
| CodeGen-15b            | ---        | ---    | ---                             |
| **Math Models**        |            |        |                                 |
| WizardMath-7B-V1.0     | ---        | ---    | ---                             |
| WizardMath-13B-V1.0    | ---        | ---    | ---                             |
| MAmmoTH-70B            | ---        | ---    | ---                             |
| galactica-1.3b         | ---        | ---    | ---                             |
| galactica-6.7b         | ---        | ---    | ---                             |
| MetaMath-Mistral-7B    | ---        | ---    | ---                             |
| MetaMath-Llemma-7B     | ---        | ---    | ---                             |
| MetaMath-70B       | ---        | ---    | ---                             |



### Mode Without Multiple-Choice Questions Hint.
| Model Name             | GeoEval(test) |
|:----------------------:|:----------:|
| **Commercial Data Model**|            |
| **Common Models**      |            |
| GPT3.5-turbo           | 0.55       | 
| Llama2-70B-Chat        | ---        | 
| Qwen-70B-Chat          | ---        | 
| -70B-Chat              | ---        | 
| **Code Models**        |            |  
| CodeLlama-70B          | ---        |
| CodeGen2-16B           | ---        | 
| **Math Models**        |            |
| WizardMath-70B         | ---        | 
| MAmmoTH-70B            | ---        | 
| galactica-120B         | ---        | 
| MetaMath-70B           | ---        | 


## Caculation Prolem Results(Visual-Text Large Laugage Model)
| Model Name          | Geometry3K | PGPS9K | UniGeo Caculation(GeoQA English) |
|:-------------------:|:----------:|:------:|:-------------------------------:|
| visualglm-6b        | ---        | ---    | ---                             |
| llava-v1.5-7b       | ---        | ---    | ---                             |
| llama-adapter-7b    | ---        | ---    | ---                             |
| Qwen-VL             | ---        | ---    | ---                             |
| mPLUG-Owl           | ---        | ---    | ---                             |
| InstructBLIP        | ---        | ---    | ---                             |
| CogVLM              | ---        | ---    | ---                             |






