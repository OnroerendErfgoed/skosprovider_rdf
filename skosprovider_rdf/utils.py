# -*- coding: utf-8 -*-
'''
This module contains utility functions for dealing with skos providers.
'''
from __future__ import unicode_literals
import logging
import warnings
import rdflib
import sys

log = logging.getLogger(__name__)

from rdflib import Graph, Literal
from rdflib.term import URIRef
from rdflib.namespace import RDF, SKOS, DCTERMS
SKOS_THES = rdflib.Namespace('http://purl.org/iso25964/skos-thes#')
from skosprovider.skos import (
    Concept,
    Collection
)

PY3 = sys.version_info[0] == 3

if PY3:  # pragma: no cover
    binary_type = bytes
else:  # pragma: no cover
    binary_type = str


def rdf_dumper(provider):
    '''
    Dump a provider to a format that can be passed to a
    :class:`skosprovider.providers.RDFProvider`.

    :param skosprovider.providers.VocabularyProvider provider: The provider
        that wil be turned into an :class:`rdflib.graph.Graph`.

    :rtype: :class:`rdflib.graph.Graph`
    '''
    return _rdf_dumper(provider, None)

def rdf_c_dumper(provider, c):
    '''
    Dump one concept or collection from a provider to a format that can be passed to a
    :class:`skosprovider.providers.RDFProvider`.

    :param skosprovider.providers.VocabularyProvider provider: The provider
        that wil be turned into an :class:`rdflib.graph.Graph`.

    :param String c: identifier

    :rtype: :class:`rdflib.graph.Graph`
    '''
    return _rdf_dumper(provider, [c])

def _rdf_dumper(provider, id_list=None):
    '''
    Dump a provider to a format that can be passed to a
    :class:`skosprovider.providers.RDFProvider`.

    :param skosprovider.providers.VocabularyProvider provider: The provider
        that wil be turned into an :class:`rdflib.graph.Graph`.

    :param List id_list: List of id's of the data to dump.

    :rtype: :class:`rdflib.graph.Graph`
    '''
    graph = Graph()
    graph.namespace_manager.bind("skos", SKOS)
    graph.namespace_manager.bind("dcterm", DCTERMS)
    graph.namespace_manager.bind("skos-thes", SKOS_THES)
    conceptscheme=URIRef(provider.concept_scheme.uri)
    _add_labels(graph, provider.concept_scheme, conceptscheme)
    _add_notes(graph, provider.concept_scheme, conceptscheme)
    # Add triples using store's add method.
    if not id_list:
        id_list = [x['id'] for x in provider.get_all()]
    for id in id_list:
        c = provider.get_by_id(id)
        subject = URIRef(c.uri)
        graph.add((subject, DCTERMS.identifier, Literal(c.id)))
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

def rdf_conceptscheme_dumper(provider):
    '''
    Dump all information of the conceptscheme of a provider to a format that can be passed to a
    :class:`skosprovider.providers.RDFProvider`.

    :param skosprovider.providers.VocabularyProvider provider: The provider
        that wil be turned into an :class:`rdflib.graph.Graph`.

    :rtype: :class:`rdflib.graph.Graph`
    '''
    graph = Graph()
    graph.namespace_manager.bind("skos", SKOS)
    graph.namespace_manager.bind("dcterm", DCTERMS)
    graph.namespace_manager.bind("skos-thes", SKOS_THES)
    conceptscheme=URIRef(provider.concept_scheme.uri)
    graph.add((conceptscheme, DCTERMS.identifier, Literal(provider.metadata['id'])))
    _add_labels(graph, provider.concept_scheme, conceptscheme)
    _add_notes(graph, provider.concept_scheme, conceptscheme)
    graph.add((conceptscheme, RDF.type, SKOS.ConceptScheme))
    for c in provider.get_top_concepts():
        graph.add((conceptscheme, SKOS.hasTopConcept, URIRef(c['uri'])))

    return graph

def _warning(id):
    return 'id %s could not be resolved' % id


def _add_labels(graph, c, subject):
    for l in c.labels:
        predicate = URIRef(SKOS + l.type)
        lang = extract_language(l.language)
        graph.add((subject, predicate, Literal(l.label, lang=lang)))


def _add_notes(graph, c, subject):
    for n in c.notes:
        predicate = URIRef(SKOS + n.type)
        lang = extract_language(n.language)
        graph.add((subject, predicate, Literal(n.note, lang=lang)))


def extract_language(lang):
    if lang is None:
        lang = 'und'  # return undefined code when no language
    else:
        lang = text_(lang, encoding="UTF-8")
    return lang


def text_(s, encoding='latin-1', errors='strict'):
    """ If ``s`` is an instance of ``binary_type``, return
    ``s.decode(encoding, errors)``, otherwise return ``s``"""
    if isinstance(s, binary_type):
        return s.decode(encoding, errors)
    return s
