#! coding: utf-8
# THIS IMPORT MUST BE THE FIRST IN EVERY tests.py FILE
#from test import LeninTestCaseNoDrop
from test import LeninTestCase
from unittest import TestCase
from unittest import skip

from information_value.models import Document
from information_value.models import InformationValueResult
from information_value.models import DocumentList

from analyzers.wn_analyzer import WordNetAnalyzer
from analyzers.wn_analyzer import wn

class TestAnalyzers(LeninTestCase):

  def test_war_analyzer(self):
    
    #genera [(synset, ponderacion)] para todos los synsets de una palabra
    all_war_synset_list = WordNetAnalyzer.get_init_synsets_for_word("war")
    just_first_war_synset_list = WordNetAnalyzer.get_init_synsets_for_word("war", take_only_first = True) #solo genera para el primer synset
    
    self.assertEqual(1, len(just_first_war_synset_list), "take_only_first => toma solo el primer sentido")
    self.assertEqual([(wn.synset("war.n.01"), 1.0)], just_first_war_synset_list, "el parametro de WNA es una lista ponderada de synsets")
    

    self.assertEqual(4, len(all_war_synset_list), "todos los synsets de la palabra 'war' son 4")
    self.assertEqual((wn.synset("war.n.01"), 0.25), all_war_synset_list[0], "el parametro de WNA es una lista ponderada de synsets (sum(ponderacion) = 1)")
    self.assertEqual((wn.synset("war.n.02"), 0.25), all_war_synset_list[1])
    self.assertEqual((wn.synset("war.n.03"), 0.25), all_war_synset_list[2])
    self.assertEqual((wn.synset("war.n.04"), 0.25), all_war_synset_list[3])
    
    all_war_analyzer =  WordNetAnalyzer(all_war_synset_list)
    one_war_analyzer =  WordNetAnalyzer(just_first_war_synset_list)

    self.assertEqual(1.0, one_war_analyzer.judge_synset(just_first_war_synset_list[0][0]), "compara el analizador contra su propio synset")
    self.assertEqual(1.0, all_war_analyzer.judge_synset(all_war_synset_list[0][0]), "la logica es tomar la mayor similaridad entre synsets")

    
    self.assertEqual(1.0, one_war_analyzer.judge_word("war"))
    self.assertEqual(1.0, all_war_analyzer.judge_word("war"))
    self.assertEqual(1.0, all_war_analyzer.judge_word("war", take_only_first_synset = True )) #por default toma todos los synsets
    self.assertEqual(1.0, one_war_analyzer.judge_word("war", take_only_first_synset = True ))

    #self.assertEqual(1.0, one_war_analyzer.judge_word("warrior"))
    self.assertEqual(0.5, all_war_analyzer.judge_synset( wn.synset('civil_war.n.01'))) #un hiponimo, da 0.5
    self.assertEqual(0.5, one_war_analyzer.judge_synset( wn.synset('military_action.n.01'))) #un hipernimo, da 0.5
    self.assertEqual(0.125, all_war_analyzer.judge_word('bomb')) #un hipernimo, da 0.5
    self.assertEqual(0.125, all_war_analyzer.judge_word('bomb')) #un hipernimo, da 0.5
    
    #lch: return a score denoting how similar two word senses are, based on the shortest path that connects the senses (as above) 
    # and the maximum depth of the taxonomy in which the senses occur. 
    #The relationship is given as -log(p/2d) where p is the shortest path length and d is the taxonomy depth.
    all_war_analyzer.set_similarity("lch")      
    one_war_analyzer.set_similarity("lch")      
    
    self.assertAlmostEqual(1.558, all_war_analyzer.judge_word('bomb'), 3)
    self.assertAlmostEqual(1.335, all_war_analyzer.judge_word('warrior'), 3)
    self.assertAlmostEqual(0.998, all_war_analyzer.judge_word('kitchen'), 2)
    self.assertAlmostEqual(0.929, one_war_analyzer.judge_word('kitchen'), 2)
    self.assertAlmostEqual(1.440, all_war_analyzer.judge_word('hypothesis'), 3)

    #self.assertEqual(0.125,) #un hipernimo, da 0.5

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
      
    self.assertAlmostEqual(0.1666, analyzers['revolution'].judge_word("revolution", take_only_first_synset = False), 3) #epic fail
    rev_synsets = [(wn.synset('revolution.n.02'), 1.0)] #the overthrow of a government by those who are governed
      
