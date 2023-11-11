import fitz
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
import torch.nn.functional as F
from rdflib import Graph, URIRef, BNode, Literal, Namespace, RDF, RDFS, OWL, FOAF, SKOS, DC
from rdflib.extras.infixowl import Restriction

from dataset_preparation.pdf_parser import get_non_annotated_text


def detect_concepts(sentences):
    sentences_with_detected_concepts = []
    labels = [False, True]
    model_path = "./Pretrained models/binary classifier"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    for sentence in sentences:
        tokens = tokenizer(sentence[0], return_tensors='pt')
        result = model(**tokens)
        result = result.logits.argmax()
        result = labels[result]
        if result:
            sentences_with_detected_concepts.append(sentence)
    return sentences_with_detected_concepts

def classify_concepts(sentences):
    sentences_with_concepts = []
    labels = ['ss:adolescenca', 'ss:embrioloski_razvoj', 'ss:fiziologija', 'ss:higiena', 'ss:kontracepcija', 'ss:oploditev', 'ss:razmnozevanje', 'ss:socialne_spolne_oblike', 'ss:spolna_anatomija', 'ss:spolna_identiteta', 'ss:spolna_nedotakljivost', 'ss:seksologija', 'ss:spolni_izraz', 'ss:spolni_razvoj', 'ss:spolno_prenosljive_okuzbe_in_spolno_prenosljive_bolezni', 'ss:spolno_vedenje', 'ss:spolno_zdravje', 'ss:spolna_identiteta', 'ss:uzitek', 'ss:zgodovina_seksualnosti']
    model_path = "./Pretrained models/concept classifier"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    for sentence in sentences:
        tokens = tokenizer(sentence[0], return_tensors='pt')
        result = model(**tokens)
        result = result.logits.argmax()
        label = labels[result]
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

def pipeline(pdf_input_path, output_path):
    sentences = read_a_curriculum_document(pdf_input_path)
    sentences = detect_concepts(sentences)
    sentences = classify_concepts(sentences)
    serialized_ontology = build_ontology(sentences)
    with open(output_path, 'w') as f:
        f.write(serialized_ontology)

if __name__ == '__main__':
    pipeline("Curriculum documents/Curriculum pdf/1 UN_spoznavanje_okolja_pop-2.pdf", 'SemSEX_extracted_concepts.ttl')