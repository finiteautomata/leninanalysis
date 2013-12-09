#! coding:utf-8
from unittest import TestCase, skip
from analyzers.year_analyzer import YearAnalyzer
#from test import LeninTestCase
from mock import patch, Mock 

class YearAnalyzerTest(TestCase):
    def test_can_create_an_analyzer(self):
        YearAnalyzer(concepts=["war", "toilette", "mathemathics"])

    @skip
    @patch('analyzers.year_analyzer.Document')
    def test_returns_concept_in_zero_for_no_documents(self, document_class_mock):
        analyzer = YearAnalyzer(concepts=["war", "toilette"])
        document_class_mock.query.find.return_value = query_returning([])
        
        ret = analyzer.analyze_year(1899)

        self.assertDictEqual({'toilette':.0, 'war':.0}, ret)

    @skip
    @patch('analyzers.year_analyzer.Document')
    def test_returns_no_concepts_if_none_brought(self, document_class_mock):
        analyzer = YearAnalyzer(concepts=[])
        document_class_mock.query.find_return_value = query_returning([
            document_returning_top_words(("war", .3), ("toilette", .4), ("music", 0.3))
        ])

        ret = analyzer.analyze_year(1899)

        self.assertDictEqual({}, ret)



def query_returning(docs):
    query = Mock()
    query.__iter__ = Mock()
    query.__iter__.return_value = iter(docs)
    query.count.return_value = len(docs)
    return query


def document_returning_top_words(*ponderated_words):
    doc = Mock()
    doc.top_words.return_value = ponderated_words
    return doc
