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

class TestAnalyzers(unittest.TestCase):

    def test_wn_analyzer(self):
        #analyzer = WordNetAnalyzer();    
        state_list = DocumentList("State and Revolution")
        state = state_list.documents[0]
        top_words = state.top_words()

        self.assertEquals(u'working', top_words[0][0])
    

