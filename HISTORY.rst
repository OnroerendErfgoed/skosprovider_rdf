0.8.0 (08-06-2020)
------------------

- Update to RDFlib 0.5.0 (#74)


0.7.0 (12-02-2020)
------------------

- Compatibile with `SkosProvider 0.7.0 <http://skosprovider.readthedocs.io/en/0.7.0/>`_.
- Make it possible to read an RDF file containing more than one conceptscheme. (#35)
- Drop support for Python 3.3, 3.4 and 3.5. This is the last version that will
  support Python 2. (#63)

0.6.0 (16-07-2017)
------------------

- Compatibile with `SkosProvider 0.6.1 <http://skosprovider.readthedocs.io/en/0.6.1/>`_.
- Add information about the void.Dataset when dumping to RDF.

0.5.0 (11-08-2016)
------------------

- Compatibile with `SkosProvider 0.6.0 <http://skosprovider.readthedocs.io/en/0.6.0/>`_.
- Add official python 3.5 compatibility.
- Add support for sources when dumping to RDF and reading from RDF. (#17)
- Add support for languages to conceptschemes when dumping to and reading from
  RDF. (#16)
- Add support for HTML in SKOS notes and sources. (#15, #20)

0.4.1 (17-07-2015)
------------------

- RDF dump: Add the top concepts and the conceptscheme identifier in the full RDF dump
  (equal to the RDF conceptscheme dump).
- RDF provider: literal and binary type to text when parsing the graph to a list.

0.4.0 (03-03-2015)
------------------

- Allow dumping a single conceptscheme to RDF. This does not dump the entire
  conceptscheme with all it's concepts or collections, just information on the
  conceptscheme itself and it's top concepts.
- Allow dumping a single concept or collection to RDF, and not just an entire
  conceptscheme with all concepts or collections.
- Add skos:inScheme information to RDF dumps.
- Better handling of dc(t):identifier. When reading an RDF file both 
  dcterms:identifier and dc:identifier are considered when analysing the 
  identifier. During dumping, we also dump to dcterms:identifier.

0.3.0 (19-12-2014)
------------------

- Compatibile with `SkosProvider 0.5.0 <http://skosprovider.readthedocs.org/en/0.5.0>`_.
- Dumping to an RDF file now also dumps information on the Conceptscheme.
- Dumping to an RDF file now also adds notes to a Collection, not just to a
  Concept.
- Now handles subordinate_array and superordinate concept.

0.2.0 (14-10-2014)
------------------

- Add support for Dublin Core identifier (#5)

0.1.3 (02-09-2014)
------------------

- Fix a namespace error for SKOS Notes. (#2)

0.1.2 (31-07-2014)
------------------

- Documentation fixes and cleanup
- Removed RDFlib artefacts from output.

0.1.1 (20-05-2014)
------------------

- Bugfixing
- encoding/decoding problems
- casting rdf subjects and objects to rdflib URI's
- Added tests

0.1.0
-----

- Initial version
