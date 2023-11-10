# SemSEX

This repository contains an ontology related to sexual education, represented in Turtle file format, along with machine learning models for detecting concepts defined in the ontology.

## Repository Structure

```
📦 SemSEX Repository
├── 📂 Ontology
│   ├── 📄 SemSEX.ttl
│   └── 📂 docs
├── 📂 Concept-Detection
│   ├── 📂 Curriculum documents
│   ├── 📂 dataset_preparation
│   ├── 📂 Classifiers
│   ├── 📄 common.py
│   ├── 📄 README.md
│   └── 📄 requirements.txt
└── 📄 README.md
```

### 1. Ontology

The ontology is stored in the "Ontology" folder, which contains the following:

- **SemSEX.ttl**: This Turtle file represents the sexual education ontology, capturing various concepts related to the subject.

- **docs**: The docs directory contains the documentation of the ontology in the html format. The main file is index.html.

### 2. Concept Detection

The "Concept-Detection" folder contains machine learning models for detecting concepts defined in the ontology. Each model is stored as an individual file:

- **Curriculum documents**: Contains raw documents with description of curriculums. The documents are annotated with concepts from the ontology.
- **dataset_preparation**: Contains python code for converting the raw pdf documents into pandas dataframes that can be used for training the classifiers. 
- **Classifiers**: Contains classifiers written in python for automatically detecting concepts from sexual education.
- **common.py**: A helper file containing functions useful across other documents
- **README.md**: Instructions for running the classifiers and the description of their results.
- **requirements.txt**: A list of required python packages.

Feel free to explore and use these models for concept detection based on the sexual education ontology.

### 3. README.md

This file serves as an introduction and guide to the repository, outlining its structure, content, and purpose.

## License

This repository is licensed under the [LICENSE](LICENSE) - please review it for details on how you can use and share the content.

Feel free to contribute, report issues, or suggest improvements by creating a pull request.
