import json
import os
import re

import wikipedia
from rdflib import Graph, URIRef, BNode, Literal, Namespace, RDF, RDFS, OWL, FOAF, SKOS, XSD

import description_parser
from gather_text import name_formatter

ignored_relations = [
    "http://example.org/relations/child",
    "http://www.w3.org/2000/01/rdf-schema#subClassOf",
]


def find_parent(graph, uri):
    query = "SELECT * WHERE {<" + str(uri) + "> rdfs:subClassOf ?parent }"
    result = graph.query(query)
    for stmt in result:
        return str(stmt['parent'])
    return None


def find_links_with_definitoins(graph, uri):
    query = "SELECT * WHERE {<" + str(uri) + "> <http://www.w3.org/2004/02/skos/core#definition> ?definitionURL }"
    result = graph.query(query)
    links = []
    for stmt in result:
        links.append(str(stmt['definitionURL']))
    return links


def find_label(graph, uri):
    query = "SELECT * WHERE {<" + str(uri) + "> rdfs:label ?l }"
    result = graph.query(query)
    for stmt in result:
        return str(stmt['l'])
    return uri.split("/")[-1]


def find_alt_label(graph, uri):
    query = "SELECT * WHERE {<" + str(uri) + "> <http://www.w3.org/2004/02/skos/core#altLabel> ?l }"
    result = graph.query(query)
    for stmt in result:
        return str(stmt['l'])
    return uri.split("/")[-1]


def get_all_concepts(graph):
    query = "SELECT * WHERE {?c rdf:type owl:Class }"
    concepts = []
    result = graph.query(query)
    for stmt in result:
        concept_uri = stmt['c']
        concepts.append(concept_uri)
    return concepts


wiki_cache = {}


def get_data_from_wikipedia(concept):
    global wiki_cache
    json_path = "cached_wikipedia_info.json"
    if len(wiki_cache) == 0 and os.path.isfile(json_path):
        f = open(json_path)
        wiki_cache = json.load(f)

    if str(concept['label']) in wiki_cache:
        concept['labelEN'] = wiki_cache[str(concept['label'])]['labelEN']
        concept['labelSL'] = wiki_cache[str(concept['label'])]['labelSL']
        concept['definitionEN'] = wiki_cache[str(concept['label'])]['definitionEN']
        concept['definitionSL'] = wiki_cache[str(concept['label'])]['definitionSL']
    else:
        links = concept['definitionLinks']
        english_label = "TODO"
        english_definition = "TODO"
        slovene_label = concept['label']
        slovene_definition = "TODO"
        for link in links:
            if link.startswith("https://en.wikipedia.org/wiki/"):
                name = link[len("https://en.wikipedia.org/wiki/"):]
                wikipedia.set_lang("en")
                page = wikipedia.page(name_formatter(name, lang="en"))
                english_definition = page.summary
                english_label = page.title
            if link.startswith("https://sl.wikipedia.org/wiki/"):
                name = link[len("https://sl.wikipedia.org/wiki/"):]
                wikipedia.set_lang("sl")
                page = wikipedia.page(name_formatter(name, lang="sl"))
                slovene_definition = page.summary
                slovene_label = page.title

        wiki_cache[str(concept['label'])] = {
            'labelEN': english_label,
            'labelSL': slovene_label,
            'definitionEN': english_definition,
            'definitionSL': slovene_definition
        }
        concept['labelEN'] = english_label
        concept['labelSL'] = slovene_label
        concept['definitionEN'] = " ".join(english_definition.split())
        concept['definitionSL'] = " ".join(slovene_definition.split())

        s = json.dumps(wiki_cache)
        with open(json_path, "w") as outfile:
            outfile.write(s)
    return concept


def read_ontology(ontology_path, json_path):
    # define results
    objectProperties = {}
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
        if concept['label'] == "abstieneca":
            print("a")

        concept['wikidata'] = "TODO"
        for e in existing_data_from_json:
            if e['name'] == concept['label']:
                if 'wikidata' in e:
                    concept['wikidata'] = e['wikidata']
        concept['index'] = find_alt_label(graph, concept_id)
        concept['parent'] = find_parent(graph, concept_id)
        concept['definitionLinks'] = find_links_with_definitoins(graph, concept_id)

        # add wikipedia data
        concept = get_data_from_wikipedia(concept)

        # add object properties
        concept['objectProperties'] = []

        query = "SELECT * WHERE {<" + str(concept_id) + "> rdfs:subClassOf ?a . " + \
                "?a owl:someValuesFrom ?o . " + \
                "?a owl:onProperty ?p " + \
                "}"

        result = graph.query(query)
        for stmt in result:
            target = stmt['o']
            property = stmt['p']

            if property not in objectProperties:
                objectProperties[property] = {'label': find_label(graph, property)}

            concept['objectProperties'].append((str(property), str(target)))

            count += 1
            print(count, find_label(graph, concept_id), find_label(graph, str(property)),
                  find_alt_label(graph, str(target)))
        classes[str(concept_id)] = concept

    return objectProperties, classes


def address_from_name(name):
    name = "-".join([a.strip() for a in name.split("/")])
    name = name.lower().strip().replace(" ", "_")
    name = name.replace("(", "")
    name = name.replace(")", "")
    name = name.replace("č", "c")
    name = name.replace("š", "s")
    name = name.replace("ž", "z")
    return name


url_translations = {}


def translage_url_string(url: str, label=None):
    global url_translations
    custom_namespace = Namespace("http://onto.clarin.si/semsex#")
    if url in url_translations:
        return url_translations[url]

    if label is None:
        label = url.split("/")[-1]

    if url.startswith("http://example.org") or url.startswith("http://webprotege.stanford.edu"):
        uri_ref = custom_namespace[address_from_name(label)]
    else:
        uri_ref = URIRef(url)
    url_translations[url] = uri_ref
    return uri_ref


def write_object_properties(graph, object_proporties):
    for property in object_proporties:
        property_uri = translage_url_string(str(property), object_proporties[property]['label'])
        graph.add((property_uri, RDF.type, OWL.ObjectProperty))
        graph.add((property_uri, RDFS.label, Literal(object_proporties[property]['label'], lang='sl')))
        graph.add((property_uri, RDFS.label, Literal("TODO", lang='en')))
        graph.add((property_uri, SKOS.definition, Literal("TODO", lang='sl')))
        graph.add((property_uri, SKOS.definition, Literal("TODO", lang='en')))
        graph.add((property_uri, RDFS.domain, OWL.Thing))
        graph.add((property_uri, RDFS.range, OWL.Thing))


def write_data_properties(graph):
    usedProperties = {
        RDFS.isDefinedBy: ["opisano na URL-ju", "described at URL", ],
        OWL.sameAs: ["Isto kot", "Same as"],
        RDFS.subClassOf: ["Podtip", "Subclass of"],
        RDFS.label: ["Oznaka", "Label"],
        SKOS.definition: ["Definicija", "Definition"],
        SKOS.altLabel: ["Druga oznaka", "Alternative label"],
        RDF.type: ["tip", "type"],
    }
    for property_uri in usedProperties:
        graph.add((property_uri, RDF.type, OWL.DatatypeProperty))
        graph.add((property_uri, SKOS.definition, Literal("TODO", lang='sl')))
        graph.add((property_uri, SKOS.definition, Literal("TODO", lang='en')))
        graph.add((property_uri, RDFS.domain, OWL.Thing))
        graph.add((property_uri, RDFS.range, XSD.string))
        graph.add((property_uri, RDF.type, Literal(usedProperties[property_uri][0], lang='sl')))
        graph.add((property_uri, RDF.type, Literal(usedProperties[property_uri][1], lang='en')))


def write_classes(graph, classes):
    wd = Namespace("http://wikidata.org/entity/")
    for cls in classes:
        translage_url_string(cls, classes[cls]['label'])

    for cls in classes:
        cls_object = classes[cls]
        cls_uri = translage_url_string(cls, cls_object['label'])
        graph.add((cls_uri, RDF.type, OWL.Class))
        graph.add((cls_uri, OWL.sameAs, wd[cls_object['wikidata']]))
        if cls_object['parent'] is None:
            graph.add((cls_uri, RDFS.subClassOf, OWL.Thing))
        else:
            graph.add((cls_uri, RDFS.subClassOf, translage_url_string(cls_object['parent'])))
        graph.add((cls_uri, RDFS.label, Literal(cls_object['labelEN'], lang='en')))
        graph.add((cls_uri, RDFS.label, Literal(cls_object['labelSL'], lang='sl')))
        graph.add((cls_uri, SKOS.definition, Literal(cls_object['definitionEN'], lang='en')))
        graph.add((cls_uri, SKOS.definition, Literal(cls_object['definitionSL'], lang='sl')))
        graph.add((cls_uri, SKOS.altLabel, Literal(cls_object['index'], lang='sl')))

        for url in cls_object['definitionLinks']:
            graph.add((cls_uri, RDFS.isDefinedBy, Literal(url, datatype=XSD.string)))

        for property, target in cls_object['objectProperties']:
            graph.add((cls_uri, translage_url_string(property), translage_url_string(target)))

def edit_serialization(turtle_string):
    turtle_string = re.sub('([A-Z:a-z])+ a owl:DatatypeProperty,\s+"([^"]+)"@en *,\s+"([^"]+)"@sl *;', '\\1 a owl:DatatypeProperty;\n    rdfs:label "\\2"@en,\n    rdfs:label "\\3"@sl ;', turtle_string)
    return turtle_string

def generate_nice_ontology():
    object_propoerties, classes = read_ontology('ontologies/SemSEX1.ttl', 'ontologies/json_ontology_descriptions.json')
    graph = Graph()

    write_object_properties(graph, object_propoerties)
    write_data_properties(graph)
    write_classes(graph, classes)

    v = graph.serialize(format="turtle")
    v = edit_serialization(v)
    with open('ontologies/result.ttl', 'w') as f:
        f.write(v)


if __name__ == '__main__':
    generate_nice_ontology()
