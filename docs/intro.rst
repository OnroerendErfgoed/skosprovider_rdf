.. _introduction:

Introduction
============

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
