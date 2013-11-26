#! coding:utf-8
from unittest import TestCase
from analyzers.wn_analyzer import WordNetAnalyzer 
from mock import Mock
from utils import document_returning_top_words, create_document_list

class JudgeListTests(TestCase):
    def test_returns_0_for_no_documents(self):
        wna = WordNetAnalyzer("war")
        doc_list = create_document_list()
        self.assertAlmostEqual(wna.judge_list(doc_list), .0)

    def test_returns_1_for_document_with_one_top_word(self):
        wna = WordNetAnalyzer("war")
        doc_list = create_document_list(
            document_returning_top_words(("war", 1.0))
        )

        self.assertAlmostEqual(wna.judge_list(doc_list), 1.0)

