#! coding:utf-8
from unittest import TestCase
from analyzers.year_analyzer import YearAnalyzer
#from test import LeninTestCase
from mock import patch, Mock 

class YearAnalyzerTest(TestCase):
    def test_can_create_an_analyzer(self):
        YearAnalyzer(concepts=["war", "toilette", "mathemathics"])

    @patch('analyzers.year_analyzer.Document')
    def test_get_year_analysis_for_empty_year_returns_concepts_in_zero(self, document_class_mock):
        analyzer = YearAnalyzer(concepts=["war", "toilette"])
        document_class_mock.query.find.return_value = query_returning([])
        
        ret = analyzer.analyze_year(1899)

        self.assertDictEqual({'toilette':.0, 'war':.0}, ret)

def query_returning(docs):
    query = Mock()
    query.__iter__ = Mock()
    query.__iter__.return_value = iter(docs)
    query.count.return_value = len(docs)
    return query