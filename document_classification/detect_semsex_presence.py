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
from document_classification.baseline_classifier import compute_baseline_score

data_path = "ucni_nacrti_oznaceno.csv"
text_column_name = "text"
label_column_name = "label"

# model_name = "distilbert-base-uncased"
model_name = "EMBEDDIA/sloberta"
test_size = 0.2
num_labels = 2

df = pd.read_csv(data_path)

le = preprocessing.LabelEncoder()
le.fit(df[label_column_name].tolist())
df['label'] = le.transform(df[label_column_name].tolist())
number_of_classes = len(le.classes_)

df_train, df_val, df_test = split_data(df, oversample=True, label_name='label', split_by_documents=False)
# df_train, df_test = train_test_split(df, test_size=test_size)

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
    output_dir="./results",
    learning_rate=2e-4,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=5,
    save_steps=15000,
    weight_decay=0.01,
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

print("==============BASELINE==============")
print(compute_baseline_score(df_test))
print("====================================")

trainer.train()

trainer.save_model('models/ucni_nacrti_model')

test_results = trainer.evaluate(tokenized_test)
print('===============RESULTS=================')
print(test_results)