The SemSex corpus is designed to facilitate the automated recognition of sexual education concepts within curriculum description documents. The corpus contains two components: PDF documents detailing Slovene school subjects and a structured JSON file named curriculums.json.

The first part of the corpus contains the PDF documents describing various school subjects. Annotations within these documents show specific phrases that pertain to one or more sexual education concepts. These annotations serve as markers, aiding in the extraction of relevant information.

The second part of the corpus, curriculums.json, is a structured file presenting the extracted texts from the PDF documents in the JSON format. This file encapsulates the textual content extracted from the PDF documents as well as annotations corresponding to the sections that describe sexual education concepts. Each annotation in curriculums.json comprises a list of concepts that the particular description is referencing.

The JSON structure of the corpus unfolds as follows:
- At the first level, individual objects represent each PDF document.
- Under 'pages,' a list is provided for each document, encapsulating various pages.
  - 'content': This section contains a string representing all the text extracted from the corresponding PDF page.
  - 'page_number': Each page is tagged with the original page number from the PDF document.
  - 'annotations': A list associated with each page, outlining specific annotations.
    - 'start_index': Denotes the starting index of the annotated phrase within the page content.
    - 'end_index': Specifies the concluding index of the annotated phrase within the page content.
    - 'labels': This list encompasses the concepts to which the annotated phrase refers.