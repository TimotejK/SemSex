#!/bin/bash

/usr/lib/jvm/java-17-openjdk-amd64/bin/java -jar java-17-widoco-1.4.17-jar-with-dependencies.jar \
    -ontFile ../ontologies/result.ttl \
    -outFolder ../docs/SemSEX \
    -getOntologyMetadata \
    -oops \
    -rewriteAll \
    -lang en-sl \
    -htaccess \
    -webVowl \
    -licensius \
    -uniteSections \
    -displayDirectImportsOnly #\
    #-ignoreIndividuals 

node clean.js
