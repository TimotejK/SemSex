import re

import text_translation


def read_ontology():
    file = open("ontologies/SemSEX3.ttl", "r")
    ttl_file = file.read()
    file.close()
    return ttl_file

def replace_descriptions():
    ttl_file = read_ontology()
    def edit_definition(definition, lang):
        definition = definition.replace("\n", " ")

        if definition == "TODO":
            return "TODO"

        if lang == 'en':
            with open('definicije.txt', 'a') as file:
                file.write(definition + "\n\n")

        return "ZAMENJAJ " + lang

    def replace_internal_quotes(text):
        inside = False
        for i in range(1, len(text) - 1):
            if text[i] == '"' and text[i-1] == '"' and text[i+1] == '"':
                inside = not inside
            elif inside and text[i] == '"' and text[i-1] != '"' and text[i+1] != '"':
                text = text[:i] + "'" + text[i+1:]
            elif text[i] == '"' and text[i-1] == '\\':
                text = text[:i] + "'" + text[i+1:]
        return text


    ttl_file = replace_internal_quotes(ttl_file)
    ttl_file = ttl_file.replace("\\'", "'")

    replaced = re.sub('skos:definition ""?"?([^"]*)""?"?@en,\s+""?"?([^"]*)""?"?@sl',
           lambda match: 'skos:definition "%s"@en,\n        "%s"@sl' % (edit_definition(match.group(1), 'en'), edit_definition(match.group(2), 'sl')), ttl_file)
    # replaced = re.sub('skos:definition """((?:.|\s)*)"""@en,\s+"""((?:.|\s)*)"""@sl',
    #        lambda match: 'skos:definition "%s"@en,\n        "%s"@sl' % (edit_definition(match.group(1)), edit_definition(match.group(2))), replaced)

    print(replaced)

with open("definicije-slo.txt", "r") as text_file:
    translated_lines = text_file.readlines()
line_num = 0

def translate_definitions():
    ttl_file = read_ontology()
    def translate_definition(eng_text):
        global translated_lines, line_num
        slo_text = eng_text
        if eng_text != "TODO":
            slo_text = translated_lines[line_num].replace("\n", "")
            line_num += 1

        # return text_translation.translate_from_english(eng_text)
        return slo_text

    replaced = re.sub('skos:definition ""?"?([^"]*)""?"?@en,\s+""?"?([^"]*)""?"?@sl', lambda match: 'skos:definition "%s"@en,\n        "%s"@sl' % (match.group(1), translate_definition(match.group(1))), ttl_file)
    print(replaced)

def replace_internal_quotes2():
    text = read_ontology()
    inside = False
    for i in range(17, len(text)):
        if not inside and text[i-17 : i] == 'skos:definition "':
            inside = True
        elif inside and text[i] == '@':
            inside = False
        elif inside and text[i] == '"':
            text = text[:i] + "'" + text[i+1:]
    print(text)

if __name__ == '__main__':
    # replace_internal_quotes2()
    # replace_descriptions()
    translate_definitions()

