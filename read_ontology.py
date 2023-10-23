import json

from rdflib import Graph, Namespace

import description_parser

ignored_relations = [
    "http://example.org/relations/child",
    "http://www.w3.org/2000/01/rdf-schema#subClassOf",
]

def find_parent(graph, uri):
    query = "SELECT * WHERE {<" + str(uri) + "> rdfs:subClassOf ?parent }"
    result = graph.query(query)
    for stmt in result:
        return stmt['parent']
    return None

def find_links_with_definitoins(graph, uri):
    query = "SELECT * WHERE {<" + str(uri) + "> <http://www.w3.org/2004/02/skos/core#definition> ?definitionURL }"
    result = graph.query(query)
    links = []
    for stmt in result:
        links.append(stmt['definitionURL'])
    return links

def find_label(graph, uri):
    query = "SELECT * WHERE {<" + str(uri) + "> rdfs:label ?l }"
    result = graph.query(query)
    for stmt in result:
        return stmt['l']
    return uri.split("/")[-1]

def find_alt_label(graph, uri):
    query = "SELECT * WHERE {<" + str(uri) + "> <http://www.w3.org/2004/02/skos/core#altLabel> ?l }"
    result = graph.query(query)
    for stmt in result:
        return stmt['l']
    return uri.split("/")[-1]

def get_all_concepts(graph):
    query = "SELECT * WHERE {?c rdf:type owl:Class }"
    concepts = []
    result = graph.query(query)
    for stmt in result:
        concept_uri = stmt['c']
        concepts.append(concept_uri)
    return concepts

def get_data_from_wikipedia(concept):
    links = concept['definitionLinks']
    english_label = ""
    english_definition = ""
    slovene_label = ""
    slovene_definition = ""
    for link in links:
        if link.startswith("https://en.wikipedia.org/wiki/"):
            
            pass
def read_ontology(ontology_path, json_path):
    # define results
    properties = {}
    classes = {}

    f = open(json_path)
    existing_data_from_json = json.load(f)

    graph = Graph()
    graph.parse(ontology_path, format='ttl')

    all_concepts = get_all_concepts(graph)

    count = 0

    for concept_id in all_concepts:
        # define basic properties of a concept
        concept = {}
        concept['label'] = find_label(graph, concept_id)
        for e in existing_data_from_json:
            if e['name'] == concept['label']:
                concept['wikidata'] = e['wikidata']
        concept['index'] = find_alt_label(graph, concept_id)
        concept['parent'] = find_parent(graph, concept_id)
        concept['definitionLinks'] = find_links_with_definitoins(graph, concept_id)

        query = "SELECT * WHERE {<"+str(concept_id)+"> rdfs:subClassOf ?a . "+\
                "?a owl:someValuesFrom ?o . "+\
                "?a owl:onProperty ?p "+\
                "}"

        result = graph.query(query)
        for stmt in result:
            target = stmt['o']
            property = stmt['p']

            if property not in properties:
                properties[property] = {'label': find_label(graph, property)}

            count += 1
            print(count, find_label(graph, concept_id), find_label(graph, str(property)), find_alt_label(graph, str(target)))
    pass

if __name__ == '__main__':
    read_ontology('ontologies/SemSEX1.ttl', 'ontologija_opisi.json')