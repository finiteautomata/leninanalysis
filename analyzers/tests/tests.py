#! coding: utf-8
# THIS IMPORT MUST BE THE FIRST IN EVERY tests.py FILE
#from test import LeninTestCaseNoDrop
from unittest import TestCase
from unittest import skip

from nltk.corpus import wordnet as wn
from analyzers.wn_analyzer import WordNetAnalyzer



class TestAnalyzers(TestCase):

  def test_war_analyzer(self):    
    all_war_analyzer =  WordNetAnalyzer("war")
    
    self.assertEqual(1.0, all_war_analyzer.judge_word("war"))

    #self.assertEqual(1.0, one_war_analyzer.judge_word("warrior"))
    self.assertEqual(0.125, all_war_analyzer.judge_word('bomb')) #un hipernimo, da 0.5
    self.assertEqual(0.125, all_war_analyzer.judge_word('bomb')) #un hipernimo, da 0.5
    

  @skip
  def test_simple_wn_analyzers(self):
    politics_synsets = [(wn.synset('politics.n.01'), 1.0)]
    praxis_synsets = [(wn.synset('practice.n.03'), 1.0)]
    theory_synsets = [(wn.synset('theory.n.01'), 1.0)]
    
    rev_synsets = [(wn.synset('revolution.n.02'), 1.0)] #the overthrow of a government by those who are governed
    analyzers = {   
                      'politics': WordNetAnalyzer(politics_synsets), 
                      'theory': WordNetAnalyzer(theory_synsets),
                      'praxis': WordNetAnalyzer(praxis_synsets),
                      'revolution': WordNetAnalyzer(rev_synsets),
                  }
    self.assertAlmostEqual(0.1666, analyzers['revolution'].judge_word("revolution"), 3) #epic fail
      
    rev_synsets = [(wn.synset('revolution.n.02'), 1.0)] #the overthrow of a government by those who are governed      
