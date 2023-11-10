import fitz
import pandas as pd

def intersect(rect1, rect2):
    pass
def get_highlights(page):
    # list to store the co-ordinates of all highlights
    highlights = []

    # get all annotated parts of the page
    annot = page.first_annot
    while annot:
        if annot.type[0] == 8:
            all_coordinates = annot.vertices
            if len(all_coordinates) == 4:
                highlight_coord = fitz.Quad(all_coordinates).rect
                highlights.append([highlight_coord])
            else:
                all_coordinates = [all_coordinates[x:x + 4] for x in range(0, len(all_coordinates), 4)]
                current_highlight = []
                for i in range(0, len(all_coordinates)):
                    coord = fitz.Quad(all_coordinates[i]).rect
                    current_highlight.append(coord)
                highlights.append(current_highlight)
        annot = annot.next

    # get text
    all_words = page.get_text_words()
    highlight_text = []
    for current_highlight in highlights:
        current_highlight_text = []
        for h in current_highlight:
            sentence = [w[4] for w in all_words if fitz.Rect(w[0:4]).intersect(h).is_valid]
            current_highlight_text.append(" ".join(sentence))
        highlight_text.append(" ".join(current_highlight_text))
    return highlight_text

def get_non_annotated_text(page):
    text = page.get_text()
    text = text.replace("", "|-")
    text = text.replace("\n\n", "|")
    text = text.replace("\n \n", "|")

    text = text.replace("\n", "")
    sections = text.split("|")
    sections = map(lambda x: x.strip(), sections)
    sections = filter(lambda x: x.startswith("-"), sections)
    sections = map(lambda x: x[1:].strip(), sections)
    sections = list(sections)
    return sections

def filter_negative_examples(negative, positive):
    new_neg = []
    for neg in negative:
        include = True
        for p in positive:
            if p in neg:
                include = False
        if include:
            new_neg.append(neg)
    return new_neg

def generate_dataset(docs):
    dataset = []
    for doc in docs:
        for page in doc:
            neg = get_non_annotated_text(page)
            pos = get_highlights(page)
            neg = filter_negative_examples(neg, pos)
            for p in pos:
                dataset.append([p, True])
            for n in neg:
                dataset.append([n, False])
    return pd.DataFrame(dataset, columns=['text', 'label'])

def get_dataset_for_binary_classification():
    docs = []
    file_names = [
        'Curriculum documents/Curriculum pdf/10 UN_glasbena_vzgoja.pdf',
        'Curriculum documents/Curriculum pdf/2 UN_zgodovina.pdf',
        'Curriculum documents/Curriculum pdf/11 UN_Biologija.pdf',
        'Curriculum documents/Curriculum pdf/3 UN_fizika.pdf',
        'Curriculum documents/Curriculum pdf/12 UN_tehnika_tehnologija.pdf',
        'Curriculum documents/Curriculum pdf/4 UN_kemija.pdf',
        'Curriculum documents/Curriculum pdf/13 UN_gospodinjstvo.pdf',
        'Curriculum documents/Curriculum pdf/5 UN_geografija.pdf',
        'Curriculum documents/Curriculum pdf/14 UN_DDE_OS.pdf',
        'Curriculum documents/Curriculum pdf/6 UN_matematika.pdf',
        'Curriculum documents/Curriculum pdf/15 UN_druzba_OS.pdf',
        'Curriculum documents/Curriculum pdf/7 UN_slovenscina.pdf',
        'Curriculum documents/Curriculum pdf/16 UN_naravoslovje.pdf',
        'Curriculum documents/Curriculum pdf/8 UN_naravoslovje_in_tehnika.pdf',
        'Curriculum documents/Curriculum pdf/17 UN_sportna_vzgoja.pdf',
        'Curriculum documents/Curriculum pdf/9 UN_likovna_vzgoja.pdf',
        'Curriculum documents/Curriculum pdf/1 UN_spoznavanje_okolja_pop-2.pdf'
    ]
    for name in file_names:
        docs.append(fitz.open(name))
    dataset = generate_dataset(docs)
    return dataset

if __name__ == '__main__':
    dataset = get_dataset_for_binary_classification()
    dataset.to_csv("ucni_nacrti_oznaceno.csv")
    pass
