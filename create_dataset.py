import json
import pandas as pd
import nltk.data

def create_dataset():
    f = open('ontologies/json_ontology_descriptions.json')
    data = json.load(f)
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    rows = []
    number_of_samples = {}
    for concept in data:
        target_class = concept['name']
        for document in concept['texts']:
            sentences = tokenizer.tokenize(document)
            for sentence in sentences:
                rows.append([sentence, target_class])
                if target_class in number_of_samples:
                    number_of_samples[target_class] += 1
                else:
                    number_of_samples[target_class] = 1
    rows = filter(lambda x: number_of_samples[x[1]] > 4, rows)
    df = pd.DataFrame(rows, columns=['text', 'category'])
    df.to_csv('dataset-filtrirano.csv')

if __name__ == '__main__':
    create_dataset()