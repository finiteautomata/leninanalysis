#! coding: utf-8
# THIS IMPORT MUST BE THE FIRST IN EVERY tests.py FILE
from unittest import skip
import types
from nltk.corpus import wordnet as wn
from mock import Mock
from test import LeninTestCase
from factories import DocumentFactory
    
class DocumentTest(LeninTestCase):

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

    def test_top_senses_for_empty_top_words_is_empty(self):
        document = get_document_with_top_words([])

        self.assertEquals([], document.top_senses())

    def test_top_senses_for_one_top_word_returns_correct_sense(self):
        document = get_document_with_top_words([('bank', 1.0)], text='I went to the bank to deposit my money')       

        self.assertEqual([wn.synset('depository_financial_institution.n.01')],  document.top_senses()) 


def get_document_with_top_words(top_words, **kwargs):
    document = DocumentFactory(**kwargs)
    document.top_words = types.MethodType(lambda self: top_words, document)
    return document


def mock_calculator_class_returning(iv_words):
    calculator_mock = Mock()
    calculator_mock.information_value.return_value = iv_words

    return Mock(return_value=calculator_mock)
