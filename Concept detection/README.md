# SemSex - Concept detection

## Background
The aim of this project is to facilitate the analysis of curriculum plans, specifically focusing on the extraction of concepts related to sexual education.

### Task Definition
To automate the extraction of sexual education concepts from curriculum plans, we have defined two tasks.

**Concept Detection**
The first task involves detecting the presence of a concept mentioned in the curriculum description. The input is a short sentence describing one of the subject's goals, and the output is a binary classification indicating whether the description refers to a sexual education concept.

**Concept Classification**
Once the presence of an interesting concept is detected, the next task is to recognize which specific concept the description refers to. The concept classification task takes a short description of a subject's goal containing one of the target concepts as input and outputs a classification categorizing the description under one of the concepts in our ontology.

## Training
We built models for both tasks using large pretrained language models. As the curriculum texts are in Slovene, we utilized pretrained models with support for the Slovene language, including the *Sloberta* model and the *Cro-slo-engual BERT* model. We fine-tuned the hyperparameters on a validation dataset and evaluated the performance on a testing set.

## Results
The table below presents the results of our models:

| **Model**                  | **Test Accuracy** | **Baseline** |
|----------------------------|-------------------|--------------|
| **Concept Detection**      |                   |              |
| EMBEDDIA/crosloengual-bert |             0.912 |        0.500 |
| EMBEDDIA/sloberta          |             0.693 |        0.500 |
| **Concept Classification** |                   |              |
| EMBEDDIA/crosloengual-bert |             0.463 |        0.181 |
| EMBEDDIA/sloberta          |             0.529 |        0.181 |

## Running the Models
To replicate our training setup, use the provided scripts.

**Concept Detection**
To train the concept detection model, run the `Classifiers/train_binary_classifier.py` file using the command below.
```shell
python Classifiers/train_binary_classifier.py
```

**Concept Classification**
To train the concept classification model, run the `Classifiers/train_concept_classification.py` file using the command below.
```shell
python Classifiers/train_concept_classification.py
```