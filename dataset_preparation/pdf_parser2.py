import fitz

doc = fitz.open('dokumenti/nacrti/1 UN_spoznavanje_okolja_pop-2.pdf')

page = doc[14]

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
                highlights.append(highlight_coord)
            else:
                all_coordinates = [all_coordinates[x:x + 4] for x in range(0, len(all_coordinates), 4)]
                for i in range(0, len(all_coordinates)):
                    coord = fitz.Quad(all_coordinates[i]).rect
                    highlights.append(coord)
        annot = annot.next

    # get text
    all_words = page.get_text_words()
    highlight_text = []
    for h in highlights:
        sentence = [w[4] for w in all_words if fitz.Rect(w[0:4]).intersect(h).is_valid]
        highlight_text.append(" ".join(sentence))
    pass

page.get_text()
get_highlights(page)
