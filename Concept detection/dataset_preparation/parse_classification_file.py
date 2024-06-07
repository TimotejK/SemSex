import json

import nltk
import pandas as pd

# mode = random | double
def convert_to_single_label_classification(samples, mode='random'):
    result = []
    for text, labels in samples:
        if mode == 'random':
            result.append([text, labels[0]])
        else:
            for label in labels:
                result.append([text, label])
    return pd.DataFrame(result, columns=['text', 'label'])

def prepare_dataframe(raw_output=False):
    with open('Curriculum documents/annotated_descriptions.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    lines = list(map(lambda x: x.strip(), lines))
    samples = []
    description = None
    for line in lines:
        if line.startswith('-'):
            if description is not None:
                print("Error", line)
            description = line
        elif description is not None:
            # classes
            classes = list(map(lambda x: x.strip(), line.split(',')))
            samples.append((description.replace('-', '').strip(), classes))
            description = None
    if raw_output:
        return samples
    dataset = convert_to_single_label_classification(samples)
    return dataset


original_labels = ['Adolescenca', 'Embrionalni razvoj', 'Fiziologija', 'Higiena', 'Kontracepcija', 'Oploditev', 'Razmnoževanje', 'Socialne spolne oblike', 'Spolna anatomija', 'Spolna identiteta', 'Spolna nedotakljivost', 'Spolna vzgoja', 'Spolni izraz', 'Spolni razvoj', 'Spolno prenosljive okužbe in spolno prenosljive bolezni', 'Spolno vedenje', 'Spolno zdravje', 'Spolnostna identiteta', 'Užitek', 'Zgodovina seksologije']
def prepare_wikipedia_dataframe():
    ontology_translations = {
        "Embrionalni razvoj": "Embriološki razvoj",
        "Spolna vzgoja": "Spolno zdravje",
        'Spolno prenosljive okužbe in spolno prenosljive bolezni': "spolno prenosljive okužbe in spolno prenosljive bolezni",
        'Zgodovina seksologije': "Seksologija"
    }
    dataset = []
    f = open("json_ontology_descriptions.json", "r")
    ontology = json.load(f)
    for label in original_labels:
        concept = next((x for x in ontology if x["name"] == (ontology_translations[label] if label in ontology_translations else label)), None)
        if len(concept["texts"]) == 0:
            print("prazno")
        for text in concept["texts"]:
            sentences = nltk.sent_tokenize(text)
            for sentence in sentences:
                dataset.append([sentence, label])
            pass
        pass
    return pd.DataFrame(dataset, columns=['text', 'label'])

if __name__ == '__main__':
    prepare_wikipedia_dataframe()
    # prepare_dataframe()