# -*- coding: utf-8 -*-
'''
This module contains utility functions for dealing with skos providers.
'''
from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

from rdflib import Graph, Literal
from rdflib.term import URIRef
from rdflib.namespace import RDF, SKOS
from skosprovider.skos import (
    Concept,
    Collection
)


def rdf_dumper(provider):
    '''
    Dump a provider to a format that can be passed to a
    :class:`skosprovider.providers.RDFProvider`.

    :param skosprovider.providers.VocabularyProvider provider: The provider
        that wil be turned into a `RDF graph`.
    :rtype: A :class:`rdflib.Graph`.
    '''
    graph = Graph()
    graph.namespace_manager.bind("skos", SKOS)
    # Add triples using store's add method.
    for stuff in provider.get_all():
        c = provider.get_by_id(stuff['id'])
        subject = URIRef(c.uri)

        for l in c.labels:
            predicate = URIRef(SKOS + l.type)
            lang = l.language
            if lang:
                lang = lang.decode("UTF-8")
            graph.add((subject, predicate, Literal(l.label, lang=lang)))
        if isinstance(c, Concept):
            graph.add((subject, RDF.type, SKOS.Concept))
            for b in c.broader:
                broader = provider.get_by_id(b)
                object = URIRef(broader.uri)
                graph.add((subject, SKOS.broader, object))
            for n in c.narrower:
                narrower = provider.get_by_id(n)
                object = URIRef(narrower.uri)
                graph.add((subject, SKOS.narrower, object))
            for r in c.related:
                related = provider.get_by_id(r)
                object = URIRef(related.uri)
                graph.add((subject, SKOS.related, object))
            for n in c.notes:
                predicate = URIRef(SKOS + "#" + n.type)
                lang = n.language
                if lang:
                    lang = lang.decode("UTF-8")
                graph.add((subject, predicate, Literal(n.note, lang=lang)))
        elif isinstance(c, Collection):
            graph.add((subject, RDF.type, SKOS.Collection))
            for m in c.members:
                member = provider.get_by_id(m)
                object = URIRef(member.uri)
                graph.add((subject, SKOS.member, object))

    return graph
