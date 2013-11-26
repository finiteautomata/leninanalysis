#! coding:utf-8
from analyzers.wn_analyzer import WordNetAnalyzer 
from unittest import TestCase
from mock import Mock

class JudgeDocTests(TestCase):
    def test_judge_doc_should_return_1_for_a_document_with_just_one_word(self):
        wna = WordNetAnalyzer("war")
        doc = Mock()
        doc.top_words.return_value = [("war", 1.0)]
    
        self.assertAlmostEqual(wna.judge_doc(doc), 1.0)

    def test_judge_doc_should_return_0_for_a_document_with_just_one_distinct_word(self):
        wna = WordNetAnalyzer("music")
        doc = Mock()
        doc.top_words.return_value = [("war", 1.0)]
    
        self.assertAlmostEqual(wna.judge_doc(doc), .0)

