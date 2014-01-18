#! coding:utf-8
from nltk.corpus import wordnet as wn
from analyzers.synset_analyzer import SynsetAnalyzer
from unittest import TestCase
from mock import Mock
from utils import document_returning_top_senses

class JudgeSynsetTest(TestCase):
    def test_returns_1_for_same_synset(self):
        analyzer = SynsetAnalyzer(synsets=[wn.synset("war.n.01")])

        self.assertAlmostEqual(analyzer.judge_synset(wn.synset("war.n.01")), 1.0)


class JudgeDocTests(TestCase):
    def test_judge_doc_should_return_1_for_a_document_with_just_one_word(self):
        wna = SynsetAnalyzer([wn.synset("war.n.01")])
        doc = document_returning_top_senses(wn.synset("war.n.01"))    
        self.assertAlmostEqual(wna.judge_doc(doc), 1.0)

    def test_judge_doc_should_return_1_for_a_document_with_two_equal_words(self):
        wna = SynsetAnalyzer([wn.synset("war.n.01")])
        doc = Mock()
        doc = document_returning_top_senses(wn.synset("war.n.01"), wn.synset("war.n.01"))    
    
        self.assertAlmostEqual(wna.judge_doc(doc), 1.0)


    def test_should_take_into_account_an_immediate_hypernym(self):
        # Action is a lemma of military action, which is an hypernym of war.n.01
        wna = SynsetAnalyzer([wn.synset("military_action.n.01")])
        doc = document_returning_top_senses(wn.synset("war.n.01"), wn.synset("music.n.01"), wn.synset("fruit.n.01"))    

        # As it is an hypernym, its similarity is 0.5
        self.assertGreaterEqual(wna.judge_doc(doc), 0.5)
