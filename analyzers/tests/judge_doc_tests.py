#! coding:utf-8
from analyzers.wn_analyzer import WordNetAnalyzer 
from unittest import TestCase
from mock import Mock
from utils import document_returning_top_words

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
    
        self.assertAlmostEqual(wna.judge_doc(doc), 0.166666666)

    def test_judge_doc_should_return_1_for_a_document_with_two_equal_words(self):
        wna = WordNetAnalyzer("war")
        doc = Mock()
        doc.top_words.return_value = [("war", .5), ("war", .5)]
    
        self.assertAlmostEqual(wna.judge_doc(doc), 1.0)


    def test_should_take_into_account_an_immediate_hypernym(self):
        # Action is a lemma of military action, which is an hypernym of war.n.01
        wna = WordNetAnalyzer("action")
        doc = document_returning_top_words(("war", 0.5), ("music", 0.4), ("fruit", 0.1))

        # As it is an hypernym, its similarity is 0.5
        self.assertGreaterEqual(wna.judge_doc(doc), 0.25)


