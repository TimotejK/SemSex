# importing required modules
# import PyPDF2
import PyMuPDF

def read_annotation(page):
    annotations = page.annotations()
    (pwidth, pheight) = (page.pageSize().width(), page.pageSize().height())
    if len(annotations) > 0:
        for annotation in annotations:
            if annotation.get_object()['/Subtype'] == '/Highlight':
                    quads = annotation.highlightQuads()
                    txt = ""
                    for quad in quads:
                        rect = (quad.points[0].x() * pwidth,
                                quad.points[0].y() * pheight,
                                quad.points[2].x() * pwidth,
                                quad.points[2].y() * pheight)
                        bdy = PyQt4.QtCore.QRectF()
                        bdy.setCoords(*rect)
                        txt = txt + unicode(page.text(bdy)) + ' '

                    # print("========= ANNOTATION =========")
                    print(unicode(txt))
    pass

# creating a pdf file object
pdfFileObj = open('dokumenti/nacrti/1 UN_spoznavanje_okolja_pop-2.pdf', 'rb')

# creating a pdf reader object
pdfReader = PyPDF2.PdfReader(pdfFileObj)

# printing number of pages in pdf file
print(len(pdfReader.pages))

# creating a page object
pageObj = pdfReader.pages[0]

# extracting text from page
print(pageObj.extract_text())

# closing the pdf file object
pdfFileObj.close()