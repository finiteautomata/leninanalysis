#! coding: utf-8
# THIS IMPORT MUST BE THE FIRST IN EVERY tests.py FILE
#from test import LeninTestCaseNoDrop
import unittest
from unittest import TestCase
from pymongo import MongoClient

client = MongoClient()

from information_value.models import Document
from information_value.models import InformationValueResult
from information_value.models import DocumentList

from analyzers.wn_analyzer import WordNetAnalyzer
from analyzers.wn_analyzer import wn

class TestAnalyzers(unittest.TestCase):

    def test_wn_analyzer(self):
        
        state_list = DocumentList("State and Revolution")
        state = state_list.documents[0]

        theoretical_synsets = [
                                #(wn.synset('entity.n.01'), 1.0),
                                #(wn.synset('politics.n.05'), 1.0), #'the activities and affairs involved in managing a state or a government''the study of government of states and other political units'
                                (wn.synset('abstraction.n.06'), 0.5),
                                #(wn.synset('physical_entity.n.01'), 1.0)
                                #(wn.synset("philosophy.n.02"), 1.0), #'the rational investigation of questions about existence and knowledge and ethics'
                                #wn.synset('theory.n.01'),     #a well-substantiated explanation of some aspect of the natural world; an organized system of accepted knowledge that applies in a variety of circumstances to explain a specific set of phenomena
                                (wn.synset('theorization.n.01'), 0.5),  #the production or use of theories
                                #(wn.synset('politics.n.02'), 1.0),#   'the study of government of states and other political units'
                                #(wn.synset('hypothesis.n.02'), 0.8),    #a tentative insight into the natural world; a concept that is not yet verified but that if true would explain certain facts or phenomena
                                #(wn.synset('theory.n.03'), 1.2)      #a belief that can guide behavior
                                ]
        analyzer = WordNetAnalyzer(state, theoretical_synsets);    
        analyzer.get_results()
        #print top_words
        self.assertEquals(u'working', top_words[0][0])
    

