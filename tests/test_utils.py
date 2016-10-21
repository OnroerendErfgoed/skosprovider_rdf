# -*- coding: utf-8 -*-
import unittest
import os
from rdflib import Graph
from rdflib.namespace import RDF, SKOS, DCTERMS
from rdflib.term import URIRef, Literal

from skosprovider.providers import DictionaryProvider
from skosprovider.skos import (
    ConceptScheme,
    Label,
    Note
)

from skosprovider_rdf.providers import RDFProvider
from skosprovider_rdf import utils

from skosprovider_rdf.utils import (
    _add_lang_to_html,
    extract_language
)

import logging
log = logging.getLogger(__name__)


# unittest.TestCase
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
                {
                    'type': 'definition',
                    'language': 'en',
                    'note': 'A type of tree.'
                }, {
                    'type': 'definition',
                    'language': 'nl',
                    'note': '<p>Een soort boom.</p>',
                    'markup': 'HTML'
                }
            ],
            'narrower': [],
            'broader': [],
            'related': [],
            'member_of': ['3'],
            'sources': [
                {'citation': 'Monthy Python. Episode Three: How to recognise different types of trees from quite a long way away.'}
            ]
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
            'member_of': ['3'],
            'subordinate_arrays': [],
            'sources': [
                {
                    'citation': '<strong>Monthy Python.</strong> Episode Three: How to recognise different types of trees from quite a long way away.',
                    'markup': 'HTML'
                }
            ]
        }
        self.oak_dump = {
            'id': '4',
            'uri': 'http://id.trees.org/4',
            'type': 'concept',
            'labels': [
                {'type': 'prefLabel',
                 'language': 'en',
                 'label': 'The Oak'},
                {'type': 'altLabel',
                 'language': 'nl',
                 'label': 'De Eik'},
                {'type': 'altLabel',
                 'language': 'fr',
                 'label': 'le chêne'}
            ],
            'notes': [
                {
                    'type': 'definition', 'language': 'en',
                    'note': 'A different type of tree.'
                }
            ],
            'narrower': ['6'],
            'broader': ['6'],
            'related': ['6'],
            'member_of': ['6'],
            'subordinate_arrays': ['6', '3'],
            'matches': {
                'exact': ['http://blabla/2'],
                'narrow': ['http://blabla/1', 'http://blabla/5'],
            }
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
            'member_of': [],
            'superordinates': ['6', '4']
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
            'member_of': [],
            'subordinate_arrays': []
        }

        self.tree_provider = DictionaryProvider(
            {
                'id': 'TREE',
                'dataset': {
                    'uri': 'https://id.trees.org/dataset'
                }
            },
            [self.larch_dump, self.chestnut_dump, self.species_dump],
            concept_scheme=ConceptScheme(
                uri='http://id.trees.org',
                labels=[
                    Label(
                        'Pythonic trees.',
                        type='prefLabel',
                        language='en'
                    ), 
                    Label(
                        'Pythonische bomen.',
                        type='prefLabel',
                        language=None
                    )
                ],
                notes=[
                    Note(
                        '<p>Trees as used by Monthy Python.</p>',
                        type='definition',
                        language='en',
                        markup='HTML'
                    )
                ]
            )
        )
        self.tree_provider2 = DictionaryProvider({'id': 'TREE'},
                                                [self.oak_dump, self.chestnut_dump, self.species_dump])
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

    def test_dump_dictionary_to_rdf(self):
        graph_dump = utils.rdf_dumper(self._get_materials_provider())
        xml = graph_dump.serialize(format='xml', encoding="UTF-8")
        if isinstance(xml, bytes):
            xml = xml.decode("UTF-8")
        print (xml)
        self.assertEquals("<?xml", xml[:5])
        bont_skos_definition = '<skos:definition xml:lang="nl-BE">Bont is een gelooide dierlijke huid, dicht bezet met haren. Het wordt voornamelijk gebruikt voor het maken van kleding.</skos:definition>'
        dcterms_id_skos_definition = '<dcterms:identifier rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">9</dcterms:identifier>'
        self.assertIn(bont_skos_definition, xml)
        self.assertIn(dcterms_id_skos_definition, xml)

    def test_dump_rdf_to_rdf(self):
        graph_dump = utils.rdf_dumper(self.rdf_products_provider)
        xml = graph_dump.serialize(format='xml', encoding="UTF-8")
        if isinstance(xml, bytes):
            xml = xml.decode("UTF-8")
        self.assertEquals("<?xml", xml[:5])

    def test_dump_rdf_compare_type(self):
        graph_dump = utils.rdf_dumper(self.rdf_products_provider)
        self.assertEquals(type(graph_dump), Graph)

    def test_dump_tree_to_rdf(self):
        graph_dump = utils.rdf_dumper(self.tree_provider)
        xml = graph_dump.serialize(format='xml', encoding="UTF-8")
        if isinstance(xml, bytes):
            xml = xml.decode("UTF-8")
        self.assertEquals("<?xml", xml[:5])

    def test_dump_larch_to_rdf(self):
        graph_dump = utils.rdf_c_dumper(self.tree_provider, 1)
        cs = URIRef('http://id.trees.org')
        assert (cs, RDF.type, SKOS.ConceptScheme) in graph_dump
        assert (cs, SKOS.definition, Literal('<p xml:lang="en">Trees as used by Monthy Python.</p>', datatype=RDF.HTML)) in graph_dump
        assert (cs, SKOS.prefLabel, Literal('Pythonic trees.', lang='en')) in graph_dump
        xml = graph_dump.serialize(format='xml', encoding="UTF-8")
        if isinstance(xml, bytes):
            xml = xml.decode("UTF-8")
        self.assertEquals("<?xml", xml[:5])

    def test_dump_chestnut_to_rdf(self):
        graph_dump = utils.rdf_c_dumper(self.tree_provider, 2)
        citations = graph_dump.objects(predicate=DCTERMS.bibliographicCitation)
        for c in citations:
            assert Literal(
                '<strong>Monthy Python.</strong> Episode Three: How to recognise different types of trees from quite a long way away.', 
                datatype=RDF.HTML
            ) == c

    def test_dump_tree_to_rdf_2(self):
        graph_dump = utils.rdf_dumper(self.tree_provider2)
        xml = graph_dump.serialize(format='xml', encoding="UTF-8")
        if isinstance(xml, bytes):
            xml = xml.decode("UTF-8")
        self.assertEquals("<?xml", xml[:5])

    def test_dump_one_id_to_rdf_and_reload(self):
        graph_dump1 = utils.rdf_c_dumper(self.tree_provider, 1)
        provider = RDFProvider(
            {
                'id': 'Number1',
                'dataset': {
                    'uri': 'http://id.trees.org/dataset'
                }
            },
            graph_dump1
        )
        graph_dump2 = utils.rdf_c_dumper(provider, 1)
        graph_full_dump2 = utils.rdf_dumper(provider)
        assert len(graph_dump1) ==  len(graph_dump2)
        assert len(graph_full_dump2) > len(graph_dump2)

    def test_dump_conceptscheme_tree_to_rdf(self):
        graph_dump = utils.rdf_conceptscheme_dumper(self.tree_provider)
        cs = URIRef('http://id.trees.org')
        assert (cs, RDF.type, SKOS.ConceptScheme) in graph_dump
        assert (cs, SKOS.definition, Literal('<p xml:lang="en">Trees as used by Monthy Python.</p>', datatype=RDF.HTML)) in graph_dump
        assert (cs, SKOS.prefLabel, Literal('Pythonic trees.', lang='en')) in graph_dump

    def test_extract_language_None(self):
        assert 'und' == extract_language(None)


class TestHtml:

    def test_lang_und(self):
        assert '' == _add_lang_to_html('', 'und')
        assert '<p></p>' == _add_lang_to_html('<p></p>', 'und')

    def test_lang_no_html(self):
        assert '<div xml:lang="en"></div>' == _add_lang_to_html('', 'en')

    def test_no_single_child(self):
        html = '<p>Paragraph 1</p><p>Paragraph2</p>'
        assert '<div xml:lang="en"><p>Paragraph 1</p><p>Paragraph2</p></div>' == _add_lang_to_html(html, 'en')

    def test_text_node(self):
        html = 'Something'
        assert '<div xml:lang="en">Something</div>' == _add_lang_to_html(html, 'en')

    def test_single_child_no_attributes(self):
        html = '<p>Paragraph 1</p>'
        assert '<p xml:lang="en">Paragraph 1</p>' == _add_lang_to_html(html, 'en')

    def test_single_child_already_has_langs(self):
        html = '<p xml:lang="en">Paragraph 1</p>'
        assert '<p xml:lang="en">Paragraph 1</p>' == _add_lang_to_html(html, 'en')

    def test_single_child_other_attributes(self):
        html = '<p class="something">Paragraph 1</p>'
        assert '<p class="something" xml:lang="en">Paragraph 1</p>' == _add_lang_to_html(html, 'en')
