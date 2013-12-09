#! coding:utf-8
from unittest import TestCase, skip
from analyzers.wn_analyzer import WordNetAnalyzer 
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

    @skip
    def test_returns_0_for_document_with_one_distinct_top_word(self):
        wna = WordNetAnalyzer("war")
        doc_list = create_document_list(
            document_returning_top_words(("music", 1.0))
        )
        self.assertAlmostEqual(wna.judge_list(doc_list), .0)

    @skip
    def test_returns_the_distance_ponderated_with_the_top_word_value(self):
        wna = WordNetAnalyzer("war")
        doc_list = create_document_list(
            document_returning_top_words(("music", .5), ("war", 0.5))
        )
        self.assertAlmostEqual(wna.judge_list(doc_list), .5)

    @skip
    def test_with_two_documents(self):
        wna = WordNetAnalyzer("war")
        doc_list = create_document_list(
            document_returning_top_words(("war", 1.0)),
            document_returning_top_words(("music", 1.0))
        )

        self.assertGreaterEqual(wna.judge_list(doc_list), 0.5)

    @skip
    def test_with_two_documents_with_several_top_words(self):
        wna = WordNetAnalyzer("war")
        doc_list = create_document_list(
            # Both docs adds 0.25 of similarity
            document_returning_top_words(("war", 1.0)),
            document_returning_top_words(("war", 1.0)),
            # This one adds 
            document_returning_top_words(("action", 0.5), ("war", 0.25), ("fury", 0.5)),
            # This is filtered because its value is less than 0.4
            document_returning_top_words(("action", 0.25))
        )

        self.assertAlmostEqual(wna.judge_list(doc_list), 0.625)
