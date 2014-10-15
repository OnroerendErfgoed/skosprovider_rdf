# -*- coding: utf-8 -*-
'''
This module contains utility functions for dealing with skos providers.
'''
from __future__ import unicode_literals
import logging
import rdflib

log = logging.getLogger(__name__)

from rdflib import Graph, Literal
from rdflib.term import URIRef
from rdflib.namespace import RDF, SKOS, DC
SKOS_THES = rdflib.Namespace('http://purl.org/iso25964/skos-thes#')
from skosprovider.skos import (
    Concept,
    Collection
)


def rdf_dumper(provider):
    '''
    Dump a provider to a format that can be passed to a
    :class:`skosprovider.providers.RDFProvider`.

    :param skosprovider.providers.VocabularyProvider provider: The provider
        that wil be turned into an :class:`rdflib.graph.Graph`.

    :rtype: A :class:`rdflib.rdflib.Graph`.
    '''
    graph = Graph()
    graph.namespace_manager.bind("skos", SKOS)
    graph.namespace_manager.bind("dc", DC)
    graph.namespace_manager.bind("skos-thes", SKOS_THES)
    # Add triples using store's add method.
    for stuff in provider.get_all():
        c = provider.get_by_id(stuff['id'])
        subject = URIRef(c.uri)
        graph.add((subject, DC.identifier, Literal(stuff['id'])))
        graph.add((subject, SKOS.ConceptScheme, URIRef(provider.concept_scheme.uri)))
        for l in c.labels:
            predicate = URIRef(SKOS + l.type)
            lang = l.language
            if isinstance(lang, bytes):
                lang = lang.decode("UTF-8")
            graph.add((subject, predicate, Literal(l.label, lang=lang)))
        for n in c.notes:
            predicate = URIRef(SKOS + n.type)
            lang = n.language
            if isinstance(lang, bytes):
                lang = lang.decode("UTF-8")
            graph.add((subject, predicate, Literal(n.note, lang=lang)))
        if isinstance(c, Concept):
            graph.add((subject, RDF.type, SKOS.Concept))
            for b in c.broader:
                broader = provider.get_by_id(b)
                object = URIRef(broader.uri) if broader else URIRef(b)
                graph.add((subject, SKOS.broader, object))
            for n in c.narrower:
                narrower = provider.get_by_id(n)
                object = URIRef(narrower.uri) if narrower else URIRef(n)
                graph.add((subject, SKOS.narrower, object))
            for r in c.related:
                related = provider.get_by_id(r)
                object = URIRef(related.uri) if related else URIRef(r)
                graph.add((subject, SKOS.related, object))
            #question how to solve problem of subordinateArray/list
            for s in c.subordinate_arrays:
                member = provider.get_by_id(s)
                object = URIRef(member.uri) if member else URIRef(s)
                graph.add((subject, SKOS.member, object))
        elif isinstance(c, Collection):
            graph.add((subject, RDF.type, SKOS.Collection))
            for m in c.members:
                member = provider.get_by_id(m)
                object = URIRef(member.uri) if member else URIRef(m)
                graph.add((subject, SKOS.member, object))
            for s in c.superordinates:
                superordinate = provider.get_by_id(s)
                object = URIRef(superordinate.uri) if superordinate else URIRef(s)
                graph.add((subject, SKOS_THES.superOrdinate, object))

    return graph

def uri_to_id(uri):
    #question: not every uri can be converted to a graph, how can we get the id with a generalised method
    graph = uri_to_graph(uri)
    for s, p, o in graph.triples((uri, DC.identifier, None)):
        return o
    return False

def uri_to_graph(uri):
    graph = rdflib.Graph()
    try:
        graph.parse(uri)
        return graph
    # for python2.7 this is urllib2.HTTPError
    # for python3 this is urllib.error.HTTPError
    except Exception as err:
        if hasattr(err, 'code'):
            if err.code == 404:
                return False
        else:
            raise
