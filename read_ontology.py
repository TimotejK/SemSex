from rdflib import Graph

if __name__ == '__main__':
    graph = Graph()
    graph.parse('urn_webprotege_ontology_b023949d-0cc7-486d-976b-21324510ec03.ttl', format='ttl')
    print(graph)