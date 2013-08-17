#! coding: utf-8
# THIS IMPORT MUST BE THE FIRST IN EVERY tests.py FILE
from test import LeninTestCase
from unittest import TestCase
import types
import operator
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
        simple_doc = DocumentFactory()
        
        iv_result = InformationValueResultFactory(
            iv_words = dict([("w%s" % i,0.001 * i) for i in range(100)]),
            sum_threshold = 0.03
        )

        """
         It should sum the three most valuable words... that's it:
            w99, w98, w97, which its sum is 
            0.099 + 0.098 + 0.097 
        """
        self.assertAlmostEqual(iv_result.iv_sum, 0.099 + 0.098 + 0.097)
    
class DocumentTest(LeninTestCase):

    def test_top_words_returns_words_in_same_order_of_iv_top_words_for_best_window_size(self):
        top_words = [
            ("bar", 0.2),
            ("foo", 0.01),
            ("john", 0.001),
            ("sarasa", 0.0005),
        ]

        document = get_document_with_top_words(top_words=top_words)

        self.assertEquals([word for word, iv in document.top_words()], [word for word, iv in document.top_words()])

def get_document_with_top_words(top_words):
    document = DocumentFactory()
    document.get_iv_by_window_size = types.MethodType(lambda self, window_size: top_words, document)
    return document
