import json
import pandas as pd
import nltk.data

def create_dataset():
    f = open('ontologija_opisi.json')
    data = json.load(f)
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    rows = []
    for concept in data:
        target_class = concept['name']
        for document in concept['texts']:
            sentences = tokenizer.tokenize(document)
            for sentence in sentences:
                rows.append([sentence, target_class])
    df = pd.DataFrame(rows, columns=['text', 'category'])
    df.to_csv('datasaet.csv')

if __name__ == '__main__':
    create_dataset()