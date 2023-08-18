import re

class Concept:
    def __init__(self, line):
        concept_test = re.compile(r"^((?:\d+\.)+) (.*)$")
        result = concept_test.match(line)
        index = result.group(1)
        self.index = tuple([int(s) for s in index.split(".") if s.isnumeric()])
        self.name = result.group(2)
        self.children = []
        self.links = []
        self.relations = {}

    def add_parent(self, concepts):
        if self.index[:-1] in concepts:
            self.parent = concepts[self.index[:-1]]
            if self not in concepts[self.index[:-1]].children:
                concepts[self.index[:-1]].children.append(self)

    def __str__(self):
        return str(self.index) + " " + self.name

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
    pass

if __name__ == '__main__':
    text_file = open("test-descriptions.txt", "r")
    text = text_file.read()
    text_file.close()

    parse_descriptions(text)