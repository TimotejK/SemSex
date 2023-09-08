import json
import wikipedia

from description_parser import concepts_from_json
from text_translateion import translate_from_english


def name_formatter(name):
    if name == "HIV":
        name += "v"
    elif name.lower() == "condom":
        name += "n"
    return name

def add_text_sources():
    # load from json
    f = open('ontologija.json')
    con = concepts_from_json(json.load(f))
    f.close()
    print(con)
    for ind in con:
        concept = con[ind]
        concept.texts = []
        for link in concept.links:
            text = None
            if link.startswith("https://en.wikipedia.org/wiki/"):
                name = link[len("https://en.wikipedia.org/wiki/"):]
                wikipedia.set_lang("en")
                text = wikipedia.summary(name_formatter(name))
                text = translate_from_english(text)
            elif link.startswith("https://sl.wikipedia.org/wiki/"):
                name = link[len("https://sl.wikipedia.org/wiki/"):]
                wikipedia.set_lang("sl")
                text = wikipedia.summary(name_formatter(name))
            else:
                print(link)
            if text is not None:
                concept.texts.append(text)

    entities_list = []
    for index in con:
        concept = con[index]
        entities_list.append(concept.to_dict())
    s = json.dumps(entities_list)
    with open("ontologija_opisi.json", "w") as outfile:
        outfile.write(s)

from wikidata.client import Client
def automatic_building(name):
    wikipedia.set_lang("sl")
    page = wikipedia.page(name_formatter(name))

    client = Client()
    entity = client.get('Q20145', load=True)
    entity.description

def parse_wikipedia(link):
    print(wikipedia.summary(link))
    pass

if __name__ == '__main__':
    # parse_wikipedia("Sexual and reproductive health")
    add_text_sources()