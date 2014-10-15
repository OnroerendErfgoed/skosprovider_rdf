import unittest,os
from rdflib import Graph
from skosprovider.skos import Note,Label,Collection,Concept, ConceptScheme
from rdflib.namespace import RDF, SKOS
from skosprovider_rdf.providers import RDFProvider
from rdflib.term import URIRef


#unittest.TestCase
from skosprovider_rdf.utils import uri_to_graph, rdf_dumper


class RDFProviderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        return

    def setUp(self):
        # Set up testdata
        self._create_test_data()

        # Set up providers
        self.products_provider = RDFProvider(
            {'id': 'PRODUCTS', 'conceptscheme_id': 1}, self.products_graph)
        self.toepassingen_provider = RDFProvider(
            {'id': 'TOEPASSINGEN', 'conceptscheme_id': 2}, self.toepassingen_graph)

    def tearDown(self):
        return

    def _create_test_data(self):
        self.products_graph = Graph()
        filepath=os.path.dirname(os.path.realpath(__file__))
        abspath=os.path.abspath(filepath + "/data/simple_turtle_products")
        self.products_graph.parse(abspath, format="turtle")

        self.u_products="http://www.products.com/"
        self.u_jewellery="http://www.products.com/Jewellery"
        self.u_perfume="http://www.products.com/Perfume"
        self.u_product="http://www.products.com/Product"
        self.u_stuff="http://www.products.com/Stuff"
        self.u_unexistingProduct="http://www.products.com/UnexistingProduct"

        self.toepassingen_graph = Graph()
        filepath=os.path.dirname(os.path.realpath(__file__))
        abspath=os.path.abspath(filepath + "/data/toepassingen.xml")
        self.toepassingen_graph.parse(abspath, format="application/rdf+xml")

    def test_include(self):
        return

    def test_get_vocabulary_id(self):
        self.assertEquals('PRODUCTS', self.products_provider.get_vocabulary_id())

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
        ids = self.products_provider.expand_concept(self.u_product)
        self.assertIn(self.u_perfume, ids)

    def test_expand_collection(self):
        ids = self.products_provider.expand(self.u_stuff)
        self.assertIn(self.u_perfume, ids)

    def test_expand_unexisting(self):
        ids = self.products_provider.expand(404)
        self.assertFalse(ids)

    def test_suboordinate_arrays(self):
        graph = uri_to_graph("http://vocab.getty.edu/aat/300138225")
        concept_scheme =ConceptScheme("http://vocab.getty.edu/aat/")
        provider = RDFProvider(
            {'id': '300138225', 'conceptscheme_id': 'aat'}, graph, concept_scheme=concept_scheme)
        graph = rdf_dumper(provider)
        print graph.serialize(format='n3')

    def test_superordinate(self):
        graph = uri_to_graph("http://vocab.getty.edu/aat/300007492")
        concept_scheme =ConceptScheme("http://vocab.getty.edu/aat/")
        provider = RDFProvider(
            {'id': '300007492', 'conceptscheme_id': 'aat'}, graph, concept_scheme=concept_scheme)
        graph = rdf_dumper(provider)
        print graph.serialize(format='n3')



