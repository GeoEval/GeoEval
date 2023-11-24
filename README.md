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

To get started with this project, you need to download the initial dataset from [Google Cloud Drive](https://drive.google.com/file/d/13xWRtt_C4jpA3F8NZ3deR089I3s17_WK/view?usp=drive_link). Follow the steps below to download the dataset:


### Preprocess Data

Place the dataset in the workspace, and then run the following code:

```python
python tool\process_geometry3k_pgps9k.py
python tool\process_unigeo_cat_prove.py
```


## Model Evaluation

Run the scripts under sh_files/{dataset} to achieve inference responsiveness, result extraction, and metric calculation for large models.

```bash
bash pgps9k/get_response.sh
bash pgps9k/ext_result.sh
bash pgps9k/ext_result
```

### Results


| Model Name      | Numeric Accuracy |
|-----------------|------------------|
| GPT3.5-turbo         | 0.95             |
| ---         | ---            |
| ---        | ---            |




