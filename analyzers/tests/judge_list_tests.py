#! coding:utf-8
from unittest import TestCase, skip
from nltk.corpus import wordnet as wn
from analyzers.similarity import path_similarity
from analyzers.synset_analyzer import SynsetAnalyzer 
from utils import document_returning_top_words, create_document_list

class JudgeListTests(TestCase):
    def test_returns_0_for_no_documents(self):
        wna = SynsetAnalyzer(synsets=[wn.synset("war.n.01")])
        doc_list = create_document_list()
        self.assertAlmostEqual(wna.judge_list(doc_list), .0)

    def test_returns_1_for_document_with_one_top_word(self):
        wna = SynsetAnalyzer(synsets=[wn.synset("war.n.01")])
        doc_list = create_document_list(
            document_returning_top_words(("war", 1.0))
        )

        self.assertAlmostEqual(wna.judge_list(doc_list), 1.0)

    def test_returns_0_for_document_with_one_distinct_top_word(self):
        wna = SynsetAnalyzer(synsets=[wn.synset("war.n.01")])
        doc_list = create_document_list(
            document_returning_top_words(("music", 1.0))
        )
        self.assertAlmostEqual(wna.judge_list(doc_list), path_similarity([wn.synset("war.n.01")], wn.synsets("music")))

    @skip
    def test_returns_the_distance_ponderated_with_the_top_word_value(self):
        wna = SynsetAnalyzer(synsets=[wn.synset("war.n.01")])
        doc_list = create_document_list(
            document_returning_top_words(("music", .5), ("war", 0.5))
        )
        self.assertAlmostEqual(wna.judge_list(doc_list), .5)

    def test_with_two_documents(self):
        wna = SynsetAnalyzer(synsets=[wn.synset("war.n.01")])
        doc_list = create_document_list(
            document_returning_top_words(("war", 1.0)),
            document_returning_top_words(("music", 1.0))
        )

        self.assertGreaterEqual(wna.judge_list(doc_list), 0.5 + 0.5 * path_similarity([wn.synset("war.n.01")], wn.synsets("music")))

    @skip
    def test_with_two_documents_with_several_top_words(self):
        wna = SynsetAnalyzer(synsets=[wn.synset("war.n.01")])
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
