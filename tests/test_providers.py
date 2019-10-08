# -*- coding: utf-8 -*-

import unittest
import os
import sys

import pytest

from skosprovider.skos import Note, Collection, ConceptScheme
from skosprovider.utils import dict_dumper

from rdflib import Graph
from skosprovider_rdf.providers import RDFProvider

PY3 = sys.version_info[0] == 3

if PY3:  # pragma: no cover
    text_type = str
else:  # pragma: no cover
    text_type = unicode


class RDFProviderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        return

    def setUp(self):
        # Set up testdata
        self._create_test_data()

        # Set up providers
        self.products_provider = RDFProvider(
            {'id': 'PRODUCTS'}, self.products_graph)
        self.toepassingen_provider = RDFProvider(
            {'id': 'TOEPASSINGEN'}, self.toepassingen_graph)

    def tearDown(self):
        return

    def _create_test_data(self):
        self.products_graph = Graph()
        filepath = os.path.dirname(os.path.realpath(__file__))
        abspath = os.path.abspath(filepath + "/data/simple_turtle_products")
        self.products_graph.parse(abspath, format="turtle")

        self.u_products = "http://www.products.com/"
        self.u_jewellery = "http://www.products.com/Jewellery"
        self.u_perfume = "http://www.products.com/Perfume"
        self.u_product = "http://www.products.com/Product"
        self.u_stuff = "http://www.products.com/Stuff"
        self.u_unexistingProduct = "http://www.products.com/UnexistingProduct"

        self.toepassingen_graph = Graph()
        filepath = os.path.dirname(os.path.realpath(__file__))
        abspath = os.path.abspath(filepath + "/data/toepassingen.xml")
        self.toepassingen_graph.parse(abspath, format="application/rdf+xml")

        self.trees_graph = Graph()
        filepath = os.path.dirname(os.path.realpath(__file__))
        abspath = os.path.abspath(filepath + "/data/trees.xml")
        self.trees_graph.parse(abspath, format="application/rdf+xml")

    def test_include(self):
        return

    def test_get_vocabulary_id(self):
        self.assertEquals('PRODUCTS', self.products_provider.get_vocabulary_id())

    def test_conceptscheme(self):
        cs = self.products_provider.concept_scheme

        assert cs.uri == self.u_products + 'Scheme'
        assert cs.label('en') is not None
        assert len(cs.languages) == 3

    def test_too_many_conceptscheme(self):
        self.toepassingen_graph = Graph()
        filepath = os.path.dirname(os.path.realpath(__file__))
        abspath = os.path.abspath(filepath + "/data/schemes.xml")
        self.toepassingen_graph.parse(abspath, format="application/rdf+xml")
        with pytest.raises(RuntimeError) as exc:
            self.toepassingen_provider = RDFProvider(
                {'id': 'TOEPASSINGEN'}, self.toepassingen_graph
            )
        assert 'https://id.erfgoed.net/toepassingen' in str(exc.value)
        assert 'https://id.erfgoed.net/applicaties' in str(exc.value)

    def test_parse_without_conceptscheme_generates_default_uri(self):
        trees_provider = RDFProvider(
            {'id': 'TREES'}, self.trees_graph
        )
        assert 'urn:x-skosprovider:trees' == trees_provider.concept_scheme.uri

    def test_pick_one_conceptscheme(self):
        self.wb_graph = Graph()
        filepath = os.path.dirname(os.path.realpath(__file__))
        abspath = os.path.abspath(filepath + "/data/waarde_en_besluit_types.ttl")
        self.wb_graph.parse(abspath, format="turtle")
        self.wb_provider = RDFProvider(
            {'id': 'WAARDETYPES'},
            self.wb_graph,
            concept_scheme_uri = 'https://id.erfgoed.net/thesauri/waardetypes'
        )
        assert 'https://id.erfgoed.net/thesauri/waardetypes' == self.wb_provider.concept_scheme.uri
        assert len(self.wb_provider.get_all()) == 21

    def test_set_a_conceptscheme_manually(self):
        self.wb_graph = Graph()
        filepath = os.path.dirname(os.path.realpath(__file__))
        abspath = os.path.abspath(filepath + "/data/waarde_en_besluit_types.ttl")
        self.wb_graph.parse(abspath, format="turtle")
        self.wb_provider = RDFProvider(
            {'id': 'BESLUITTYPES'},
            self.wb_graph,
            concept_scheme = ConceptScheme(
                'https://id.erfgoed.net/thesauri/besluittypes',
            )
        )
        assert 'https://id.erfgoed.net/thesauri/besluittypes' == self.wb_provider.concept_scheme.uri
        assert len(self.wb_provider.get_all()) == 24

    def test_pick_wrong_conceptscheme(self):
        self.wb_graph = Graph()
        filepath = os.path.dirname(os.path.realpath(__file__))
        abspath = os.path.abspath(filepath + "/data/waarde_en_besluit_types.ttl")
        self.wb_graph.parse(abspath, format="turtle")
        with pytest.raises(RuntimeError) as exc:
            self.wb_provider = RDFProvider(
                {'id': 'WAARTYPES'},
                self.wb_graph,
                concept_scheme_uri = 'https://id.erfgoed.net/thesauri/waartypes'
            )
        assert 'https://id.erfgoed.net/thesauri/waardetypes' in str(exc.value)
        assert 'https://id.erfgoed.net/thesauri/besluittypes' in str(exc.value)

    def test_get_concept_by_id(self):
        from skosprovider.skos import Concept
        con = self.products_provider.get_by_id(self.u_jewellery)
        self.assertIsInstance(con, Concept)
        self.assertEqual(self.u_jewellery, con.id)
        self.assertEqual([self.u_perfume], con.related)

        con = self.toepassingen_provider.get_by_id('1')
        self.assertEqual('https://id.erfgoed.net/toepassingen/1', con.uri)
        self.assertEqual('1', str(con.id))

    def test_get_unexisting_by_id(self):
        con = self.products_provider.get_by_id(404)
        self.assertFalse(con)

    def test_createLabel(self):
        with self.assertRaises(ValueError):
            self.products_provider._create_label("literal","nonexistinglabeltype")

    def test_createNote(self):
        with self.assertRaises(ValueError):
            self.products_provider._create_note("literal","nonexistingnotetype")

    def test_get_concept_by_uri(self):
        cona = self.products_provider.get_by_id(self.u_product)
        conb = self.products_provider.get_by_uri(self.u_product)
        self.assertEqual(cona.id, conb.id)
        self.assertEqual(cona.uri, conb.uri)

    def test_get_unexisting_by_uri(self):
        con = self.products_provider.get_by_uri(self.u_unexistingProduct)
        self.assertFalse(con)

    def test_concept_has_correct_note(self):
        con = self.products_provider.get_by_id(self.u_jewellery)
        self.assertEqual(2, len(con.notes))
        self.assertIsInstance(con.notes[0], Note)

    def test_get_collection_by_id(self):
        col = self.products_provider.get_by_id(self.u_stuff)
        self.assertIsInstance(col, Collection)
        self.assertEquals(self.u_stuff, col.id)
        self.assertTrue(self.u_product in col.members)
        for m in col.members:
            m = self.products_provider.get_by_id(m)
            self.assertIn(col.id, m.member_of)

    def test_get_collection_by_uri(self):
        cola = self.products_provider.get_by_id(self.u_stuff)
        colb = self.products_provider.get_by_uri(self.u_stuff)
        self.assertEqual(cola.id, colb.id)
        self.assertEqual(cola.uri, colb.uri)

    def test_get_all(self):
        all = self.products_provider.get_all()
        self.assertEquals(4, len(all))

    def test_get_top_concepts(self):
        all = self.products_provider.get_top_concepts()
        self.assertEquals(1, len(all))

    def test_get_top_display(self):
        all = self.products_provider.get_top_display()
        self.assertEquals(1, len(all))

    def test_get_children_display_unexisting(self):
        children = self.products_provider.get_children_display(700)
        self.assertFalse(children)

    def test_get_children_display_collection(self):
        children = self.products_provider.get_children_display(self.u_stuff)
        self.assertEquals(3, len(children))

    def test_get_children_display_concept(self):
        children = self.products_provider.get_children_display(self.u_product)
        self.assertEquals(2, len(children))

    def test_find_all(self):
        all = self.products_provider.find({})
        self.assertEquals(4, len(all))

    def test_find_type_all(self):
        all = self.products_provider.find({'type': 'all'})
        self.assertEquals(4, len(all))

    def test_find_type_concept(self):
        all = self.products_provider.find({'type': 'concept'})
        self.assertEquals(3, len(all))

    def test_find_type_collection(self):
        all = self.products_provider.find({'type': 'collection'})
        self.assertEquals(1, len(all))

    def test_find_label_perfume(self):
        all = self.products_provider.find({'label': 'Perfume'})
        self.assertEquals(1, len(all))

    def test_find_label_perfume_type_concept(self):
        all = self.products_provider.find({'label': 'Perfume', 'type': 'concept'})
        self.assertEquals(1, len(all))

    def test_find_collection_unexisting(self):
        self.assertRaises(
            ValueError,
            self.products_provider.find,
            {'collection': {'id': 404}}
        )

    def test_find_collection_stuff_no_depth(self):
        all = self.products_provider.find({'collection': {'id': self.u_stuff}})
        self.assertEquals(3, len(all))

    def test_expand_concept(self):
        ids = self.products_provider.expand(self.u_product)
        self.assertIn(self.u_perfume, ids)

    def test_expand_collection(self):
        ids = self.products_provider.expand(self.u_stuff)
        self.assertIn(self.u_perfume, ids)

    def test_expand_unexisting(self):
        ids = self.products_provider.expand(404)
        self.assertFalse(ids)

    def test_no_literal(self):
        self.assertIsNone(self.products_provider._get_language_from_literal("test"))

    def test_rdf_provider_list(self):
        rdf_prov = RDFProvider(
            {'id': 'TREES'},
            self.trees_graph
        )
        dump = dict_dumper(rdf_prov)

        self.assertEqual(len(dump), 3)
        chestnut = [item for item in dump if item['uri'] == 'http://id.trees.org/2'][0]
        self.assertEqual(chestnut['broader'], [])
        self.assertEqual(chestnut['id'], '2')
        self.assertEqual(chestnut['member_of'], ['3'])
        self.assertEqual(chestnut['narrower'], [])
        label_en = [label for label in chestnut['labels'] if label['language'] == 'en'][0]
        self.assertDictEqual(label_en, {'label': 'The Chestnut', 'language': 'en', 'type': 'prefLabel'})
        label_nl = [label for label in chestnut['labels'] if label['language'] == 'nl'][0]
        self.assertDictEqual(label_nl, {'label': 'De Paardekastanje', 'language': 'nl', 'type': 'altLabel'})
        label_fr = [label for label in chestnut['labels'] if label['language'] == 'fr'][0]
        self.assertEqual(type(label_fr['label']), text_type)
        self.assertDictEqual(label_fr, {'label': u'la châtaigne', 'language': 'fr', 'type': 'altLabel'})
        assert {
                'language': 'en',
                'note': '<p>A different type of tree.</p>',
                'type': 'definition',
                'markup': 'HTML'
            } in chestnut['notes']
        assert {
                'language': 'und',
                'note': 'Een ander soort boom.',
                'type': 'definition',
                'markup': 'HTML'
            } in chestnut['notes']
        assert {
                'markup': 'HTML',
                'citation': '<strong>Monthy Python.</strong> Episode Three: How to recognise different types of trees from quite a long way away.'
        } in chestnut['sources']
        larch = [item for item in dump if item['uri'] == 'http://id.trees.org/1'][0]
        assert {
                'citation': 'Monthy Python. Episode Three: How to recognise different types of trees from quite a long way away.',
                'markup': None
            } in larch['sources']
        assert {
                'language': 'en',
                'note': 'A type of tree.',
                'type': 'definition',
                'markup': None
            } in larch['notes']
        assert {
                'language': 'nl',
                'note': '<p>Een soort boom.</p>',
                'type': 'definition',
                'markup': 'HTML'
            } in larch['notes']
