import unittest,os
from rdflib import Graph
from skosprovider.skos import Note,Label,Collection,Concept
from rdflib.namespace import RDF, SKOS
from skosprovider_rdf.providers import RDFProvider
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
        filepath=os.path.dirname(os.path.realpath(__file__))
        abspath=os.path.abspath(filepath + "/data/simple_turtle_products")
        self.graph.parse(abspath, format="turtle")

        self.u_products=URIRef("http://www.products.com/")
        self.u_jewellery=URIRef("http://www.products.com/Jewellery")
        self.u_perfume=URIRef("http://www.products.com/Perfume")
        self.u_product=URIRef("http://www.products.com/Product")
        self.u_stuff=URIRef("http://www.products.com/Stuff")
        self.u_unexistingProduct=URIRef("http://www.products.com/UnexistingProduct")

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

    def test_createLabel(self):
        with self.assertRaises(ValueError):
            self.provider._create_label("literal","nonexistinglabeltype")

    def test_createNote(self):
        with self.assertRaises(ValueError):
            self.provider._create_note("literal","nonexistingnotetype")

    def test_get_concept_by_uri(self):
        cona = self.provider.get_by_id(self.u_product)
        conb = self.provider.get_by_uri(self.u_product)
        self.assertEqual(cona.id, conb.id)
        self.assertEqual(cona.uri, conb.uri)

    def test_get_unexisting_by_uri(self):
        con = self.provider.get_by_uri(self.u_unexistingProduct)
        self.assertFalse(con)


    def test_concept_has_correct_note(self):
        con = self.provider.get_by_id(self.u_jewellery)
        self.assertEqual(2, len(con.notes))
        self.assertIsInstance(con.notes[0], Note)

    def test_get_collection_by_id(self):
        col = self.provider.get_by_id(self.u_stuff)
        self.assertIsInstance(col, Collection)
        self.assertEquals(self.u_stuff, col.id)
        self.assertTrue(self.u_product in col.members)

    def test_get_collection_by_uri(self):
        cola = self.provider.get_by_id(self.u_stuff)
        colb = self.provider.get_by_uri(self.u_stuff)
        self.assertEqual(cola.id, colb.id)
        self.assertEqual(cola.uri, colb.uri)

    def test_get_all(self):
        all = self.provider.get_all()
        self.assertEquals(4, len(all))

    def test_get_top_concepts(self):
        all = self.provider.get_top_concepts()
        self.assertEquals(1, len(all))

    def test_get_top_display(self):
        all = self.provider.get_top_display()
        self.assertEquals(1, len(all))

    def test_get_children_display_unexisting(self):
        children = self.provider.get_children_display(700)
        self.assertFalse(children)

    def test_get_children_display_collection(self):
        children = self.provider.get_children_display(self.u_stuff)
        self.assertEquals(3, len(children))

    def test_get_children_display_concept(self):
        children = self.provider.get_children_display(self.u_product)
        self.assertEquals(2, len(children))

    def test_find_all(self):
        all = self.provider.find({})
        self.assertEquals(4, len(all))

    def test_find_type_all(self):
        all = self.provider.find({'type': 'all'})
        self.assertEquals(4, len(all))

    def test_find_type_concept(self):
        all = self.provider.find({'type': 'concept'})
        self.assertEquals(3, len(all))

    def test_find_type_collection(self):
        all = self.provider.find({'type': 'collection'})
        self.assertEquals(1, len(all))

    def test_find_label_perfume(self):
        all = self.provider.find({'label': 'Perfume'})
        self.assertEquals(1, len(all))

    def test_find_label_perfume_type_concept(self):
        all = self.provider.find({'label': 'Perfume', 'type': 'concept'})
        self.assertEquals(1, len(all))

    def test_find_collection_unexisting(self):
        self.assertRaises(
            ValueError,
            self.provider.find,
            {'collection': {'id': 404}}
        )

    def test_find_collection_stuff_no_depth(self):
        all = self.provider.find({'collection': {'id': self.u_stuff}})
        self.assertEquals(3, len(all))

    def test_expand_concept(self):
        ids = self.provider.expand_concept(self.u_product)
        self.assertIn(self.u_perfume, ids)

    def test_expand_collection(self):
        ids = self.provider.expand(self.u_stuff)
        self.assertIn(self.u_perfume, ids)

    def test_expand_unexisting(self):
        ids = self.provider.expand(404)
        self.assertFalse(ids)
