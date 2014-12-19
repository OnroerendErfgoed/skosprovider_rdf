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
    
    $ pip install skosprovider_ref

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

It also provides a utility function to dump any implementation 
of :class:`skosprovider.providers.VocabularyProvider` to a 
:class:`rdflib.graph.Graph`. Again, since the provider only deals with the 
:class:`~rdflib.graph.Graph` object, it's possible to serialise a VocabularyProvider
to whatever RDF serialisations :mod:`rdflib` allows.

.. literalinclude:: /../examples/dump.py
    :language: python
