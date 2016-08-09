from rdflib import Graph, URIRef, RDF
from lxml import etree


def get_dataset_uris():
    # http://ecat.ga.gov.au/geonetwork/srv/eng/csw-services?service=CSW&version=2.0.2&request=GetRecords&elementSetName=full&outputSchema=own&outputFormat=application/xml&resultType=results&constraintLanguage=CQL_TEXT&constraint_language_version=1.1.0&constraint=AnyText+like+%27marine%27
    return [
        'http://example.com/dataset/1',
        'http://example.com/dataset/2',
        'http://example.com/dataset/3',
        'http://example.com/dataset/4',
        'http://example.com/dataset/5',
        'http://example.com/dataset/6'
    ]


def get_dataset_uris_static(uri_base):
    # http://ecat.ga.gov.au/geonetwork/srv/eng/csw-services?service=CSW&version=2.0.2&request=GetRecords&elementSetName=full&outputSchema=own&outputFormat=application/xml&resultType=results&constraintLanguage=CQL_TEXT&constraint_language_version=1.1.0&constraint=AnyText+like+%27%27
    xml = etree.parse('test/static-datasets.xml')
    namespaces = {
        'mdb': 'http://standards.iso.org/iso/19115/-3/mdb/1.0',
        'gco': 'http://standards.iso.org/iso/19115/-3/gco/1.0',
        'mcc': 'http://standards.iso.org/iso/19115/-3/mcc/1.0',
        'cit': 'http://standards.iso.org/iso/19115/-3/cit/1.0',
    }
    # UUIDs
    #ds = xml.xpath('//mdb:MD_Metadata/mdb:metadataIdentifier/mcc:MD_Identifier/mcc:code/gco:CharacterString/text()',
    #               namespaces=namespaces)

    # eCat IDs
    xpath = '//mdb:alternativeMetadataReference/cit:CI_Citation/cit:identifier/mcc:MD_Identifier/mcc:code/gco:CharacterString/text()'
    ds = xml.xpath(xpath,
                   namespaces=namespaces)

    return (uri_base + s for s in ds)


def uri_list_to_graph(uri_list, item_class):
    g = Graph()
    for uri in uri_list:
        g.add((URIRef(uri), RDF.type, URIRef(item_class)))

    return g
