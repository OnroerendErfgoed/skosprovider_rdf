# -*- coding: utf-8 -*-
import unittest
import os
from rdflib import Graph
from rdflib.namespace import RDF, SKOS
from skosprovider.providers import DictionaryProvider
from skosprovider_rdf.providers import RDFProvider
from skosprovider_rdf import utils
from rdflib.term import URIRef


#unittest.TestCase
class RDFProviderUtilsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        return

    def setUp(self):
        # Set up testdata
        self._create_test_data()

    def tearDown(self):
        del self.larch_dump
        del self.chestnut_dump
        del self.world_dump

    def _create_test_data(self):
        self.graph = Graph()
        filepath = os.path.dirname(os.path.realpath(__file__))
        abspath = os.path.abspath(filepath + "/data/simple_turtle_products")
        self.graph.parse(abspath, format="turtle")

        self.u_products = URIRef("http://www.products.com/")
        self.u_jewellery = URIRef("http://www.products.com/Jewellery")
        self.u_perfume = URIRef("http://www.products.com/Perfume")
        self.u_product = URIRef("http://www.products.com/Product")
        self.u_stuff = URIRef("http://www.products.com/Stuff")

        self.larch_dump = {
            'id': '1',
            'uri': 'http://id.trees.org/1',
            'type': 'concept',
            'labels': [
                {'type': 'prefLabel', 'language': 'en', 'label': 'The Larch'},
                {'type': 'prefLabel', 'language': 'nl', 'label': 'De Lariks'}
            ],
            'notes': [
                {'type': 'definition',
                 'language': 'en',
                 'note': 'A type of tree.'}
            ],
            'narrower': [],
            'broader': [],
            'related': [],
            'member_of': ['3']
        }
        self.chestnut_dump = {
            'id': '2',
            'uri': 'http://id.trees.org/2',
            'type': 'concept',
            'labels': [
                {'type': 'prefLabel',
                 'language': 'en',
                 'label': 'The Chestnut'},
                {'type': 'altLabel',
                 'language': 'nl',
                 'label': 'De Paardekastanje'},
                {'type': 'altLabel',
                 'language': 'fr',
                 'label': 'la châtaigne'}
            ],
            'notes': [
                {
                    'type': 'definition', 'language': 'en',
                    'note': 'A different type of tree.'
                }
            ],
            'narrower': [],
            'broader': [],
            'related': [],
            'member_of': ['3']
        }
        self.species_dump = {
            'id': 3,
            'uri': 'http://id.trees.org/3',
            'labels': [
                {'type': 'prefLabel', 'language': 'en', 'label': 'Trees by species'},
                {'type': 'prefLabel', 'language': 'nl', 'label': 'Bomen per soort'}
            ],
            'type': 'collection',
            'members': ['1', '2'],
            'member_of': []
        }
        self.world_dump = {
            'id': '1',
            'uri': 'urn:x-skosprovider:geography:1',
            'type': 'concept',
            'labels': [
                {'type': 'prefLabel', 'language': 'en', 'label': 'World'}
            ],
            'notes': [
            ],
            'narrower': [2, 3],
            'broader': [],
            'related': [],
            'member_of': []
        }

        self.tree_provider = DictionaryProvider({'id': 'TREE'}, [self.larch_dump,self.chestnut_dump,self.species_dump])
        self.world_provider = DictionaryProvider({'id': 'WORLD'}, [self.world_dump])
        # Set up rdf_provider
        self.rdf_products_provider = RDFProvider(
            {'id': 'PRODUCTS', 'conceptscheme_id': 1}, self.graph)


    def _get_materials_provider(self):
        import json
        materials_data = json.load(
        open(os.path.join(os.path.dirname(__file__), 'data', 'materiaal.txt')),
        )['materiaal']
        from skosprovider.providers import DictionaryProvider
        from skosprovider.uri import UriPatternGenerator
        materials = DictionaryProvider(
            {'id': 'Materials'},
            materials_data,
            uri_generator=UriPatternGenerator('https://id.erfgoed.net/thesauri/materialen/%s')
        )
        return materials

    def test_dump_dictionary_to_rdf(self):
        graph_dump = utils.rdf_dumper(self._get_materials_provider())
        xml = graph_dump.serialize(format='xml', encoding="UTF-8")
        if isinstance(xml,bytes):
            xml=xml.decode("UTF-8")
        self.assertEquals("<?xml", xml[:5])
        bont_skos_definition = '<skos:definition xml:lang="nl-BE">Bont is een gelooide dierlijke huid, dicht bezet met haren. Het wordt voornamelijk gebruikt voor het maken van kleding.</skos:definition>'
        self.assertIn(bont_skos_definition, xml)

    def test_dump_rdf_to_rdf(self):
        graph_dump = utils.rdf_dumper(self.rdf_products_provider)
        xml = graph_dump.serialize(format='xml', encoding="UTF-8")
        if isinstance(xml,bytes):
            xml=xml.decode("UTF-8")
        self.assertEquals("<?xml", xml[:5])

    def test_dump_rdf_compare_type(self):
        graph_dump = utils.rdf_dumper(self.rdf_products_provider)
        self.assertEquals(type(graph_dump), Graph)

    def test_dump_tree_to_rdf(self):
        graph_dump = utils.rdf_dumper(self.tree_provider)
        xml = graph_dump.serialize(format='xml', encoding="UTF-8")
        if isinstance(xml,bytes):
            xml=xml.decode("UTF-8")
        self.assertEquals("<?xml", xml[:5])

    def test_include_me(self):
        return