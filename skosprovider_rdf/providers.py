# -*- coding: utf-8 -*-

import logging

log = logging.getLogger(__name__)

from skosprovider.providers import VocabularyProvider

from skosprovider.skos import (
    Concept,
    Collection,
    Label,
    Note
)


class RDFProvider(VocabularyProvider):
    '''
    A :class:`skosprovider.providers.VocabularyProvider` that uses RDF
    '''

    def get_all(self, **kwargs):
        super(RDFProvider, self).get_all(**kwargs)

    def find(self, query, **kwargs):
        super(RDFProvider, self).find(query, **kwargs)

    def expand(self, id):
        super(RDFProvider, self).expand(id)

    def expand_concept(self, id):
        super(RDFProvider, self).expand_concept(id)

    def get_by_uri(self, uri):
        super(RDFProvider, self).get_by_uri(uri)

    def get_vocabulary_id(self):
        return super(RDFProvider, self).get_vocabulary_id()

    def get_top_display(self, **kwargs):
        super(RDFProvider, self).get_top_display(**kwargs)

    def __init__(self, metadata, **kwargs):
        super(RDFProvider, self).__init__(metadata, **kwargs)

    def get_top_concepts(self, **kwargs):
        super(RDFProvider, self).get_top_concepts(**kwargs)

    def get_by_id(self, id):
        super(RDFProvider, self).get_by_id(id)

    def get_metadata(self):
        return super(RDFProvider, self).get_metadata()

    def _get_language(self, **kwargs):
        return super(RDFProvider, self)._get_language(**kwargs)

    def get_children_display(self, id, **kwargs):
        super(RDFProvider, self).get_children_display(id, **kwargs)

