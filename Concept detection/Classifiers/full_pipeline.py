from collections import Counter

import fitz
import torch
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
import torch.nn.functional as F
from rdflib import Graph, URIRef, BNode, Literal, Namespace, RDF, RDFS, OWL, FOAF, SKOS, DC
from rdflib.extras.infixowl import Restriction

import dataset_preparation.parse_classification_file
from dataset_preparation.pdf_parser import get_non_annotated_text, get_dataset_for_binary_classification, generate_dataset
from Levenshtein import distance
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import precision_recall_fscore_support as score

def detect_concepts(sentences, return_tf=False):
    sentences_with_detected_concepts = []
    labels = [False, True]
    # model_path = "./Pretrained models/binary classifier"
    model_path = "./models/binary-classifier"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    results = []
    for sentence in sentences:
        tokens = tokenizer(sentence[0], return_tensors='pt')
        result = model(**tokens)
        result = result.logits.argmax()
        result = labels[result]
        if result:
            sentences_with_detected_concepts.append(sentence)
        results.append(result)
    if return_tf:
        return results
    else:
        return sentences_with_detected_concepts

labels = ['ss:adolescenca', 'ss:embrioloski_razvoj', 'ss:fiziologija', 'ss:higiena', 'ss:kontracepcija', 'ss:oploditev', 'ss:razmnozevanje', 'ss:socialne_spolne_oblike', 'ss:spolna_anatomija', 'ss:spolna_identiteta', 'ss:spolna_nedotakljivost', 'ss:seksologija', 'ss:spolni_izraz', 'ss:spolni_razvoj', 'ss:spolno_prenosljive_okuzbe_in_spolno_prenosljive_bolezni', 'ss:spolno_vedenje', 'ss:spolno_zdravje', 'ss:spolna_identiteta', 'ss:uzitek', 'ss:zgodovina_seksualnosti']
original_labels = ['Adolescenca', 'Embrionalni razvoj', 'Fiziologija', 'Higiena', 'Kontracepcija', 'Oploditev', 'Razmnoževanje', 'Socialne spolne oblike', 'Spolna anatomija', 'Spolna identiteta', 'Spolna nedotakljivost', 'Spolna vzgoja', 'Spolni izraz', 'Spolni razvoj', 'Spolno prenosljive okužbe in spolno prenosljive bolezni', 'Spolno vedenje', 'Spolno zdravje', 'Spolnostna identiteta', 'Užitek', 'Zgodovina seksologije']
original_labels_in_wikipedia = ['Adolescenca', 'Embrionalni razvoj', 'Fiziologija', 'Higiena',
 'Kontracepcija', 'Oploditev', 'Razmnoževanje', 'Socialne spolne oblike',
 'Spolna anatomija', 'Spolna identiteta', 'Spolna nedotakljivost',
 'Spolna vzgoja', 'Spolni izraz', 'Spolni razvoj',
 'Spolno prenosljive okužbe in spolno prenosljive bolezni',
 'Spolno vedenje', 'Spolno zdravje', 'Spolnostna identiteta', 'Užitek',
 'Zgodovina seksologije']
def classify_concepts(sentences, use_ontology_labels=True):
    wiki = True
    sentences_with_concepts = []
    # model_path = "./Pretrained models/concept classifier"
    if wiki:
        model_path = "./models/wiki-concept-classifier"
    else:
        model_path = "./models/concept-classifier"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    for sentence in sentences:
        tokens = tokenizer(sentence[0], return_tensors='pt')
        result = model(**tokens)
        result = result.logits.argmax()
        if use_ontology_labels:
            label = labels[result]
        else:
            if wiki:
                label = original_labels_in_wikipedia[result]
            else:
                label = original_labels[result]
        sentences_with_concepts.append(sentence + [label])
    return sentences_with_concepts

def read_a_curriculum_document(path):
    file = fitz.open(path)
    sentences = []
    for page in file:
        text = get_non_annotated_text(page)
        for t in text:
            sentences.append([t, path])
    return sentences

def build_ontology(classified_sentences):
    ss_namespace = Namespace("http://onto.clarin.si/semsex#")
    schema = Namespace("http://schema.org/")
    g = Graph()
    for sentence, source, concept in classified_sentences:
        node = BNode()
        g.add((node, RDF.type, ss_namespace[concept.split(":")[1]]))
        g.add((node, DC.source, Literal(source)))
        g.add((node, schema.text, Literal(sentence)))
    v = g.serialize(format="turtle")
    return v

def find_most_simmilar(sentences, sent):
    min_distance = -1
    best_sent = ""
    best_sent_idx = 0
    for i, s in enumerate(sentences):
        levenstein_dist = distance(sent, s)
        if min_distance < 0 or min_distance > levenstein_dist:
            min_distance = levenstein_dist
            best_sent = s
            best_sent_idx = i

    return best_sent_idx, best_sent, min_distance

def get_ground_truth(pdf_input_path, dataset_to_exclude):
    texts_to_exclude = set(dataset_to_exclude["text"])

    binary_classification_dataset = get_dataset_for_binary_classification()
    concept_classification_dataset = dataset_preparation.parse_classification_file.prepare_dataframe()
    sentences = read_a_curriculum_document(pdf_input_path)

    results = []

    for s in sentences:
        sent = s[0]
        contains_semsex = False
        concept = ""

        matching_binary_idx, matching_binary_text, matching_binary_distance = find_most_simmilar(list(binary_classification_dataset["text"]), sent)
        if matching_binary_text in texts_to_exclude:
            continue
        binary_label = binary_classification_dataset.iloc[matching_binary_idx]["label"]
        if binary_label:
            matching_label_idx, matching_label_text, matching_label_distance = find_most_simmilar(list(concept_classification_dataset["text"]), sent)
            if matching_label_text in texts_to_exclude:
                continue
            classification_label = concept_classification_dataset.iloc[matching_label_idx]["label"]

        results.append((sent, binary_label, classification_label if binary_label else ""))

    return results

def analyze_results(predicted, correct, average="binary", labels=None):
    # Calculate accuracy
    print("Counts: ", Counter(correct))

    accuracy = accuracy_score(correct, predicted)
    print("Accuracy:", accuracy)

    # Calculate precision
    precision = precision_score(correct, predicted, average=average)
    print("Precision:", precision)

    # Calculate recall (sensitivity)
    recall = recall_score(correct, predicted, average=average)
    print("Recall (Sensitivity):", recall)

    # Calculate F1-score
    f1 = f1_score(correct, predicted, average=average)
    print("F1-Score:", f1)


    precision, recall, fscore, support = score(correct, predicted, labels=labels)
    print('| {:>7s} | {:5s} |{:5s} | {:5s} | {:5s} |'.format("labels", "precision", "recall", "fscore", "support"))
    for i in range(len(labels)):

        print('| {:>7s} | {:1.3f} | {:1.3f} | {:1.3f} | {:1.3f} | '.format(str(labels[i]), precision[i], recall[i], fscore[i], support[i]))
        # print('precision: {}'.format(precision))
        # print('recall: {}'.format(recall))
        # print('fscore: {}'.format(fscore))
        # print('support: {}'.format(support))

def evaluate_pipeline(pdf_input_path):
    training_set = torch.load("training examples.pt")
    dataset = get_ground_truth(pdf_input_path, training_set)
    predicted_presence = detect_concepts(dataset, return_tf=True)
    ground_truth_presence = [x[1] for x in dataset]
    correct = [x == y for x, y in zip(ground_truth_presence, predicted_presence)]
    if len(correct) == 0:
        return
    accuracy = sum(correct) / len(correct)
    print("My accuracy:", accuracy)
    analyze_results(predicted_presence, ground_truth_presence, average="binary", labels=[True, False])

    print("Labels")

    predicted_labels = classify_concepts([list(x) for x in dataset if x[1]], use_ontology_labels=False)
    predicted_labels = [x[-1] for x in predicted_labels]
    ground_truth_labels = [x[2] for x in dataset if x[1]]
    analyze_results(predicted_labels, ground_truth_labels, average="micro", labels=original_labels)
    pass

def pipeline(pdf_input_path, output_path):
    sentences = read_a_curriculum_document(pdf_input_path)
    sentences = detect_concepts(sentences)
    sentences = classify_concepts(sentences)
    serialized_ontology = build_ontology(sentences)
    with open(output_path, 'w') as f:
        f.write(serialized_ontology)

if __name__ == '__main__':
    evaluate_pipeline("Curriculum documents/Curriculum pdf/1 UN_spoznavanje_okolja_pop-2.pdf")
    # all_documents = ['10 UN_glasbena_vzgoja.pdf', '13 UN_gospodinjstvo.pdf', '16 UN_naravoslovje.pdf', '2 UN_zgodovina.pdf', '5 UN_geografija.pdf', '8 UN_naravoslovje_in_tehnika.pdf',
    #                  '11 UN_Biologija.pdf', '14 UN_DDE_OS.pdf', '17 UN_sportna_vzgoja.pdf', '3 UN_fizika.pdf', '6 UN_matematika.pdf', '9 UN_likovna_vzgoja.pdf',
    #                  '12 UN_tehnika_tehnologija.pdf', '15 UN_druzba_OS.pdf', '1 UN_spoznavanje_okolja_pop-2.pdf', '4 UN_kemija.pdf', '7 UN_slovenscina.pdf']
    #
    # for document in all_documents:
    #     print(document)
    #     evaluate_pipeline("Curriculum documents/Curriculum pdf/" + document)
    #     # pipeline("Curriculum documents/Curriculum pdf/1 UN_spoznavanje_okolja_pop-2.pdf", 'SemSEX_extracted_concepts.ttl')