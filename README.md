

# GeoEval
![MathQA](https://img.shields.io/badge/Task-MathQA-red) 
![Mathematical Reasoning](https://img.shields.io/badge/Task-Mathematical_Reasoning-red) 
![Multi-Modal](https://img.shields.io/badge/Task-Multi--Modal-red)  
![ChatGPT](https://img.shields.io/badge/Model-ChatGPT-green) 
![GPT-4](https://img.shields.io/badge/Model-GPT--4-green) 
![GPT-4V](https://img.shields.io/badge/Model-GPT--4V-green)

This is the Repository for Geometry Problem Solving Method Evaluation

Code for the Paper "GeoEval: Benchmark for Evaluating LLMs and Multi-Modal Models on Geometry Problem-Solving".


## Overview

This project comprises a LLM evaluation of Geometry Problem Solving methods and the construction of comprehensive datasets. The aim is to advance the field of solving geometry problems. The project is focused on the construction of datasets in the field of geometry problem solving and to provide a comprehensive evaluation of current large language models.

## About GeoEval
The GeoEval benchmark is specifically designed for assessing the ability of models in resolving geometric math problems. This benchmark features five characteristics: Comprehensive Variety, Varied Problems, Dual Inputs, Diverse Challenges, and Complexity Ratings.

For an insightful contrast, we offer a comparative analysis of GeoEval against earlier datasets.


The GeoEval benchmark is specifically designed for assessing the ability of models in resolving geometric math problems. This benchmark features five characteristics: Comprehensive Variety, Varied Problems, Dual Inputs, Diverse Challenges, and Complexity Ratings.

For an insightful contrast, we offer a comparative analysis of GeoEval against earlier datasets.


<p align="center">
<img src="img_bench/lidia.jpg" width="400"> <br>
</p>

GeoEval Benchmark Features
Comprehensive Variety: The benchmark covers a wide range of geometric topics, providing a comprehensive test for models.

__Varied Problems__: Problems in the benchmark are varied, testing the model's ability to handle different types of geometric problems.

<div style="text-align: inline-block;">
    <div style="display: inline-block;">
        <img src="img_bench/geostat1.jpg" width="250">
    </div>
    <div style="display: inline-block;">
        <img src="img_bench/geostat2.jpg" width="290">
    </div>
</div>

__Dual Inputs__: The benchmark includes both text and diagram inputs, testing the model's ability to process and integrate information from different sources.

__Diverse Challenges__: The benchmark poses diverse challenges, testing the model's ability to handle complex and varied geometric problems.

__Complexity Ratings__: The benchmark includes problems of different complexity levels, allowing for a nuanced assessment of the model's capabilities.



<p align="center">
<img src="img_bench/geoexample.jpg" width="400"> <br>
</p>
## Table of Contents

1. [Data Preparation](#data-preparation)
   - [Download Initial Dataset](#download-initial-dataset)
   - [Preprocess Data](#preprocess-data)
   
2. [Model Evaluation](#model-evaluation)


## Data Preparation


### Download Initial Dataset

To get started with this project, you need to download the initial dataset Contrain Geometry3K, PGPS9K, UniGeo from Google Cloud Drive[Dataset Collection](https://drive.google.com/file/d/13xWRtt_C4jpA3F8NZ3deR089I3s17_WK/view?usp=drive_link). GeoQA+ can be download from this dataset [link](https://drive.google.com/file/d/1KL4_wIzr3p8XSKMkkLgYcYwCbb0TzZ9O/view?usp=drive_link).  

In addition to that, there are also some text-based datasets, including [MathQA](https://drive.google.com/file/d/11E3ALsQxEtOPVtjKxrAwN99MIhtWl4No/view?usp=drive_link), [GeometryQA](https://github.com/DoubleBite/Sequence-to-General-tree/blob/master/data/geometryQA/geometry1398.json), and the [MATH](https://drive.google.com/file/d/1t4X03JIVXl6X_GNXl8R70W_rExJ_m_xD/view?usp=sharing) dataset, for geometry portion, please download here [MATH-Geometry](https://drive.google.com/file/d/1NaSMxlHM7zyBxW7cHV8ZSXeWLeDEpTIG/view?usp=sharing). These questions require a thorough understanding of geometric concepts and knowledge to solve.

### Download GeoVal-merge Dataset

1. Choose the merged data from the provided Google Drive [GeoEval](https://drive.google.com/file/d/1CpoZ3bFSxJXZxJhj0fmUp4ZxcR5TUdiu/view?usp=sharing).
2. Extract the selected data into the "LLM Eval" directory.
3. Notably, the "select.json" file serves as the test set for GeoEval, while "train.json" corresponds to the original training sets of various data sources, and "test.json" represents the original test sets of various data sources.

The backward reasoning dataset is on [GeoEval-backward-augmentation](https://drive.google.com/file/d/1Oj0z7mGbDBdBbvjP6gbmhAs1sP553Hz3/view?usp=sharing) This data is constructed using the backward-reasoning technique.
The rephrase augmentation dataset is on [GeoEval-rephase-aug-augmentation](https://drive.google.com/file/d/1Zprrw8Q-5t9g9iiI0b_eLoAwGM06YMw1/view?usp=drive_link) This data is constructed by rewriting the question description format and rearranging the order of options. 


## Model Evaluation

Run the scripts under sh_files/{model} to achieve inference responsiveness, result extraction, and metric calculation for large models.

```bash
bash sh_files/{model_name}/evaluate_general.sh
bash sh_files/{model_name}/ext_all.sh
bash sh_files/{model_name}/caculate_score.sh
bash sh_files/{model_name}/caculate_aug_score.sh
bash sh_files/{model_name}/caculate_back_score.sh
bash sh_files/{model_name}/caculate_solid_score.sh
bash sh_files/{model_name}/caculate_score.sh
```

##  🏆 Leaderboard 🏆

| Model                    | GeoEval-2000 (A/T %) | GeoEval-backward (A %) | GeoEval-aug (A %) | GeoEval-hard (A %) |
|--------------------------|----------------------|------------------------|-------------------|--------------------|
| CodeGen2-16B $\lozenge$  | 28.76 / 22.06         | 5.10                   | 8.50              | 5.66               |
| GPT-3.5 $\lozenge$       | 24.71 / 21.27         | 22.66                  | 41.25             | 22.33              |
| GPT-4 $\lozenge$         | 27.95 / 43.86         | 26.00                  | 45.75             | 10.10              |
| WizardMath-70B $\lozenge$| **55.67** / 34.20    | 28.66                  | 37.75             | 6.00               |
| WizardMath-7B-V1.1 $\lozenge$| 54.78 / 32.76    | 32.66                  | **47.75**         | 6.00               |
| llava-7B-V1.5            | 12.80 / 21.01         | 11.33                  | 20.25             | 20.30              |
| Qwen-VL                  | 25.60 / 25.97         | 5.66                   | 22.25             | 21.66              |
| mPLUG-Owl2               | 37.76 / n/a           | **35.33**               | 38.00             | **22.66**          |
| InstructBLIP $\dagger$   | **52.18** / n/a       | 15.66                  | 35.00             | **70.30**          |
| GPT-4V                   | 37.22 / **43.86** $\ddagger$ | 26.00            | 45.75             | 10.10              |
 






