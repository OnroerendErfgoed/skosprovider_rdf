# -*- coding: utf-8 -*-

'''
This module contains an RDFProvider, an implementation of the 
:class:`skosprovider.providers.VocabularyProvider` interface that uses a 
:class:`rdflib.graph.Graph` as input.
'''

import logging
import rdflib
from rdflib.term import Literal, URIRef
from skosprovider_rdf.utils import text_

log = logging.getLogger(__name__)

from skosprovider.providers import MemoryProvider
from skosprovider.uri import (
    DefaultConceptSchemeUrnGenerator
)
from skosprovider.skos import (
    Concept,
    Collection,
    ConceptScheme,
    Label,
    Note
)

from rdflib.namespace import RDF, SKOS, DC, DCTERMS
SKOS_THES = rdflib.Namespace('http://purl.org/iso25964/skos-thes#')


class RDFProvider(MemoryProvider):
    '''
    A simple vocabulary provider that use an :class:`rdflib.graph.Graph`
    as input. The provider expects a RDF graph with elements that represent
    the SKOS concepts and collections.

    Please be aware that this provider needs to load the entire graph in memory.
    '''

    def __init__(self, metadata, graph, **kwargs):
        self.graph = graph
        if not 'concept_scheme' in kwargs:
            kwargs['concept_scheme'] = self._cs_from_graph(metadata)
        super(RDFProvider, self).__init__(metadata, [], **kwargs)
        self.list = self._from_graph()

    def _cs_from_graph(self, metadata):
        cslist = []
        for sub, pred, obj in self.graph.triples((None, RDF.type, SKOS.ConceptScheme)):
            uri = self.to_text(sub)
            cs = ConceptScheme(uri=uri)
            cs.labels = self._create_from_subject_typelist(sub, Label.valid_types)
            cs.notes = self._create_from_subject_typelist(sub, Note.valid_types)
            cslist.append(cs)
        if len(cslist) == 0:
            return ConceptScheme(
                uri=DefaultConceptSchemeUrnGenerator().generate(
                    id=metadata.get('id')
                )
            )
        elif len(cslist) == 1:
            return cslist[0]
        else:
            raise RuntimeError(
                'This RDF file contains more than one ConceptScheme.'
            )

    def _from_graph(self):
        clist = []
        for sub, pred, obj in self.graph.triples((None, RDF.type, SKOS.Concept)):
            uri = self.to_text(sub)
            con = Concept(self._get_id_for_subject(sub, uri), uri=uri)
            con.broader = self._create_from_subject_predicate(sub, SKOS.broader)
            con.narrower = self._create_from_subject_predicate(sub, SKOS.narrower)
            con.related = self._create_from_subject_predicate(sub, SKOS.related)
            con.notes = self._create_from_subject_typelist(sub, Note.valid_types)
            con.labels = self._create_from_subject_typelist(sub, Label.valid_types)
            con.subordinate_arrays = self._create_from_subject_predicate(sub, SKOS_THES.subordinateArray)
            for k in con.matches.keys():
                con.matches[k] = self._create_from_subject_predicate(sub, URIRef(SKOS + k +'Match'))
            self._create_from_subject_predicate(sub, SKOS_THES.subordinateArray)
            con.concept_scheme = self.concept_scheme
            con.member_of = []
            clist.append(con)

        for sub, pred, obj in self.graph.triples((None, RDF.type, SKOS.Collection)):
            uri = self.to_text(sub)
            col = Collection(self._get_id_for_subject(sub, uri), uri=uri)
            col.members = self._create_from_subject_predicate(sub, SKOS.member)
            col.labels = self._create_from_subject_typelist(sub, Label.valid_types)
            col.notes = self._create_from_subject_typelist(sub, (Note.valid_types))
            col.superordinates = self._create_from_subject_predicate(sub, SKOS_THES.superOrdinate)
            col.concept_scheme = self.concept_scheme
            col.member_of = []
            clist.append(col)
        self._fill_member_of(clist)
        return clist

    def _fill_member_of(self, clist):
        collections = list(set([c for c in clist if isinstance(c, Collection)]))
        for col in collections:
            for c in clist:
                if c.id in col.members:
                    c.member_of.append(col.id)
        return

    def _create_from_subject_typelist(self,subject,typelist):
        list = []
        for p in typelist:
            term=SKOS.term(p)
            list.extend(self._create_from_subject_predicate(subject,term))
        return list

    def _get_id_for_subject(self, subject, uri):
        for stmt in self.graph:
            print(stmt)
        if (subject, DCTERMS.identifier, None) in self.graph:
            return self.to_text(self.graph.value(subject=subject, predicate=DCTERMS.identifier, any=False))
        elif (subject, DC.identifier, None) in self.graph:
            return self.to_text(self.graph.value(subject=subject, predicate=DC.identifier, any=False))
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
                o = self._get_id_for_subject(o, self.to_text(o))
            list.append(o)
        return list

    def _create_label(self, literal, type):
        if not Label.is_valid_type(type):
            raise ValueError(
                'Type of Label is not valid.'
            )
        return Label(self.to_text(literal), type, self._get_language_from_literal(literal))

    def _create_note(self, literal, type):
        if not Note.is_valid_type(type):
            raise ValueError(
                'Type of Note is not valid.'
            )
        return Note(self.to_text(literal), type, self._get_language_from_literal(literal))

    def _get_language_from_literal(self, data):
        if not isinstance(data, Literal):
            return None
        if data.language is None:
            return None
        return self.to_text(data.language)

    def to_text(self, data):
        """
        data of binary type or literal type that needs to be converted to text.
        :param data
        :return: text representation of the data
        """
        return text_(data.encode('utf-8'), 'utf-8')
