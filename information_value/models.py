from ming import Session, create_datastore
from ming import schema

from ming.odm.declarative import MappedClass
from ming.odm import ODMSession


#from ming.odm import RelationProperty, ForeignIdProperty
from ming.odm.property import ForeignIdProperty
from ming.odm.property import FieldProperty, RelationProperty


bind = create_datastore('lenin')
session = Session(bind)
odm_session = ODMSession(doc_session=session)


class Document(MappedClass):

    class __mongometa__:
        session = odm_session
        name = 'document'

    _id = FieldProperty(schema.ObjectId)
    url = FieldProperty(str)
    name = FieldProperty(str)
    text = FieldProperty(str)
    month = FieldProperty(str)
    year = FieldProperty(int)
    results = RelationProperty('InformationValueResult')


class InformationValueResult(MappedClass):

    class __mongometa__:
        session = odm_session
        name = 'information_value_result'

    _id = FieldProperty(schema.ObjectId)
    window_size = FieldProperty(int)
    results = FieldProperty([int])
    document_id = ForeignIdProperty(Document)
    document = RelationProperty(Document)
