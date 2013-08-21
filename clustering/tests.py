#! coding:utf-8
from mock import Mock
from unittest import TestCase
from distance import path_distance, word_path_distance

class DistanceTest(TestCase):

    def test_distance_to_itself_should_be_zero(self):
        iv_words = [
            ("war", 0.1),
            ("revolution", 0.09),
            ("lenin", 0.08),
        ]

        document = create_document_with_words(iv_words)

        self.assertAlmostEqual(path_distance(document, document), 0.0)

    def test_distance_to_text_with_same_iv_words_but_different_order_should_be_zero_too(self):
        document1 = create_document_with_words([
            ("war", 0.1),
            ("revolution", 0.09),
            ("lenin", 0.08),
        ])
        document2 = create_document_with_words([
            ("revolution", 0.09),
            ("lenin", 0.08),
            ("war", 0.001),
        ])


        self.assertAlmostEqual(path_distance(document1, document2), 0.0)

    def test_distance_to_text_skips_verbs(self):
        document1 = create_document_with_words([
            ("war", 0.1),
            ("is", 0.01),
        ])
        document2 = create_document_with_words([
            ("revolution", 0.3),
            ("kicked", 0.01)
        ])

        self.assertAlmostEqual(path_distance(document1, document2), word_path_distance("war", "revolution"))



def create_document_with_words(iv_words):
    document = Mock()
    document.top_words.return_value = iv_words
    return document
