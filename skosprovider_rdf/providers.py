# -*- coding: utf-8 -*-

import logging

log = logging.getLogger(__name__)

from skosprovider.providers import MemoryProvider

from skosprovider.skos import (
    Concept,
    Collection,
    Label,
    Note
)

from rdflib.namespace import RDF, SKOS


class RDFProvider(MemoryProvider):
    '''
    A :class:`skosprovider_rdf.providers.RDFProvider` simple vocab provider that use a RDFLib graph as input.
    The provider expects a RDF graph with elements that represent
    the concepts.
    '''

    def __init__(self, metadata, graph, **kwargs):
        super(RDFProvider, self).__init__(metadata, [], **kwargs)
        self.conceptscheme_id = metadata.get(
            'conceptscheme_id', metadata.get('id')
        )
        self.graph = graph
        self.list = self._from_graph()

    def _from_graph(self):
        list = []
        for sub, pred, obj in self.graph.triples((None, RDF.type, SKOS.Concept)):
            con = Concept(sub)
            con.uri = sub
            con.broader = self._create_from_subject_predicate(sub, SKOS.broader)
            con.narrower = self._create_from_subject_predicate(sub, SKOS.narrower)
            con.related = self._create_from_subject_predicate(sub, SKOS.related)
            ##TODO implement all other note-types of SKOS: historyNote,example,...
            con.notes = self._create_from_subject_predicate(sub, SKOS.note)
            con.labels = self._create_from_subject_predicate(sub, SKOS.prefLabel) + \
                         self._create_from_subject_predicate(sub, SKOS.altLabel) + \
                         self._create_from_subject_predicate(sub, SKOS.hiddenLabel)
            list.append(con)

        for sub, pred, obj in self.graph.triples((None, RDF.type, SKOS.Collection)):
            col = Collection(sub)
            col.uri = sub
            col.members = self._create_from_subject_predicate(sub, SKOS.member)
            col.labels = self._create_from_subject_predicate(sub, SKOS.prefLabel) + \
                         self._create_from_subject_predicate(sub, SKOS.altLabel) + \
                         self._create_from_subject_predicate(sub, SKOS.hiddenLabel)
            list.append(col)

        return list

    def _create_from_subject_predicate(self, subject, predicate):
        list = []
        for s, p, o in self.graph.triples((subject, predicate, None)):
            type = predicate.split('#')[-1]
            if Label.is_valid_type(type):
                o = self._create_label(o, type)
            if Note.is_valid_type(type):
                o = self._create_note(o, type)
            list.append(o)
        return list

    def _create_label(self, literal, type):
        if not Label.is_valid_type(type):
            raise ValueError(
                'Type of Label is not valid.'
            )
        return Label(literal, type, self._get_language_from_literal(literal))

    def _create_note(self, literal, type):
        if not Note.is_valid_type(type):
            raise ValueError(
                'Type of Note is not valid.'
            )

        return Note(literal, type, self._get_language_from_literal(literal))

    def _get_language_from_literal(self, data):
        if data.language is None:
            return None
        return data.language.encode("ascii")
