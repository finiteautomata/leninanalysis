# This Python file uses the following encoding: utf-8
from __future__ import division
import nltk
import logging

from nltk.corpus import wordnet as wn
from information_value.models import *

log = logging.getLogger('lenin')

import config
reload(config)

#Similarity definitions: http://nltk.googlecode.com/svn/trunk/doc/api/nltk.corpus.reader.wordnet.Synset-class.html#path_similarity
class WordNetAnalyzer:

  #synsets is a list((synset, ponderation))
  #sum(ponderation) must be 1
  def __init__(self, word, use_similarity = config.analyzer['SIMILARITY_FUNCTION']):

    self.word = word
    self.synsets = WordNetAnalyzer.get_init_synsets_for_word(word)
    self.use_similarity = use_similarity

  def set_similarity(self, use_similarity):
    '''
    synset similarity measume
    '''
    self.use_similarity = use_similarity



  @staticmethod
  def get_init_synsets_for_word(word, only_first = config.analyzer["WNA_SYNSET_USE_ONLY_FIRST"] ):
    '''
    creates the trivial synsets set for a given word
    '''

    synsets = WordNetAnalyzer.get_word_synsets(word, only_first)
    return [(synset, 1.0/ len(synsets)) for synset in synsets]

  #get all synsets for a given word
  @staticmethod
  def get_word_synsets(word, only_first = False):
    lemmas = wn.lemmas(word)
    
    #si no me da lemmas, intento algo
    if len(lemmas) == 0:
      wnl = nltk.WordNetLemmatizer()
      lemmatized_word = wnl.lemmatize(word)
      lemmas = wn.lemmas(lemmatized_word)
      if len(lemmas) == 0:
        return []
    
    #some distances doesn't handle not-noun words
    synsets =  [lemma.synset for lemma in lemmas if lemma.synset.name.split('.')[1] == 'n']
    if only_first:
      return synsets[:1]
    
    return synsets

  def judge_list(self, doc_list):
    if doc_list.total_docs == 0:
      return None
    all_docs_with_values = [(doc, self.judge_doc(doc))  for doc in doc_list ]

    filtered_with_values = [(d, v)  for (d,v) in all_docs_with_values if v > config.analyzer["DOC_SIMILARITY_THRESHOLD"]]
    if len(filtered_with_values) == 0:
      return 0

    return config.analyzer["DOC_TO_YEAR_PONDERATION"](all_docs_with_values, filtered_with_values)     
 
   
  def judge_doc(self, document):
    '''
      returns a value between 0 and 1
    '''
    top_words_with_ivs = document.top_words(config.analyzer["TAKE_N_TOP_WORDS"])
    top_words_with_results = self.judge_top_words(top_words_with_ivs)
    
    
    doc_value = config.analyzer["TOP_WORDS_TO_DOC_PONDERATION"](top_words_with_results)
    
    if doc_value > config.analyzer["DOC_SIMILARITY_THRESHOLD"]:
      log.info("{2:.2f} =  doc('{1}', '{0}')".format(document.short_name.encode('utf-8'), self.word, doc_value))
    
    for (word, ponderation, result) in top_words_with_results:
       if result > config.analyzer["DOC_SIMILARITY_THRESHOLD"]:
          log.info("{2:.2f} = word('{1}', '{0}') word-iv: {3:.2f} ".format(word, self.word, result, ponderation))
    
    
    return doc_value

  def judge_top_words(self, top_words):
    '''
    returns list of tuples
        tuple[0] = word
        tuple[1] = word_document_ponderation [between 0 and 1]
        tuple[2] = word_distance_to_synset [between 0 and 1])
    '''
    return [(word, word_document_ponderation, self.judge_word(word) )  for (word, word_document_ponderation) in top_words]


  def judge_word(self, word, only_first_synset = config.analyzer["INPUT_SYNSET_USE_ONLY_FIRST"]):
    '''
      calls judge_synset
      @returns double a value between 1.0 and 0.0
    '''
    synsets_results = [self.judge_synset(synset) for synset in self.get_word_synsets(word, only_first_synset)]
    if len(synsets_results) != 0: 
      res = config.analyzer["SYNSETS_TO_WORD_PONDERATION"](synsets_results)
      #res =  sum(synsets_results)
      #res =  sum(synsets_results) / len(synsets_results) 
    else: 
      res= 0

    return res

  
 

  def judge_synset(self, synset):

    if self.use_similarity == 'path':
        all_distances = [syn.path_similarity(synset) for (syn, ponderacion) in self.synsets]    
    elif self.use_similarity == 'lch':
        all_distances = [syn.lch_similarity(synset) for (syn, ponderacion) in self.synsets]
    elif self.use_similarity == 'wup':
        all_distances = [syn.wup_similarity(synset) for (syn, ponderacion) in self.synsets]
    
    return config.analyzer["SYNSET_SIMILARITY_PONDERATION"](all_distances)

  
def wna_for(word):
  return WordNetAnalyzer(word)


def wnas_for(words):
  res = dict()
  for word in words:
    res[word] = wna_for(word)

  return res

def year_vs_concept_data(concepts = None, year_min = 1899, year_max = 1923):
  
  if not concepts:
    concepts = ["war", "idealism", "revolution", "philosophy"]
  
  analyzers = dict()
  res = dict()

  for concept in concepts:
    analyzers[concept] = wna_for(concept)

  print "years {0} - {1} vs concepts: {2}. working...".format(year_min, year_max, concepts)
  for year in range(year_min, year_max):
    res[year] = dict()
    output = ""
    doc_list = DocumentList("", False, str(year))
    for concept in concepts:
      res[year][concept] =  analyzers[concept].judge_list(doc_list)
      
      log.info("{2:.2f} = year-distance('{1}', '{0}') ".format(year, concept, res[year][concept]))
      output += "{0}: {1:.2f} ".format(concept, res[year][concept])
    
    print "year: {0}, #doc: {1}, res: {2}".format(year, doc_list.total_docs, output)
  return res
  