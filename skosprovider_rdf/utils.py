# -*- coding: utf-8 -*-
'''
This module contains utility functions for dealing with skos providers.
'''
from __future__ import unicode_literals
import logging
import warnings
import sys

log = logging.getLogger(__name__)

from rdflib import Graph, Literal, Namespace
from rdflib.term import URIRef, BNode
from rdflib.namespace import RDF, SKOS, DCTERMS, VOID
SKOS_THES = Namespace('http://purl.org/iso25964/skos-thes#')
from skosprovider.skos import (
    Concept,
    Collection
)

from xml.dom.minidom import Node, Element
import html5lib

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
    graph.namespace_manager.bind("dcterms", DCTERMS)
    graph.namespace_manager.bind("skos-thes", SKOS_THES)
    graph.namespace_manager.bind("void", VOID)
    conceptscheme = URIRef(provider.concept_scheme.uri)
    _add_in_dataset(graph, conceptscheme, provider)
    graph.add((conceptscheme, RDF.type, SKOS.ConceptScheme))
    graph.add((conceptscheme, DCTERMS.identifier, Literal(provider.metadata['id'])))
    _add_labels(graph, provider.concept_scheme, conceptscheme)
    _add_notes(graph, provider.concept_scheme, conceptscheme)
    _add_sources(graph, provider.concept_scheme, conceptscheme)
    _add_languages(graph, provider.concept_scheme, conceptscheme)
    # Add triples using store's add method.
    if not id_list:
        id_list = [x['id'] for x in provider.get_all()]
        for c in provider.get_top_concepts():
            graph.add((conceptscheme, SKOS.hasTopConcept, URIRef(c['uri'])))
    for id in id_list:
        _add_c(graph, provider, id)

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
    graph.namespace_manager.bind("dcterms", DCTERMS)
    graph.namespace_manager.bind("skos-thes", SKOS_THES)
    graph.namespace_manager.bind("void", VOID)
    conceptscheme = URIRef(provider.concept_scheme.uri)
    _add_in_dataset(graph, conceptscheme, provider)
    graph.add((conceptscheme, RDF.type, SKOS.ConceptScheme))
    graph.add((conceptscheme, DCTERMS.identifier, Literal(provider.metadata['id'])))
    _add_labels(graph, provider.concept_scheme, conceptscheme)
    _add_notes(graph, provider.concept_scheme, conceptscheme)
    _add_sources(graph, provider.concept_scheme, conceptscheme)
    _add_languages(graph, provider.concept_scheme, conceptscheme)
    for c in provider.get_top_concepts():
        graph.add((conceptscheme, SKOS.hasTopConcept, URIRef(c['uri'])))

    return graph


def _warning(id):
    return 'id %s could not be resolved' % id


def _add_in_dataset(graph, subject, provider):
    '''
    Checks if the provider says something about a dataset and if so adds 
    void.inDataset statements.

    :param rdflib.graph.Graph graph: The graph to add statements to.
    :param rdflib.term.URIRef subject: The subject to add an inDataset statement to.
    :param skosprovider.providers.VocabularyProvider provider:
    '''

    duri = provider.get_metadata().get('dataset', {}).get('uri', None)
    if duri:
        graph.add((subject, VOID.inDataset, URIRef(duri)))


def _add_c(graph, provider, id):
    '''
    Adds a concept or collection to the graph.

    :param rdflib.graph.Graph graph: The graph to add statements to.
    :param skosprovider.providers.VocabularyProvider provider: Provider
    :param c: The id of a concept or collection.
    '''

    c = provider.get_by_id(id)
    subject = URIRef(c.uri)
    _add_in_dataset(graph, subject, provider)
    graph.add((subject, DCTERMS.identifier, Literal(c.id)))
    conceptscheme = URIRef(provider.concept_scheme.uri)
    graph.add((subject, SKOS.inScheme, conceptscheme))
    _add_labels(graph, c, subject)
    _add_notes(graph, c, subject)
    _add_sources(graph, c, subject)
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


def _add_labels(graph, c, subject):
    for l in c.labels:
        predicate = URIRef(SKOS + l.type)
        lang = extract_language(l.language)
        graph.add((subject, predicate, Literal(l.label, lang=lang)))


def _add_notes(graph, c, subject):
    for n in c.notes:
        predicate = URIRef(SKOS + n.type)
        lang = extract_language(n.language)
        if n.markup is None:
            graph.add((subject, predicate, Literal(n.note, lang=lang)))
        else:
            html = _add_lang_to_html(n.note, lang)
            graph.add((subject, predicate, Literal(html, datatype=RDF.HTML)))

def _add_lang_to_html(htmltext, lang):
    '''
    Take a piece of HTML and add an xml:lang attribute to it.
    '''
    if lang == 'und':
        return htmltext
    parser = html5lib.HTMLParser(
        tree=html5lib.treebuilders.getTreeBuilder("dom")
    )
    html = parser.parseFragment(htmltext)
    html.normalize()
    if len(html.childNodes) == 0:
        return '<div xml:lang="%s"></div>' % lang
    elif len(html.childNodes) == 1:
        node = html.firstChild
        if node.nodeType == Node.TEXT_NODE:
            div = Element('div')
            div.ownerDocument = html
            div.setAttribute('xml:lang', lang)
            div.childNodes = [node]
            html.childNodes = [div]
        else:
            node.setAttribute('xml:lang', lang)
    else:
        #add a single encompassing div
        div = Element('div')
        div.ownerDocument = html
        div.setAttribute('xml:lang', lang)
        div.childNodes = html.childNodes
        html.childNodes = [div]
    return html.toxml()

def _add_sources(graph, c, subject):
    '''
    Add sources to the RDF graph.

    :param rdflib.graph.Graph graph: An RDF Graph.
    :param c: A :class:`skosprovider.skos.ConceptScheme`, 
        :class:`skosprovider.skos.Concept` or :class:`skosprovider.skos.Collection`
    :param subject: The RDF subject to add the sources to.
    '''
    for s in c.sources:
        source = BNode()
        graph.add((source, RDF.type, DCTERMS.BibliographicResource))
        if s.markup is None:
            graph.add((source, DCTERMS.bibliographicCitation, Literal(s.citation)))
        else:
            graph.add((source, DCTERMS.bibliographicCitation, Literal(s.citation, datatype=RDF.HTML)))
        graph.add((subject, DCTERMS.source, source))

def _add_languages(graph, c, subject):
    '''
    Add languages to the RDF graph.

    :param rdflib.graph.Graph graph: An RDF Graph.
    :param c: A :class:`skosprovider.skos.ConceptScheme`.
    :param subject: The RDF subject to add the sources to.
    '''
    for l in c.languages:
        lang = extract_language(l)
        graph.add((subject, DCTERMS.language, Literal(l)))

def extract_language(lang):
    '''
    Turn a language in our domain model into a IANA tag.
    '''
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

def _df_writexml(self, writer, indent="", addindent="", newl=""):
    '''
    Monkeypatch method for unexisting `writexml` in
    :class:`xml.dom.minidom.DocumentFragment`.
    '''
    # indent = current indentation
    # addindent = indentation to add to higher levels
    # newl = newline string
    if self.childNodes:
        if (len(self.childNodes) == 1 and
            self.childNodes[0].nodeType == Node.TEXT_NODE):
            self.childNodes[0].writexml(writer, '', '', '')
        else:
            for node in self.childNodes:
                node.writexml(writer, indent+addindent, addindent, newl)

from xml.dom.minidom import DocumentFragment
DocumentFragment.writexml = _df_writexml
