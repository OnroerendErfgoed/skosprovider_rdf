0.3.1 (??-??-2015)
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
