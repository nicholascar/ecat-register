import os.path
import json
from flask import Blueprint, Response, request, redirect, render_template, g, jsonify, render_template_string
import settings
import functions
routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
    return render_template('index.html')


@routes.route('/dataset')
def dataset():
    return render_template('datasets.html')


@routes.route('/dataset/')
def datasets():
    # produce error note if dataset index missing
    if not os.path.isfile(settings.DATASETS_JSON_FILE):
        missing_txt = render_template_string(
            open('templates/missing.html', 'r').read(),
            title='Datasets',
            missing_file='datasets index'
        )
        return Response(
            missing_txt,
            status=500
        )

    # get the metadata values of the sample
    metadata_uris = json.load(open(settings.DATASETS_JSON_FILE))
    metadata_uris.sort()

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
            uri_list = render_template_string(
                open('templates/dataset-register.uri_list', 'r').read(),
                metadata_uris=metadata_uris
            )
            return Response(uri_list,
                            mimetype='text/uri-list')
        else:  # text
            txt = render_template_string(open('templates/dataset-register.txt', 'r').read(), metadata_uris=metadata_uris)
            return Response(txt,
                            mimetype='text/plain',
                            headers={'Content-Disposition': 'attachment; filename="datasets.txt"'})
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
