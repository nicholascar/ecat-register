import os.path
from flask import Blueprint, Response, request, render_template, render_template_string
import settings
import functions
routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
    return render_template(
        'index.html',
        web_subfolder=settings.WEB_SUBFOLDER
    )


@routes.route('/dataset')
def dataset():
    return render_template('datasets.html')


@routes.route('/dataset/')
def datasets():
    # produce error note if dataset index missing
    if not os.path.isfile(settings.DATASETS_URIS_FILE):
        missing_txt = render_template_string(
            open('templates/missing.html', 'r').read(),
            title='Datasets',
            missing_file='datasets index',
            web_subfolder=settings.WEB_SUBFOLDER
        )
        return Response(
            missing_txt,
            status=500
        )

    # get the dataset URIs
    dataset_uris = open(settings.DATASETS_URIS_FILE).read().splitlines()

    # user specifies format via QSA
    if request.args.get('_format'):
        if request.args.get('_format') == 'text/uri-list':
            uri_list = render_template_string(
                open('templates/dataset-register.uri-list', 'r').read(),
                dataset_uris=dataset_uris
            )
            return Response(
                uri_list,
                status=200,
                mimetype='text/uri-list'
            )
        elif request.args.get('_format') == 'text/turtle':
            dcat_dataset = 'http://www.w3.org/ns/dcat#Dataset'
            g = functions.uri_list_to_graph(dataset_uris, dcat_dataset)
            return Response(g.serialize(format='turtle'), status=200, mimetype='text/turtle')

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
            return render_template(
                'dataset-register.html',
                dataset_uris=dataset_uris,
                mime='text/html'
            )
        elif best_mime == 'text/uri-list':
            uri_list = render_template_string(
                open('templates/dataset-register.uri-list', 'r').read(),
                dataset_uris=dataset_uris
            )
            return Response(
                uri_list,
                status=200,
                mimetype='text/uri-list'
            )
        else:  # text
            txt = render_template_string(
                open('templates/dataset-register.txt', 'r').read(),
                dataset_uris=dataset_uris
            )
            return Response(
                txt,
                status=200,
                mimetype='text/plain',
                headers={'Content-Disposition': 'attachment; filename="datasets.txt"'}
            )
    # RDF
    elif best_mime in rdf_mimes:
        # make the RDF class for the items
        dcat_dataset = 'http://www.w3.org/ns/dcat#Dataset'

        g = functions.uri_list_to_graph(dataset_uris, dcat_dataset)
        # return RDF
        if best_mime == 'application/rdf+json' or best_mime == 'application/json-ld' or best_mime == 'application/json':
            return Response(g.serialize(format='json-ld'), status=200, mimetype=best_mime)
        elif best_mime == 'text/nt':
            return Response(g.serialize(format='nt'), status=200, mimetype=best_mime)
        elif best_mime == 'text/n3':
            return Response(g.serialize(format='n3'), status=200, mimetype=best_mime)
        elif best_mime == 'applications/rdf+xml':
            return Response(g.serialize(format='xml'), status=200, mimetype=best_mime)
        else:  # if best_mime == 'text/turtle':
            return Response(g.serialize(format='turtle'), status=200, mimetype='text/turtle')
    # XML
    else:  # if best_mime in rdf_mimes:
        return render_template(
            'dataset-register.xml',
            dataset_uris=dataset_uris,
            mimetype='application/xml'
        )


@routes.route('/service')
def service():
    return render_template('services.html')


@routes.route('/service/')
def services():
    # produce error note if dataset index missing
    if not os.path.isfile(settings.SERVICES_URIS_FILE):
        missing_txt = render_template_string(
            open('templates/missing.html', 'r').read(),
            title='Services',
            missing_file='services index',
            web_subfolder=settings.WEB_SUBFOLDER
        )
        return Response(
            missing_txt,
            status=500
        )

    # get the dataset URIs
    services_uris = open(settings.SERVICES_URIS_FILE).read().splitlines()

    # user specifies format via QSA
    if request.args.get('_format'):
        if request.args.get('_format') == 'text/uri-list':
            uri_list = render_template_string(
                open('templates/service-register.uri-list', 'r').read(),
                services_uris=services_uris
            )
            return Response(
                uri_list,
                status=200,
                mimetype='text/uri-list'
            )
        elif request.args.get('_format') == 'text/turtle':
            dcat_dataset = 'http://www.w3.org/ns/dcat#Dataset'
            g = functions.uri_list_to_graph(services_uris, dcat_dataset)
            return Response(g.serialize(format='turtle'), status=200, mimetype='text/turtle')

    # list supported mime types
    human_mimes = [
        'text/html',
        'text/uri-list',
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
            return render_template(
                'service-register.html',
                services_uris=services_uris,
                mimetype='text/html'
            )
        elif best_mime == 'text/uri-list':
            uri_list = render_template_string(
                open('templates/service-register.uri-list', 'r').read(),
                services_uris=services_uris
            )
            return Response(
                uri_list,
                status=200,
                mimetype='text/uri-list'
            )
        else:  # text
            txt = render_template_string(
                open('templates/service-register.txt', 'r').read(),
                services_uris=services_uris
            )
            return Response(
                txt,
                status=200,
                mimetype='text/plain',
                headers={'Content-Disposition': 'attachment; filename="services.txt"'}
            )
    # RDF
    elif best_mime in rdf_mimes:
        # make the RDF class for the items
        dpn_service = 'http://purl.org/dpn#Service'

        g = functions.uri_list_to_graph(services_uris, dpn_service)
        # return RDF
        if best_mime == 'application/rdf+json' or best_mime == 'application/json-ld' or best_mime == 'application/json':
            return Response(g.serialize(format='json-ld'), status=200, mimetype=best_mime)
        elif best_mime == 'text/nt':
            return Response(g.serialize(format='nt'), status=200, mimetype=best_mime)
        elif best_mime == 'text/n3':
            return Response(g.serialize(format='n3'), status=200, mimetype=best_mime)
        elif best_mime == 'applications/rdf+xml':
            return Response(g.serialize(format='xml'), status=200, mimetype=best_mime)
        else:  # if best_mime == 'text/turtle':
            return Response(g.serialize(format='turtle'), status=200, mimetype='text/turtle')
    # XML
    else:  # if best_mime in rdf_mimes:
        return render_template(
            'service-register.xml',
            services_uris=services_uris,
            mimetype='application/xml'
        )
