# coding: utf-8
import logging
from ming import Session, create_datastore
from ming import schema

from ming.odm.declarative import MappedClass
from ming.odm import ODMSession

import config
#from ming.odm import RelationProperty, ForeignIdProperty
from ming.odm.property import ForeignIdProperty
from ming.odm.property import FieldProperty, RelationProperty


log = logging.getLogger('lenin')

bind = create_datastore(config.DATABASE_NAME)
session = Session(bind)
odm_session = ODMSession(doc_session=session)



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


class InformationValueResult(MappedClass):

    class __mongometa__:
        session = odm_session
        name = 'information_value_result'

    _id = FieldProperty(schema.ObjectId)
    window_size = FieldProperty(schema.Int)
    iv_words = FieldProperty(schema.Anything)
    document_id = ForeignIdProperty(Document)
    document = RelationProperty(Document)
