const fs = require("fs");

const replaceStringsInFile = (
  inputFilePath,
  outputFilePath,
  searchAndReplace,
  callback
) => {
  fs.readFile(inputFilePath, "utf8", (err, data) => {
    if (err) {
      callback(err);
      return;
    }
    // Replace all occurrences of each search string with the replace string
    searchAndReplace.forEach((search) => {
      data = data.replace(new RegExp(search.from, "g"), search.to);
    });
    // Write the modified data back to the file
    fs.writeFile(outputFilePath, data, "utf8", (err) => {
      if (err) {
        callback(err);
        return;
      }
      callback(null);
    });
  });
};

const inputFilePath = "../docs/pz/index-sl.html";
const outputFilePath = "../docs/pz/index-sl.html";
const searchAndReplace = [
  { from: "Cite as:", to: "Citiraj kot:" },
  { from: "This version:", to: "Ta verzija:" },
  { from: "Revision:", to: "Verzija: " },
  { from: "Authors:", to: "Avtorji:" },
  { from: "Release", to: "Izdaja" },
  { from: "Publisher:", to: "Izdajatelj:" },
  { from: "Download serialization:", to: "Prenesite serializacijo:" },
  { from: "License:", to: "Licenca:" },
  { from: "Visualization:", to: "Vizualizacija:" },
  { from: "Provenance of this page", to: "Izvor te strani" },
  { from: ">language ", to: ">jezik " },
  {
    from: "The Slovene Data map ontology",
    to: "Shema podatkovnega zemljevida",
  },
  {
    from: "University of Ljubljana, Faculty of Computer and Information Science",
    to: "Univerza v Ljubljani, Fakulteta za računalništvo in informatiko",
  },
  { from: "Abstract", to: "Povzetek" },
  { from: "Table of contents", to: "Kazalo" },
  { from: " back to ", to: " nazaj na " },
  { from: "Overview", to: "Pregled" },
  { from: "Namespace declarations", to: "Opredelitve imenskih prostorov" },
  { from: "Table 1", to: "Tabela 1" },
  { from: ": Description", to: ": Opis" },
  {
    from: "This is a place holder text for the introduction. The introduction should briefly describe the ontology, its motivation, state of the art and goals.",
    to: "Pri opredelitvi podatkovnega slovarja smo v največji možni meri uporabili obstoječe koncepte iz ontologij, ki so predstavljene v nadaljevanju.",
  },
  { from: "Introduction", to: "Uvod" },
  {
    from: "Namespaces used in the document",
    to: "Imenski prostori v dokumentu",
  },
  {
    from: "Cross-reference for Shema podatkovnega zemljevida classes, object properties and data properties",
    to: "Sklici na razrede, objektne in podatkovne lastnosti Sheme podatkovnega zemljevida",
  },
  {
    from: '<img src="https://dejanl.github.io/PZ/shema.svg">',
    to: '<img style="max-width:100%" src="https://dejanl.github.io/PZ/shema.svg">',
  },
  {
    from: "This ontology has the following classes and properties.",
    to: "Shema podatkovnega zemljevida ima naslednje razrede in lastnosti.",
  },
  {
    from: "This is a placeholder text for the description of your ontology. The description should include an explanation and a diagram explaining how the classes are related, examples of usage, etc.",
    to: "",
  },
  {
    from: "This section provides details for each class and property defined by Shema podatkovnega zemljevida.",
    to: "Ta razdelek podrobneje opisuje razrede in lastnosti Sheme podatkovnega zemljevida.",
  },
  { from: "is in domain of", to: "je v domeni" },
  { from: "is in range of", to: "je v obsegu" },
  { from: "Class ToC", to: "kazalo razredov" },
  { from: "Data Property ToC", to: "kazalo podatkovnih lastnosti" },
  { from: "Object Property ToC", to: "kazalo objektnih lastnosti" },
  { from: "ToC", to: "kazalo" },
  { from: "has sub-classes", to: "ima podrazrede" },
  { from: "has super-classes", to: "ima nadrazrede" },
  { from: "Classes", to: "Razredi" },
  { from: "Object Properties", to: "Objektni lastnosti" },
  { from: "Data Properties", to: "Podatkovne lastnosti" },
  { from: "Named Individuals", to: "Poimenovani primerki" },
  { from: "Legend", to: "Legenda" },
  { from: "Retrieved from:", to: "Pridobljeno iz:" },
  { from: "Term rationale", to: "Utemeljitev pojma" },
  { from: "has domain", to: "ima domeno" },
  { from: "has range", to: "ima obseg" },
  { from: "is also defined as", to: "je tudi opredeljen kot" },
  { from: "Acknowledgments", to: "Zahvala" },
  { from: ">References", to: ">Reference" },
  { from: "belongs to", to: "pripada" },
  { from: "has facts", to: "ima dejstva" },
  { from: "Add your references here. It is recommended to have them as a list.", to: "Reference na uporabljene vire." },
  {
    from: 'The authors would like to thank <a href="http://www.essepuntato.it/">Silvio Peroni</a> for developing <a href="http://www.essepuntato.it/lode">LODE</a>, a Live OWL Documentation Environment, which is used for representing the Cross Referencing Section of this document and <a href="https://w3id.org/people/dgarijo">Daniel Garijo</a> for developing <a href="https://github.com/dgarijo/Widoco">Widoco</a>, the program used to create the template used in this documentation.</p>',
    to: 'Avtorji bi se radi zahvalili <a href="http://www.essepuntato.it/">Silvio Peroniju</a> za razvoj <a href="http://www.essepuntato.it/lode">LODE</a>, ki je bil uporabljen pri izdelavi vizualizacije in <a href="https://w3id.org/people/dgarijo">Danielu Gariju</a> za razvoj <a href="https://github.com/dgarijo/Widoco">Widoco</a>, programa za generiranje te dokumentacije.</p>',
  },
];

replaceStringsInFile(inputFilePath, outputFilePath, searchAndReplace, (err) => {
  if (err) {
    console.error(err);
    return;
  }
  console.log("Done cleaning SLO translation!");
});
