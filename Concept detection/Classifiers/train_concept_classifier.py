import torch
from torch import nn

from transformers import Trainer
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from datasets import Dataset
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from transformers import DataCollatorWithPadding
from transformers import TrainingArguments, Trainer
import evaluate
import numpy as np

from common import split_data
import dataset_preparation.parse_classification_file
from Classifiers.baseline_classifier import compute_baseline_score

def train_concept_classifier():
    text_column_name = "text"
    label_column_name = "label"

    # model_name = "EMBEDDIA/sloberta"
    model_name = "EMBEDDIA/crosloengual-bert"
    test_size = 0.2

    df = dataset_preparation.parse_classification_file.prepare_dataframe()
    # df = dataset_preparation.parse_classification_file.prepare_wikipedia_dataframe()

    le = preprocessing.LabelEncoder()
    le.fit(df[label_column_name].tolist())
    df['label'] = le.transform(df[label_column_name].tolist())
    number_of_classes = len(le.classes_)

    df_train, df_val, df_test = split_data(df, label_name='label', split_by_documents=False)

    train_dataset = Dataset.from_pandas(df_train)
    val_dataset = Dataset.from_pandas(df_val)
    test_dataset = Dataset.from_pandas(df_test)

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    def preprocess_function(examples):
        return tokenizer(examples[text_column_name], truncation=True)

    tokenized_train = train_dataset.map(preprocess_function, batched=True)
    tokenized_val = val_dataset.map(preprocess_function, batched=True)
    tokenized_test = test_dataset.map(preprocess_function, batched=True)

    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=number_of_classes)

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    metric = evaluate.load("accuracy")
    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        return metric.compute(predictions=predictions, references=labels)


    training_args = TrainingArguments(
        output_dir="./wiki-results",
        learning_rate=2e-5,
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        num_train_epochs=20,
        save_steps=50,
        weight_decay=0.001,
        evaluation_strategy="epoch",
        logging_strategy="epoch",
        save_strategy="no"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_val,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics

    )

    trainer.train()
    torch.save(model, "models/wiki-concepts.pt")
    trainer.save_model('models/wiki-concept-classifier')

    test_results = trainer.evaluate(tokenized_test)
    print("===============RESULTS==============")
    print(test_results)
    print("====================================")
    print()
    print("==============BASELINE==============")
    print(compute_baseline_score(df))
    print("====================================")

if __name__ == '__main__':
    train_concept_classifier()