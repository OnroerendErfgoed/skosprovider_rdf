import unittest
import os
from rdflib import Graph
from rdflib.namespace import RDF, SKOS
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

        def test_include(self):
            return

    def test_dump_rdf(self):
        graph_dump=utils.rdf_dumper(self.provider)
        xml=graph_dump.serialize(format='xml',encoding="latin-1").decode()
        self.assertEquals("<?xml", xml[:5])

    def test_compare_dump_rdf(self):
        graph_dump=utils.rdf_dumper(self.provider)
        self.assertEquals(type(graph_dump),Graph)
