# -*- coding: utf-8 -*-

'''
This module contains an RDFProvider, an implementation of the 
:class:`skosprovider.providers.VocabularyProvider` interface that uses a 
:class:`rdflib.graph.Graph` as input.
'''

import logging
import rdflib
from rdflib.term import Literal, URIRef
from skosprovider_rdf.utils import text_, _df_writexml

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

from skosprovider.providers import MemoryProvider
from skosprovider.uri import (
    DefaultConceptSchemeUrnGenerator
)
from skosprovider.skos import (
    Concept,
    Collection,
    ConceptScheme,
    Label,
    Note,
    Source
)

from rdflib.namespace import RDF, SKOS, DC, DCTERMS
SKOS_THES = rdflib.Namespace('http://purl.org/iso25964/skos-thes#')

from language_tags import tags

from xml.dom.minidom import DocumentFragment
DocumentFragment.writexml = _df_writexml


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
        for sub in self.graph.subjects(RDF.type, SKOS.ConceptScheme):
            uri = self.to_text(sub)
            cs = ConceptScheme(
                uri=uri,
                labels = self._create_from_subject_typelist(sub, Label.valid_types),
                notes = self._create_from_subject_typelist(sub, Note.valid_types),
                sources = self._create_sources(sub),
                languages = self._create_languages(sub)
            )
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
            matches = {}
            for k in Concept.matchtypes:
                matches[k] = self._create_from_subject_predicate(sub, URIRef(SKOS + k +'Match'))
            con = Concept(
                id = self._get_id_for_subject(sub, uri), 
                uri=uri,
                concept_scheme = self.concept_scheme,
                labels = self._create_from_subject_typelist(sub, Label.valid_types),
                notes = self._create_from_subject_typelist(sub, Note.valid_types),
                sources = self._create_sources(sub),
                broader = self._create_from_subject_predicate(sub, SKOS.broader),
                narrower = self._create_from_subject_predicate(sub, SKOS.narrower),
                related = self._create_from_subject_predicate(sub, SKOS.related),
                member_of = [],
                subordinate_arrays = self._create_from_subject_predicate(sub, SKOS_THES.subordinateArray),
                matches = matches
            )
            clist.append(con)

        for sub, pred, obj in self.graph.triples((None, RDF.type, SKOS.Collection)):
            uri = self.to_text(sub)
            col = Collection(
                id=self._get_id_for_subject(sub, uri), 
                uri=uri,
                concept_scheme = self.concept_scheme,
                labels = self._create_from_subject_typelist(sub, Label.valid_types),
                notes = self._create_from_subject_typelist(sub, (Note.valid_types)),
                sources = self._create_sources(sub),
                members = self._create_from_subject_predicate(sub, SKOS.member),
                member_of = [],
                superordinates = self._create_from_subject_predicate(sub, SKOS_THES.superOrdinate)
            )
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
        if literal.datatype is None:
            return Note(self.to_text(literal), type, self._get_language_from_literal(literal), None)
        elif literal.datatype == RDF.HTML:
            df = literal.value.cloneNode(True)
            if df.firstChild and df.firstChild.attributes and 'xml:lang' in df.firstChild.attributes.keys():
                lang = self._scrub_language(df.firstChild.attributes.get('xml:lang').value)
                del df.firstChild.attributes['xml:lang']
            else:
                lang = 'und'
            return Note(self.to_text(df.toxml()), type, lang, 'HTML')

    def _create_sources(self, subject):
        '''
        Create the sources for this subject.

        :param subject: Subject to get the sources for.
        :returns: A :class:`list` of :class:`skosprovider.skos.Source` objects.
        '''
        ret = []
        for s, p, o in self.graph.triples((subject, DCTERMS.source, None)):
            for si, pi, oi in self.graph.triples((o, DCTERMS.bibliographicCitation, None)):
                ret.append(Source(self.to_text(oi)))
        return ret

    def _create_languages(self, subject):
        '''
        Create the languages for this subject.

        :param subject: Subject to get the sources for.
        :returns: A :class:`list` of IANA language tags.
        '''
        ret = set()
        for s, p, o in self.graph.triples((subject, DCTERMS.language, None)):
            ret.add(self.to_text(self._scrub_language(o)))
        for s, p, o in self.graph.triples((subject, DC.language, None)):
            ret.add(self.to_text(self._scrub_language(o)))
        return ret

    def _scrub_language(self, language):
        if tags.check(language):
            return language
        else:
            log.warn('Encountered an invalid language %s. Falling back to "und".' % language)
            return 'und'

    def _get_language_from_literal(self, data):
        if not isinstance(data, Literal):
            return None
        if data.language is None:
            return None
        return self.to_text(self._scrub_language(data.language))

    def to_text(self, data):
        """
        data of binary type or literal type that needs to be converted to text.
        :param data
        :return: text representation of the data
        """
        return text_(data.encode('utf-8'), 'utf-8')
