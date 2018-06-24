.. _introduction:

Introduction
============

Installation
------------

To be able to use this library you need to have a modern version of Python 
installed. Currently we're supporting versions 2.7, 3.3 and 3.4 of Python.

This easiest way to install this library is through :command:`pip` or 
:command:`easy install`:

.. code-block:: bash    
    
    $ pip install skosprovider_rdf

This will download and install :mod:`skosprovider_rdf` and a few libraries it 
depends on.

Usage
-----

This library offers an implementation of the 
:class:`skosprovider.providers.VocabularyProvider` interface that uses an 
:class:`rdflib.graph.Graph` as input. This provider can be used to add a :term:`SKOS` 
vocabulary contained in an :term:`RDF` file to your application. The provider
itself does not read the :term:`SKOS` file, but expects to be passed a
:class:`~rdflib.graph.Graph`. So any type of RDF serialisation that can be read by
:mod:`rdflib`, can be used with this provider.

.. literalinclude:: /../examples/load_skos.py
    :language: python

Out of the box :mod:`skosprovider_rdf` assumes your :term:`RDF` file contains 
exactly one conceptscheme. If no conceptscheme is found in the file and you did
not pass one to the provider through the `concept_scheme` parameter, a new
conceptscheme is automatically created. If more than one conceptscheme is
present in the file, you can again specify the conceptscheme through the
`concept_scheme` parameter (passing a :class:`skosprovider.skos.ConceptScheme`)
or you can pass the uri of one of the conceptschemes present in the
`concept_scheme_uri` parameter.

.. literalinclude:: /../examples/load_specific_scheme.py
    :language: python

It also provides a utility function to dump any implementation 
of :class:`skosprovider.providers.VocabularyProvider` to a 
:class:`rdflib.graph.Graph`. Again, since the provider only deals with the 
:class:`~rdflib.graph.Graph` object, it's possible to serialise a VocabularyProvider
to whatever RDF serialisations :mod:`rdflib` allows.

.. literalinclude:: /../examples/dump.py
    :language: python
