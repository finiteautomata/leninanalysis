#! coding: utf-8
# THIS IMPORT MUST BE THE FIRST IN EVERY tests.py FILE
from test import LeninTestCase
from unittest import TestCase
import pymongo
from pymongo.errors import DuplicateKeyError
from information_value.models import odm_session
from information_value.models import Document
from information_value.models import InformationValueResult
from factories import DocumentFactory, InformationValueResultFactory

class TestModels(LeninTestCase):

    def test_simple_document_pesistence(self):
        simple_doc = Document(
                url="http://www.sarasa.com.ar",
                text="sarasa sarasa sarasa sarasa sarasa!",
                name="test01",
                month="Mar",
                year='2013'
                )
        odm_session.flush()
        from_db = Document.query.get(name="test01")
        self.assertEquals(simple_doc.name, from_db.name)
        self.assertEquals(simple_doc.text, from_db.text)
        self.assertEquals(simple_doc.url, from_db.url)
        self.assertEquals(simple_doc.month, from_db.month)
        self.assertEquals(simple_doc.year, from_db.year)


    def test_duplicate_result_raises_exception(self):
        simple_doc = DocumentFactory()
        InformationValueResultFactory(document=simple_doc, window_size=500)

        odm_session.flush()
        with self.assertRaises(DuplicateKeyError):
            InformationValueResultFactory(document=simple_doc, window_size=500)
            odm_session.flush()

        count = InformationValueResult.query.find({"document_id":simple_doc._id}).count()
        self.assertEquals(count, 1)

class InformationValueResultTest(LeninTestCase):

    def test_create_information_value_result_and_sets_iv_sum_correctly(self):
        simple_doc = DocumentFactory()
        iv_result = InformationValueResultFactory(    
            window_size = 200,
            iv_words = {"sarasa" : 1.0},
            document = simple_doc,
            )

        self.assertEquals(iv_result.iv_sum, 1.0)

    def test_calculates_iv_sum_correctly_according_to_passed_threshold(self):
        pass