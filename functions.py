import requests
import json
from rdflib import Graph, URIRef, RDF
from lxml import etree


# TODO: stream XML response
# TODO: return URIs efficiently from streamed response
def get_dataset_uris(uri_base):
    # POST request the dataset list from eCat's CSW
    d = '''
    <csw:GetRecords
        xmlns:csw="http://www.opengis.net/cat/csw/2.0.2"
        xmlns:ogc="http://www.opengis.net/ogc"
        service="CSW"
        version="2.0.2"
        resultType="results"
        startPosition="1"
        maxRecords="100000"
        outputFormat="application/xml"
        outputSchema="csw:IsoRecord"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-discovery.xsd"
        xmlns:gmd="http://www.isotc211.org/2005/gmd"
        xmlns:apiso="http://www.opengis.net/cat/csw/apiso/1.0">
      <csw:Query typeNames="csw:Record">
        <csw:ElementSetName>summary</csw:ElementSetName>
        <csw:Constraint version="1.1.0">
          <ogc:Filter>
               <PropertyIsLike wildCard="*" singleChar="_" escapeChar="\">
                   <PropertyName>AnyText</PropertyName>
                   <Literal>*</Literal>
               </PropertyIsLike>
          </ogc:Filter>
        </csw:Constraint>
      </csw:Query>
    </csw:GetRecords>
    '''
    r = requests.post('http://ecat.ga.gov.au/geonetwork/srv/eng/csw',
                      data=d,
                      headers={'Content-Type': 'application/xml'})

    xml = etree.fromstring(r.content)
    namespaces = {
        'gmd': 'http://www.isotc211.org/2005/gmd',
        'mdb': 'http://standards.iso.org/iso/19115/-3/mdb/1.0',
        'gco': 'http://www.isotc211.org/2005/gco',  # ''http://standards.iso.org/iso/19115/-3/gco/1.0',
        'mcc': 'http://standards.iso.org/iso/19115/-3/mcc/1.0',
        'cit': 'http://standards.iso.org/iso/19115/-3/cit/1.0'
    }

    xpath = '//gmd:identifier/gmd:RS_Identifier/gmd:code/gco:CharacterString/text()'
    ids = xml.xpath(xpath,
                   namespaces=namespaces)

    results = []
    for id in ids:
        if is_int(id):
            results.append(uri_base + str(id))

    return results


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


# TODO: write stream to file
def store_dataset_uris(uri_list, file):
    json.dump(uri_list, open(file, 'w'), indent=4)


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


if __name__ == '__main__':
    store_dataset_uris(
        get_dataset_uris('http://pid.geoscience.gov.au/dataset/'),
        'uris.json'
    )