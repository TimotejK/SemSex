import json
import wikipedia

from description_parser import concepts_from_json
from text_translation import translate_from_english


def name_formatter(name, lang):
    print(name, lang)
    if name == "HIV":
        name += "v"
    elif name.lower() == "condom":
        name += "n"
    elif name == "Tubal_ligation":
        name += "_"
    elif name == "Tampon":
        name = "Taampon"
    elif name == "Parafilija_(psihiatrija)":
        name = "Parafilija (psihiatrija)"
    elif name == "Sex" and lang == "en":
        name = "Sexz"
    elif name == "Intersex" and lang == "en":
        name = "Intersexx"
    elif name == "Gay" and lang == "en":
        name = "gGay"
    elif name == "Drag_(entertainment)" and lang == "en":
        name = "Drag (entertainment)"
    elif name == "Masturbation" and lang == "en":
        name = "Masturbationn"
    elif name == "Virtual_sex" and lang == "en":
        name = "Virtual_sexx"
    elif name == "Monogamy" and lang == "en":
        name = "Monogamyn"
    elif name == "Gang_bang" and lang == "en":
        name = "Gang_bangn"
    elif name == "Orgy" and lang == "en":
        name = "Orgyy"
    elif name == "Non-penetrative_sex" and lang == "en":
        name = "penetrative_sexx"
    elif name == "Sex_work" and lang == "en":
        name = "Sex_workk"
    elif name == "Prostitution" and lang == "en":
        name = "Prostitutionn"
    elif name == "Consent" and lang == "en":
        name = "Consentt"
    elif name == "Puberty" and lang == "en":
        name = "Pubertyy"
    elif name == "Human_reproduction" and lang == "en":
        name = "Human rreproduction"
    elif name == "Male" and lang == "en":
        name = "Malee"
    elif name == "Penis" and lang == "en":
        name = "Peniss"
    elif name == "Foreskin" and lang == "en":
        name = "Foreskinn"
    elif name == "Glans_penis" and lang == "en":
        name = "Glans_peniss"
    elif name == "Prostate" and lang == "en":
        name = "Prostatee"
    elif name == "Bartholin%27s_gland" and lang == "en":
        name = "Bartholins gland"
    elif name == "Cervix" and lang == "en":
        name = "cCervix"
    elif name == "Vagina" and lang == "en":
        name = "Vaginaa"
    elif name == "Labia" and lang == "en":
        name = "Labiaa"
    elif name == "G-spot" and lang == "en":
        name = "Gspot"
    elif name == "Orgasm" and lang == "en":
        name = "Orgaasm"
    elif name == "Ejaculation" and lang == "en":
        name = "Ejaculationn"
    elif name == "Semen" and lang == "en":
        name = "Semenn"
    elif name == "Skene%27s_gland" and lang == "en":
        name = "Skenes gland"
    elif name == "Sex_toy" and lang == "en":
        name = "Sex toyy"
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
                try:
                    text = wikipedia.page(name_formatter(name, lang="en")).content
                    text = translate_from_english(text)
                except:
                    text = "napaka EN"
            elif link.startswith("https://sl.wikipedia.org/wiki/"):
                name = link[len("https://sl.wikipedia.org/wiki/"):]
                wikipedia.set_lang("sl")
                try:
                    text = wikipedia.page(name_formatter(name, lang="sl")).content
                except:
                    text = "napaka SL"
            else:
                print(link)
            if text is not None:
                concept.texts.append(text)

    entities_list = []
    for index in con:
        concept = con[index]
        entities_list.append(concept.to_dict())
    s = json.dumps(entities_list)
    with open("ontologies/json_ontology_descriptions.json", "w") as outfile:
        outfile.write(s)

# from wikidata.client import Client
# def automatic_building(name):
#     wikipedia.set_lang("sl")
#     page = wikipedia.page(name_formatter(name))
#
#     client = Client()
#     entity = client.get('Q20145', load=True)
#     entity.description
#
# def parse_wikipedia(link):
#     print(wikipedia.summary(link))
#     pass

def write_to_text_file():
    f = open('ontologija_opisi-dolgi.json')
    con = concepts_from_json(json.load(f))
    f.close()


if __name__ == '__main__':
    # parse_wikipedia("Sexual and reproductive health")
    add_text_sources()