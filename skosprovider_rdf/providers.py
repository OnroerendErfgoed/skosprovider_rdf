# -*- coding: utf-8 -*-

'''
This module contains an RDFProvider, an implementation of the 
:class:`skosprovider.providers.VocabularyProvider` interface that uses a 
:class:`rdflib.graph.Graph` as input.
'''

import logging
import rdflib
from rdflib.term import Literal
from skosprovider_rdf.utils import uri_to_graph, uri_to_id

log = logging.getLogger(__name__)

from skosprovider.providers import MemoryProvider
from skosprovider.skos import (
    Concept,
    Collection,
    Label,
    Note
)

from rdflib.namespace import RDF, SKOS, DC
SKOS_THES = rdflib.Namespace('http://purl.org/iso25964/skos-thes#')


class RDFProvider(MemoryProvider):
    '''
    A simple vocabulary provider that use an :class:`rdflib.graph.Graph`
    as input. The provider expects a RDF graph with elements that represent
    the SKOS concepts and collections.

    Please be aware that this provider needs to load the entire graph in memory.
    '''

    def __init__(self, metadata, graph, **kwargs):
        super(RDFProvider, self).__init__(metadata, [], **kwargs)
        self.conceptscheme_id = metadata.get(
        'conceptscheme_id', metadata.get('id')
        )
        self.graph = graph
        self.list = self._from_graph()


    def _from_graph(self):
        clist = []
        for sub, pred, obj in self.graph.triples((None, RDF.type, SKOS.Concept)):
            con = None
            uri = str(sub)
            con = Concept(self._get_id_for_subject(sub, uri), uri=uri)
            con.broader = self._create_from_subject_predicate(sub, SKOS.broader)
            con.narrower = self._create_from_subject_predicate(sub, SKOS.narrower)
            con.related = self._create_from_subject_predicate(sub, SKOS.related)
            con.notes = self._create_from_subject_typelist(sub, Note.valid_types)
            con.labels = self._create_from_subject_typelist(sub, Label.valid_types)
            con.subordinate_arrays = self._get_array_members(self._create_from_subject_predicate(sub, SKOS_THES.subordinateArray))
            con.concept_scheme = self.concept_scheme
            clist.append(con)

        for sub, pred, obj in self.graph.triples((None, RDF.type, SKOS.Collection)):
            col = None
            uri = str(sub)
            col = Collection(self._get_id_for_subject(sub, uri), uri=uri)
            col.members = self._create_from_subject_predicate(sub, SKOS.member)
            col.labels = self._create_from_subject_typelist(sub, Label.valid_types)
            col.notes = self._create_from_subject_typelist(sub, (Note.valid_types))
            col.superordinates = self._create_from_subject_predicate(sub, SKOS_THES.superOrdinate)
            col.concept_scheme = self.concept_scheme
            clist.append(col)
        self._fill_member_of(clist)

        return clist

    def _fill_member_of(self, clist):
        collections = None
        collections = list(set([c for c in clist if isinstance(c, Collection)]))
        for col in collections:
            for c in clist:
                 if c.id in col.members:
                    c.member_of.append(col.id)
                    break

    def _create_from_subject_typelist(self,subject,typelist):
        list = []
        for p in typelist:
            term=SKOS.term(p)
            list.extend(self._create_from_subject_predicate(subject,term))
        return list

    def _get_id_for_subject(self, subject, uri):
        if (subject, DC.identifier, None) in self.graph:
            return self.graph.value(subject=subject, predicate=DC.identifier, any=False)
        else:
            return uri

    def _create_from_subject_predicate(self, subject, predicate):
        list = []
        for s, p, o in self.graph.triples((subject, predicate, None)):
            type = predicate.split('#')[-1]
            if Label.is_valid_type(type):
                o = self._create_label(o, type)
            elif Note.is_valid_type(type):
                o = self._create_note(o, type)
            else:
                o = unicode(o)
            list.append(o)
        return list

    def _create_label(self, literal, type):
        if not Label.is_valid_type(type):
            raise ValueError(
                'Type of Label is not valid.'
            )
        return Label(unicode(literal), type, self._get_language_from_literal(literal))

    def _create_note(self, literal, type):
        if not Note.is_valid_type(type):
            raise ValueError(
                'Type of Note is not valid.'
            )
        return Note(unicode(literal), type, self._get_language_from_literal(literal))

    def _get_language_from_literal(self, data):
        if not isinstance(data, Literal):
            return None
        if data.language is None:
            return None
        return data.language.encode("utf-8")

    def _get_array_members(self, arr):
        member_list = []
        if len(arr) > 0:
            graph = uri_to_graph(arr[0])
            for s, p, o in graph.triples((None, SKOS.member, None)):
                o = uri_to_id(o)
                if o:
                    member_list.append(unicode(o))
        return member_list


