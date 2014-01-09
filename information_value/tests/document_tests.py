#! coding: utf-8
# THIS IMPORT MUST BE THE FIRST IN EVERY tests.py FILE
from test import LeninTestCase
from unittest import skip
import types
import operator
import pymongo
from mock import Mock
from pymongo.errors import DuplicateKeyError
from information_value.models import odm_session
from information_value.models import Document
from information_value.models import InformationValueResult
from factories import DocumentFactory, InformationValueResultFactory
    
class DocumentTest(LeninTestCase):
    @skip
    def test_top_words_returns_words_in_same_order_of_iv_top_words_for_best_window_size(self):
        top_words = [
            ("bar", 0.2),
            ("foo", 0.01),
            ("john", 0.001),
            ("sarasa", 0.0005),
        ]
        document = get_document_with_top_words(top_words=top_words)

        self.assertEquals(top_words, document.top_words(window_size=100))

    def test_information_value_result_is_created_if_it_didnt_exists(self):
        document = DocumentFactory()
        calculator_class = mock_calculator_class_returning(iv_words=[
            ("bar", 0.2),
            ("foo", 0.01),
            ("john", 0.001),
            ("sarasa", 0.0005),
        ])

        document.get_iv_by_window_size(100, calculator_class=calculator_class)

        calculator_class.assert_called_with(document.tokens)

def get_document_with_top_words(top_words):
    document = DocumentFactory()
    document.get_iv_by_window_size = types.MethodType(lambda self, window_size: top_words, document)
    return document

def mock_calculator_class_returning(iv_words):
    calculator_mock = Mock()
    calculator_mock.information_value.return_value = iv_words

    return Mock(return_value=calculator_mock)
