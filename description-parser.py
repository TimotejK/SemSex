import re
import json
from rdflib import Graph, URIRef, BNode, Literal, Namespace, RDF, RDFS


class Concept:
    def __init__(self, line=None):
        if line is not None:
            concept_test = re.compile(r"^((?:\d+\.)+) (.*)$")
            result = concept_test.match(line)
            index = result.group(1)
            self.index = tuple([int(s) for s in index.split(".") if s.isnumeric()])
            self.name = result.group(2)
        self.children = []
        self.links = []
        self.relations = {}
        self.parent = None

    def add_parent(self, concepts):
        if self.index[:-1] in concepts:
            self.parent = concepts[self.index[:-1]]
            if self not in concepts[self.index[:-1]].children:
                concepts[self.index[:-1]].children.append(self)

    def __str__(self):
        return str(self.index) + " " + self.name

    def to_dict(self):
        dict = vars(self).copy()
        dict['children'] = []
        for child in self.children:
            dict['children'].append(child.index)
        if self.parent is not None:
            dict['parent'] = self.parent.index
        return dict

    def from_dict(self, dictionary):
        self.__dict__.update(dictionary)
        self.index = tuple(self.index)
        if self.parent is not None:
            self.parent = tuple(self.parent)

    def replace_references(self, concepts):
        if self.parent is not None:
            self.parent = concepts[tuple(self.parent)]

        for i in range(len(self.children)):
            self.children[i] = concepts[tuple(self.children[i])]

def concepts_from_json(lists):
    concepts={}
    for l in lists:
        concept = Concept()
        concept.from_dict(l)
        concepts[concept.index] = concept
    for ind in concepts:
        concepts[ind].replace_references(concepts)
    return concepts

def parse_descriptions(text):
    concepts = {}
    lines = text.split("\n")
    current_concept = None
    current_relation = None
    for joint_line in lines:
        for line in joint_line.split(";"):
            line = line.strip()
            concept_test = re.compile(r"^((?:\d+\.)+) (.*)$")
            if concept_test.match(line):
                concept = Concept(line)
                current_concept = concept
                concepts[concept.index] = concept
                current_relation = None
            elif re.match("Q\d+", line):
                current_concept.wikidata = line
                current_relation = None
            elif re.match("https://.+", line):
                current_concept.links.append(line)
                current_relation = None
            elif re.match("(.+): ?((?:\d+\.)+)", line):
                result = re.match("(.+): ?((?:\d+\.)+)", line)
                relation = result[1]
                target = tuple([int(s) for s in result[2].split(".") if s.isnumeric()])
                current_concept.relations[relation] = target
                current_relation = relation
            elif current_relation is not None and re.match("((?:\d+\.)+)", line):
                target = tuple([int(s) for s in line.split(".") if s.isnumeric()])
                current_concept.relations[current_relation] = target
            elif len(line) == 0:
                pass
            else:
                print(line)

    for index in concepts:
        concepts[index].add_parent(concepts)

    # save to json
    entities_list = []
    for index in concepts:
        concept = concepts[index]
        entities_list.append(concept.to_dict())
    s = json.dumps(entities_list)
    with open("ontologija.json", "w") as outfile:
        outfile.write(s)
    # load from json
    con = concepts_from_json(json.loads(s))

    build_knowledge_graph(concepts)


def build_knowledge_graph(concepts):
    def untuple(t):
        return ".".join([str(x) for x in t])

    g = Graph()
    concepts_ns = Namespace("http://example.org/concepts/")
    relations_ns = Namespace("http://example.org/relations/")
    concept_object = concepts_ns['concept']
    g.add((concept_object, RDFS.subClassOf, RDF.object))
    for index in concepts:
        concept = concepts[index]
        concept_id = concepts_ns[untuple(index)]
        if (concept.parent is not None):
            g.add((concept_id, RDFS.subClassOf, concepts_ns[untuple(concept.parent.index)]))
        else:
            g.add((concept_id, RDFS.subClassOf, concept_object))
        g.add((concept_id, relations_ns.name, Literal(concept.name)))
        for link in concept.links:
            g.add((concept_id, relations_ns.source_link, Literal(link)))
        for child in concept.children:
            g.add((concept_id, relations_ns.child, concepts_ns[untuple(child.index)]))
        for relation in concept.relations:
            g.add((concept_id, relations_ns[relation], concepts_ns[untuple(concept.relations[relation])]))
    v = g.serialize(format="turtle")
    with open('test_ontology.ttl', 'w') as f:
        f.write(v)


if __name__ == '__main__':
    text_file = open("test-descriptions.txt", "r")
    text = text_file.read()
    text_file.close()

    parse_descriptions(text)
