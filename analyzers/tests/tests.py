#! coding: utf-8
# THIS IMPORT MUST BE THE FIRST IN EVERY tests.py FILE
#from test import LeninTestCaseNoDrop
from test import LeninTestCase
from unittest import TestCase
from unittest import skip


from analyzers.wn_analyzer import WordNetAnalyzer
from analyzers.wn_analyzer import wn


class TestAnalyzers(TestCase):

  def test_war_analyzer(self):
    
    #genera [(synset, ponderacion)] para todos los synsets de una palabra
    all_war_synset_list = WordNetAnalyzer.get_init_synsets_for_word("war")
    

    self.assertEqual(4, len(all_war_synset_list), "todos los synsets de la palabra 'war' son 4")
    self.assertEqual((wn.synset("war.n.01"), 0.25), all_war_synset_list[0], "el parametro de WNA es una lista ponderada de synsets (sum(ponderacion) = 1)")
    self.assertEqual((wn.synset("war.n.02"), 0.25), all_war_synset_list[1])
    self.assertEqual((wn.synset("war.n.03"), 0.25), all_war_synset_list[2])
    self.assertEqual((wn.synset("war.n.04"), 0.25), all_war_synset_list[3])
    
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
