#! coding:utf-8
from mock import patch
from nltk.corpus import wordnet as wn
from analyzers.document_analyzer import DocumentAnalyzer
from unittest import TestCase
from utils import document_returning_top_words

class DocumentAnalyzerTests(TestCase):
    def setUp(self):
        self.patcher = patch('analyzers.document_analyzer.db')
        db_mock = self.patcher.start()
        db_mock.document_analysis.find_one.return_value = None

    def tearDown(self):
        self.patcher.stop()

    def test_creating_analyzer_with_no_concepts_return_empty_analysis(self):
        analyzer = DocumentAnalyzer(synsets={})
        doc = document_returning_top_words(("war",1.0))

        self.assertEquals({}, analyzer.analyze_document(doc))

    def test_analyze_a_concept(self):
        analyzer = DocumentAnalyzer(synsets={"war": [wn.synset("war.n.01")]})

        doc = document_returning_top_words(("war", 1.0))

        self.assertEquals({"war": 1.0}, analyzer.analyze_document(doc))