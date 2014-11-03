# -*- coding: utf-8 -*-
'''
This module contains utility functions for dealing with skos providers.
'''
from __future__ import unicode_literals
import logging
import warnings
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
    conceptscheme=URIRef(provider.concept_scheme.uri)
    _add_labels(graph, provider.concept_scheme, conceptscheme)
    _add_notes(graph, provider.concept_scheme, conceptscheme)
    # Add triples using store's add method.
    for stuff in provider.get_all():
        c = provider.get_by_id(stuff['id'])
        subject = URIRef(c.uri)
        graph.add((subject, DC.identifier, Literal(stuff['id'])))
        graph.add((subject, SKOS.ConceptScheme, conceptscheme))
        _add_labels(graph, c, subject)
        _add_notes(graph, c, subject)
        if isinstance(c, Concept):
            graph.add((subject, RDF.type, SKOS.Concept))
            for b in c.broader:
                broader = provider.get_by_id(b)
                if broader:
                    graph.add((subject, SKOS.broader, URIRef(broader.uri)))
                else:
                    warnings.warn(_warning(b), UserWarning)
            for n in c.narrower:
                narrower = provider.get_by_id(n)
                if narrower:
                    graph.add((subject, SKOS.narrower, URIRef(narrower.uri)))
                else:
                    warnings.warn(_warning(n), UserWarning)
            for r in c.related:
                related = provider.get_by_id(r)
                if related:
                    graph.add((subject, SKOS.related, URIRef(related.uri)))
                else:
                    warnings.warn(_warning(r), UserWarning)
            for s in c.subordinate_arrays:
                subordinate_array = provider.get_by_id(s)
                if subordinate_array:
                    graph.add((subject, SKOS_THES.subordinateArray, URIRef(subordinate_array.uri)))
                else:
                    warnings.warn(_warning(s), UserWarning)
            for k in c.matches.keys():
                for uri in c.matches[k]:
                    graph.add((subject, URIRef(SKOS + k +'Match'), URIRef(uri)))
        elif isinstance(c, Collection):
            graph.add((subject, RDF.type, SKOS.Collection))
            for m in c.members:
                member = provider.get_by_id(m)
                if member:
                    graph.add((subject, SKOS.member, URIRef(member.uri)))
                else:
                    warnings.warn(_warning(m), UserWarning)
            for s in c.superordinates:
                superordinate = provider.get_by_id(s)
                if superordinate:
                    graph.add((subject, SKOS_THES.superOrdinate, URIRef(superordinate.uri)))
                else:
                    warnings.warn(_warning(s), UserWarning)

    return graph

def _warning(id):
    return 'id %s could not be resolved' % id


def _add_labels(graph, c, subject):
    for l in c.labels:
        predicate = URIRef(SKOS + l.type)
        lang = l.language
        if isinstance(lang, bytes):
            lang = lang.decode("UTF-8")
        graph.add((subject, predicate, Literal(l.label, lang=lang)))

def _add_notes(graph, c, subject):
    for n in c.notes:
        predicate = URIRef(SKOS + n.type)
        lang = n.language
        if isinstance(lang, bytes):
            lang = lang.decode("UTF-8")
        graph.add((subject, predicate, Literal(n.note, lang=lang)))
