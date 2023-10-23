from typing import Any

import pandas as pd
from datasets import Dataset
from pandas import DataFrame
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from transformers import DataCollatorWithPadding
from transformers import TrainingArguments, Trainer
import evaluate
import numpy as np

import common

# model_name = "distilbert-base-uncased"
# model_name = "EMBEDDIA/sloberta"
model_name = "EMBEDDIA/crosloengual-bert"

def prepare_dataset():
    data_path = "dataset.csv"
    label_column_name = "category"

    df = pd.read_csv(data_path)
    unique_classes = df[label_column_name].unique()
    one_vs_all_datasets = {}

    for class_label in unique_classes:
        # Create a binary classification dataset for 'class_label' vs. the rest
        df_binary = df.copy()
        df_binary['label'] = (df_binary[label_column_name] == class_label).astype(int)

        # Split the dataset into train and test sets
        df_train, df_val, df_test = common.split_data(df_binary, oversample=True, label_name='label', split_by_documents=False)


        one_vs_all_datasets[class_label] = {
            'train': df_train,
            'val': df_val,
            'test': df_test
        }
    return one_vs_all_datasets

def tokenize(one_vs_all_datasets: dict[Any, dict[str, DataFrame]], model_name: str):
    text_column_name = "text"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    def preprocess_function(examples):
        return tokenizer(examples[text_column_name], truncation=True)

    for key in one_vs_all_datasets:
        print(key)
        train_dataset = Dataset.from_pandas(one_vs_all_datasets[key]['train'])
        val_dataset = Dataset.from_pandas(one_vs_all_datasets[key]['val'])
        test_dataset = Dataset.from_pandas(one_vs_all_datasets[key]['test'])
        tokenized_train = train_dataset.map(preprocess_function, batched=True)
        tokenized_val = val_dataset.map(preprocess_function, batched=True)
        tokenized_test = test_dataset.map(preprocess_function, batched=True)
        train_model(tokenized_train, tokenized_val, tokenized_test, tokenizer, key)
        break

def train_model(tokenized_train, tokenized_val, tokenized_test, tokenizer, category_name):
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    metric = evaluate.load("accuracy")
    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        return metric.compute(predictions=predictions, references=labels)

    training_args = TrainingArguments(
        output_dir="./results",
        learning_rate=0.1,
        per_device_train_batch_size=2,
        per_device_eval_batch_size=2,
        num_train_epochs=5,
        weight_decay=0.001,
        evaluation_strategy="epoch",
        logging_strategy="epoch"
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

    trainer.save_model('one_vs_all/' + category_name)
    test_results = trainer.evaluate(tokenized_test)
    print(test_results)
    with open('results.txt', 'a') as out:
        out.write(str(test_results) + '\n')


if __name__ == '__main__':
    one_vs_all_datasets = prepare_dataset()
    tokenize(one_vs_all_datasets, model_name)