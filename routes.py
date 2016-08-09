from flask import Blueprint, Response, request, redirect, render_template, g, jsonify
import settings
import functions
routes = Blueprint('routes', __name__)


@routes.route('/')
def home():
    return 'hello home'


@routes.route('/dataset')
def dataset():
    return 'metadata about the dataset class'


@routes.route('/dataset/')
def datasets():
    # get the metadata values of the sample
    metadata_uris = functions.get_dataset_uris_static('http://pid-test.geoscience.gov.au/dataset/')

    # list supported mime types
    human_mimes = [
        'text/html',
        'text/plain'
    ]
    # RDF mime types
    rdf_mimes = [
        'text/turtle',
        'text/n3',
        'text/ntriples',
        'application/rdf+xml',
        'application/rdf+json',
        'application/json-ld',
        'application/json',
        'application/rdf+xml'
    ]
    # XML
    xml_mimes = [
        'application/xml',
        'text/xml'
    ]
    # find the best matched mime type
    all_mimes = human_mimes + rdf_mimes + xml_mimes
    best_mime = request.accept_mimetypes.best_match(all_mimes)
    # human-readable
    if best_mime in human_mimes:
        if best_mime == 'text/html':
            return render_template('dataset-register.html',
                                   metadata_uris=metadata_uris,
                                   mime='text/html')
        elif best_mime == 'text/uri-list':
            return render_template('dataset-register.txt',
                                   metadata_uris=metadata_uris,
                                   mime='text/uri-list')
        else:  # text
            return render_template('dataset-register.txt',
                                   metadata_uris=metadata_uris,
                                   mime='text/plain')
    # RDF
    elif best_mime in rdf_mimes:
        # make the RDF class for the items
        dcat_dataset = 'http://www.w3.org/ns/dcat#Dataset'

        g = functions.uri_list_to_graph(metadata_uris, dcat_dataset)
        # return RDF
        if best_mime == 'application/rdf+json' or best_mime == 'application/json-ld' or best_mime == 'application/json':
            return Response(g.serialize(format='json-ld'), mimetype=best_mime)
        elif best_mime == 'text/nt':
            return Response(g.serialize(format='nt'), mimetype=best_mime)
        elif best_mime == 'text/n3':
            return Response(g.serialize(format='n3'), mimetype=best_mime)
        elif best_mime == 'applications/rdf+xml':
            return Response(g.serialize(format='xml'), mimetype=best_mime)
        else:  # if best_mime == 'text/turtle':
            return Response(g.serialize(format='turtle'), mimetype=best_mime)
    # XML
    else:  # if best_mime in rdf_mimes:
        return render_template('dataset-register.xml',
                               metadata_uris=metadata_uris,
                               mime='application/xml')
