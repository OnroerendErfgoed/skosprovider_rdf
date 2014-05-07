import unittest

# -*- coding: utf-8 -*-

# try:
#     import unittest2 as unittest
# except ImportError:  # pragma NO COVER
#     import unittest  # noqa

from skosprovider_rdf.providers import (
    RDFProvider
)

#unittest.TestCase
class RDFProviderTests(unittest.TestCase):

    def setUp(self):
         # Set up testdata
        self._create_test_data()

        # Set up provider
        self.provider = RDFProvider(
            {'id': 'SOORTEN', 'conceptscheme_id': 2},self.graph)

    def tearDown(self):
        return

    def example(self):
       # Set up testdata
        self._create_test_data()
        # # Set up provider
        # self.provider = RDFProvider(
        #     {'id': 'SOORTEN', 'conceptscheme_id': 2},self.graph)

    def _create_test_data(self):
        """
        tester

        """
        from rdflib import Graph
        graph = Graph()
        graph.parse("./data/simple_skos.xml", format="xml")
        graph.triples()

    def test_include(self):
        return

    # def test_get_vocabulary_id(self):
    #     self.assertEquals('SOORTEN', self.provider.get_vocabulary_id())
    #
    # def test_get_concept_by_id(self):
    #     from skosprovider.skos import Concept
    #     con = self.provider.get_by_id(1)
    #     self.assertIsInstance(con, Concept)
    #     self.assertEqual(1, con.id)
    #     self.assertEqual([3], con.related)
    #     self.assertEqual([4], con.narrower)
    #
    # def test_get_concept_by_id_string(self):
    #     from skosprovider.skos import Concept
    #     con = self.provider.get_by_id('1')
    #     self.assertIsInstance(con, Concept)
    #     self.assertEqual(1, con.id)
    #     self.assertEqual([3], con.related)
    #     self.assertEqual([4], con.narrower)
    #
    # def test_get_unexisting_by_id(self):
    #     con = self.provider.get_by_id(404)
    #     self.assertFalse(con)
    #
    # def test_get_concept_by_uri(self):
    #     from skosprovider.skos import Concept
    #     cona = self.provider.get_by_id(1)
    #     conb = self.provider.get_by_uri('urn:x-skosprovider:test:1')
    #     self.assertEqual(cona.id, conb.id)
    #     self.assertEqual(cona.uri, conb.uri)
    #
    # def test_get_unexisting_by_uri(self):
    #     con = self.provider.get_by_uri('urn:x-skosprovider:test:404')
    #     self.assertFalse(con)
    #
    #
    # def test_concept_has_correct_note(self):
    #     from skosprovider.skos import Note
    #     cath = self.provider.get_by_id(4)
    #     self.assertEqual(1, len(cath.notes))
    #     self.assertIsInstance(cath.notes[0], Note)
    #
    # def test_get_collection_by_id(self):
    #     from skosprovider.skos import Collection
    #     col = self.provider.get_by_id(2)
    #     self.assertIsInstance(col, Collection)
    #     self.assertEquals(2, col.id)
    #     self.assertEquals([1], col.members)
    #
    # def test_get_collection_by_uri(self):
    #     from skosprovider.skos import Collection
    #     cola = self.provider.get_by_id(2)
    #     colb = self.provider.get_by_uri('urn:x-skosprovider:test:2')
    #     self.assertEqual(cola.id, colb.id)
    #     self.assertEqual(cola.uri, colb.uri)
    #
    # def test_get_all(self):
    #     all = self.provider.get_all()
    #     self.assertEquals(4, len(all))
    #     self.assertIn({'id': 1, 'label': 'Churches'}, all)
    #     self.assertIn({'id': 2, 'label': 'Churches by function'}, all)
    #     self.assertIn({'id': 3, 'label': 'Chapels'}, all)
    #     self.assertIn({'id': 4, 'label': 'Cathedrals'}, all)
    #
    # def test_get_top_concepts(self):
    #     all = self.provider.get_top_concepts()
    #     self.assertEquals(2, len(all))
    #     self.assertIn({'id': 1, 'label': 'Churches'}, all)
    #     self.assertIn({'id': 3, 'label': 'Chapels'}, all)
    #
    # def test_get_top_display(self):
    #     all = self.provider.get_top_display()
    #     self.assertEquals(2, len(all))
    #     self.assertIn({'id': 3, 'label': 'Chapels'}, all)
    #     self.assertIn({'id': 2, 'label': 'Churches by function'}, all)
    #
    # def test_get_children_display_unexisting(self):
    #     children = self.provider.get_children_display(700)
    #     self.assertFalse(children)
    #
    # def test_get_children_display_collection(self):
    #     children = self.provider.get_children_display(2)
    #     self.assertEquals(1, len(children))
    #     self.assertIn({'id': 1, 'label': 'Churches'}, children)
    #
    # def test_get_children_display_concept(self):
    #     children = self.provider.get_children_display(1)
    #     self.assertEquals(1, len(children))
    #     self.assertIn({'id': 4, 'label': 'Cathedrals'}, children)
    #
    # def test_find_all(self):
    #     all = self.provider.find({})
    #     self.assertEquals(4, len(all))
    #     self.assertIn({'id': 1, 'label': 'Churches'}, all)
    #     self.assertIn({'id': 2, 'label': 'Churches by function'}, all)
    #     self.assertIn({'id': 3, 'label': 'Chapels'}, all)
    #     self.assertIn({'id': 4, 'label': 'Cathedrals'}, all)
    #
    # def test_find_type_all(self):
    #     all = self.provider.find({'type': 'all'})
    #     self.assertEquals(4, len(all))
    #     self.assertIn({'id': 1, 'label': 'Churches'}, all)
    #     self.assertIn({'id': 2, 'label': 'Churches by function'}, all)
    #     self.assertIn({'id': 3, 'label': 'Chapels'}, all)
    #     self.assertIn({'id': 4, 'label': 'Cathedrals'}, all)
    #
    # def test_find_type_concept(self):
    #     all = self.provider.find({'type': 'concept'})
    #     self.assertEquals(3, len(all))
    #     self.assertIn({'id': 1, 'label': 'Churches'}, all)
    #     self.assertIn({'id': 3, 'label': 'Chapels'}, all)
    #     self.assertIn({'id': 4, 'label': 'Cathedrals'}, all)
    #
    # def test_find_type_collection(self):
    #     all = self.provider.find({'type': 'collection'})
    #     self.assertEquals(1, len(all))
    #     self.assertIn({'id': 2, 'label': 'Churches by function'}, all)
    #
    # def test_find_label_kerken(self):
    #     all = self.provider.find({'label': 'kerken'})
    #     self.assertEquals(1, len(all))
    #     self.assertIn({'id': 1, 'label': 'Churches'}, all)
    #
    # def test_find_label_churches_type_concept(self):
    #     all = self.provider.find({'label': 'churches', 'type': 'concept'})
    #     self.assertEquals(1, len(all))
    #     self.assertIn({'id': 1, 'label': 'Churches'}, all)
    #
    # def test_find_collection_unexisting(self):
    #     self.assertRaises(
    #         ValueError,
    #         self.provider.find,
    #         {'collection': {'id': 404}}
    #     )
    #
    # def test_find_collection_2_no_depth(self):
    #     all = self.provider.find({'collection': {'id': 2}})
    #     self.assertEquals(1, len(all))
    #     self.assertIn({'id': 1, 'label': 'Churches'}, all)
    #
    # def test_expand_concept(self):
    #     ids = self.provider.expand_concept(1)
    #     self.assertEquals([1, 4], ids)
    #
    # def test_expand_collection(self):
    #     ids = self.provider.expand(2)
    #     self.assertEquals([1, 4], ids)
    #
    # def test_expand_concept_without_narrower(self):
    #     ids = self.provider.expand(3)
    #     self.assertEquals([3], ids)
    #
    # def test_expand_unexisting(self):
    #     ids = self.provider.expand(404)
    #     self.assertFalse(ids)
