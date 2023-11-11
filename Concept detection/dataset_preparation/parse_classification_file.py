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

def prepare_dataframe():
    with open('Curriculum documents/annotated_descriptions.txt', 'r') as file:
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
            samples.append((description.replace('•', '').strip(), classes))
            description = None

    dataset = convert_to_single_label_classification(samples)
    return dataset

if __name__ == '__main__':
    prepare_dataframe().to_csv('manually_annotated.csv')