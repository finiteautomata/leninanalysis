# coding: utf-8
import logging
import hashlib

from pymongo.errors import DuplicateKeyError

from ming import Session, create_datastore
from ming import schema

from ming.odm.declarative import MappedClass
from ming.odm import ODMSession
from ming.odm.mapper import MapperExtension

import config
from ming.odm.property import ForeignIdProperty
from ming.odm.property import FieldProperty, RelationProperty


log = logging.getLogger('lenin')

bind = create_datastore(config.DATABASE_NAME)
session = Session(bind)
odm_session = ODMSession(doc_session=session)


class DocumentWindowSizeDuplicateHash(MapperExtension):
    """
        Used as unique key for Document - WindowSize
    """
    def before_insert(self, instance, state, session):
        doc_window_hash = hashlib.sha1(str(instance.document_id) + str(instance.window_size)).hexdigest()
        if instance.__class__.query.find({'doc_window_hash': doc_window_hash}).count() > 0:
            raise DuplicateKeyError('Duplicate hash found ', doc_window_hash)
        instance.doc_window_hash = doc_window_hash


class Document(MappedClass):

    class __mongometa__:
        session = odm_session
        name = 'document'

    _id = FieldProperty(schema.ObjectId)
    url = FieldProperty(schema.String, unique=True)
    name = FieldProperty(schema.String)
    text = FieldProperty(schema.String)
    month = FieldProperty(schema.String)
    year = FieldProperty(schema.String)
    results = RelationProperty('InformationValueResult')

    @property
    def tokens(self):
        return self.tokenizer(self.text)


class InformationValueResult(MappedClass):

    class __mongometa__:
        session = odm_session
        name = 'information_value_result'
        unique_indexes = [('doc_window_hash', ), ]
        extensions = [ DocumentWindowSizeDuplicateHash ]

    _id = FieldProperty(schema.ObjectId)
    doc_window_hash = FieldProperty(schema.String)
    window_size = FieldProperty(schema.Int)
    iv_words = FieldProperty(schema.Anything)
    document_id = ForeignIdProperty(Document)
    document = RelationProperty(Document)
