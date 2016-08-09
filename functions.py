from rdflib import Graph, URIRef, RDF, Namespace


def get_dataset_uris():
    return [
        'http://example.com/dataset/1',
        'http://example.com/dataset/2',
        'http://example.com/dataset/3',
        'http://example.com/dataset/4',
        'http://example.com/dataset/5',
        'http://example.com/dataset/6'
    ]


def uri_list_to_graph(uri_list, item_class):
    g = Graph()
    for uri in uri_list:
        g.add((URIRef(uri), RDF.type, URIRef(item_class)))

    return g
