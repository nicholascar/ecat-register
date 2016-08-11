import requests
from rdflib import Graph, URIRef, RDF
import subprocess
import shlex


def store_csw_request(csw_endpoint, request_xml, xml_file_to_save):
    r = requests.post(csw_endpoint,
                      data=request_xml,
                      headers={'Content-Type': 'application/xml'},
                      stream=True)

    with open(xml_file_to_save, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return True


def uri_list_to_graph(uri_list, item_class):
    g = Graph()
    for uri in uri_list:
        g.add((URIRef(uri), RDF.type, URIRef(item_class)))

    return g


if __name__ == '__main__':
    import sys

    datasets_xml = 'datasets.xml'
    dataset_uri_base = 'http://pid.geoscience.gov.au/dataset/'
    datasets_ids = 'datasets.txt1'
    datasets_uris = 'datasets.txt'
    services_xml = 'services.xml'
    service_uri_base = 'http://pid.geoscience.gov.au/service/'
    services_uris = 'services.txt'

    request_xml = '''
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

    if sys.argv[1] == 'services':
        if sys.argv[2] == 'download':
            csw_endpoint = 'http://ecat.ga.gov.au/geonetwork/srv/eng/csw-services'
            store_csw_request(csw_endpoint, request_xml, services_xml)
        elif sys.argv[2] == 'extract':
            subprocess.call(shlex.split('sh script_extract_ids.sh %s %s' % (services_xml, services_uris)))
        elif sys.argv[2] == 'uris':
            subprocess.call(shlex.split('sh script_make_uris.sh %s %s' % (services_uris, service_uri_base)))
    elif sys.argv[1] == 'datasets':
        if sys.argv[1] == 'download':
            csw_endpoint = 'http://ecat.ga.gov.au/geonetwork/srv/eng/csw'
            store_csw_request(csw_endpoint, request_xml, datasets_xml)
        elif sys.argv[2] == 'extract':
            uri_base = 'http://pid.geoscience.gov.au/dataset/'
            subprocess.call(shlex.split('sh script_extract_ids.sh %s %s' % (datasets_xml, datasets_uris)))
        elif sys.argv[2] == 'remove_services':
            subprocess.call(shlex.split('sh script_remove_lines.sh %s %s %s' % (services_uris, datasets_ids, datasets_uris)))
        elif sys.argv[2] == 'uris':
            subprocess.call(shlex.split('sh script_make_uris.sh %s %s' % (datasets_uris, service_uri_base)))
