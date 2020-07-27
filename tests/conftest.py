# -*- coding: utf-8 -*-

import os
import sys

import pytest
from . import TEST_DIR

from rdflib import Graph
from skosprovider_rdf.providers import RDFProvider

PY3 = sys.version_info[0] == 3

if PY3:  # pragma: no cover
    text_type = str
else:  # pragma: no cover
    text_type = unicode

@pytest.fixture(scope='module')
def products_provider():
    products_graph = Graph()
    abspath = os.path.abspath(TEST_DIR + "/data/simple_turtle_products")
    products_graph.parse(abspath, format="turtle")

    # Set up rdf_provider
    products_provider = RDFProvider(
        {'id': 'PRODUCTS'}, products_graph
    )
    return products_provider

@pytest.fixture(scope='module')
def trees_provider():
    trees_graph = Graph()
    abspath = os.path.abspath(TEST_DIR + "/data/trees.xml")
    trees_graph.parse(abspath, format="application/rdf+xml")
    trees_provider = RDFProvider(
        {'id': 'TREES'}, trees_graph
    )
    return trees_provider

@pytest.fixture(scope='module')
def materials_provider():
    import json

    materials_data = json.load(
        open(os.path.join(TEST_DIR, 'data', 'materiaal.txt')),
    )['materiaal']
    from skosprovider.providers import DictionaryProvider
    from skosprovider.uri import UriPatternGenerator
    from skosprovider.skos import ConceptScheme, Label, Note

    materials = DictionaryProvider(
        {'id': 'Materials'},
        materials_data,
        uri_generator=UriPatternGenerator('https://id.erfgoed.net/thesauri/materialen/%s'),
        conceptscheme=ConceptScheme(
            uri='https://id.erfgoed.net/thesauri/materialen',
            labels=[Label(type='prefLabel', language='nl', label='Materialen')],
            notes=[Note(type='scopeNote', language='nl', note='Materialen zijn grondstoffen of halfafgewerkte producten die vaak een rol spelen bij onroerend erfgoed.')]
        )
    )
    return materials

@pytest.fixture(scope='module')
def materials_collections_provider():
    products_graph = Graph()
    abspath = os.path.abspath(TEST_DIR + "/data/mat_collections.ttl")
    map_graph.parse(abspath, format="turtle")

    # Set up rdf_provider
    mat_provider = RDFProvider(
        {'id': 'MATCOL'}, mat_graph
    )
    return mat_provider
