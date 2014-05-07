import unittest
from rdflib import Graph
from rdflib.namespace import RDF, SKOS
from skosprovider_rdf.providers import RDFProvider
from skosprovider_rdf import utils
from rdflib.term import URIRef


#unittest.TestCase
class RDFProviderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        return

    def setUp(self):
        # Set up testdata
        self._create_test_data()

        # Set up provider
        self.provider = RDFProvider(
            {'id': 'PRODUCTS', 'conceptscheme_id': 1}, self.graph)

    def tearDown(self):
        return

    def _create_test_data(self):
        self.graph = Graph()
        self.graph.parse("../tests/data/simple_turtle_products", format="turtle")

        self.u_products=URIRef("http://www.products.com/")
        self.u_jewellery=URIRef("http://www.products.com/Jewellery")
        self.u_perfume=URIRef("http://www.products.com/Perfume")
        self.u_product=URIRef("http://www.products.com/Product")
        self.u_stuff=URIRef("http://www.products.com/Stuff")

    def test_include(self):
        return

    def test_get_vocabulary_id(self):
        self.assertEquals('PRODUCTS', self.provider.get_vocabulary_id())

    def test_get_concept_by_id(self):
        from skosprovider.skos import Concept
        con = self.provider.get_by_id(self.u_jewellery)
        self.assertIsInstance(con, Concept)
        self.assertEqual(self.u_jewellery, con.id)
        self.assertEqual([self.u_perfume], con.related)

    def test_get_unexisting_by_id(self):
        con = self.provider.get_by_id(404)
        self.assertFalse(con)

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
