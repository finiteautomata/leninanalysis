# This Python file uses the following encoding: utf-8
from __future__ import division
import logging
from similarity import path_similarity, get_word_synsets
from information_value.models import DocumentList

log = logging.getLogger('lenin')

import config
reload(config)


def ponderated_judge_function(partial_results):
    return sum(ponderation * similarity for (word, ponderation, similarity) in partial_results)

#this is horrible
best_word = None
def maximum_judge_function(partial_results):
    global best_word
    max_word, _, max_similarity  = max(partial_results, key=lambda x: x[2])
    best_word = max_word
    return max_similarity

# Similarity definitions:
# http://nltk.googlecode.com/svn/trunk/doc/api/nltk.corpus.reader.wordnet.Synset-class.html#path_similarity
class SynsetAnalyzer:
    def __init__(self, synsets, similarity_function = path_similarity, judge_function=ponderated_judge_function ):
        self.synsets = synsets
        self.judge_function = judge_function
        self.similarity_function = similarity_function

    def judge_list(self, doc_list):
        if doc_list.total_docs == 0:
            return None
        all_docs_with_values = [(doc, self.judge_doc(doc))  for doc in doc_list ]

        if len(all_docs_with_values) == 0:
            return 0

        return (sum(v for (d, v) in all_docs_with_values) / len(all_docs_with_values))   


    def judge_doc(self, document, number_of_senses=20):
        '''
          returns a value between 0 and 1
        '''
        top_senses = document.top_words(number_of_senses)

        """
        Here we have in partial_results
        [(word, word_ponderation, similarity) for word in document.top_words]
        We pass this to the judge function
        """
        partial_results = [(word, ponderation, self.judge_word(word)) for (word, ponderation) in top_senses]
        return self.judge_function(partial_results)


    def judge_word(self, word):
        '''
          @returns double a value between 1.0 and 0.0
        '''
        return self.similarity_function(self.synsets, get_word_synsets(word)) 

 
def wna_for(word):
    return SynsetAnalyzer(word)



def wnas_for(words):
    res = dict()
    for word in words:
      res[word] = wna_for(word)

    return res


def year_vs_concept_data(concepts = None, year_min = 1899, year_max = 1923):
  
    if not concepts:
        concepts = ["war", "idealism", "revolution", "philosophy"]

    res = dict()

    analyzers = dict((concept, wna_for(concept)) for concept in concepts)

    print "years {0} - {1} vs concepts: {2}. working...".format(year_min, year_max, concepts)
    for year in range(year_min, year_max):
        analyze_year(concepts, analyzers)

    return res

def analyze_year(concepts, analyzers):
    year_res = {}
    for concept in concepts:
      year_res[concept] = _year_vs_concept_analysis(concept, year, analyzers)
    
    log.info("{2:.2f} = year-distance('{1}', '{0}') ".format(year, concept, res[year][concept]))
    output += "{0}: {1:.2f} ".format(concept, res[year][concept])
  
    print "year: {0}, #doc: {1}, res: {2}".format(year, doc_list.total_docs, output)

def _year_vs_concept_analysis(concept, year, analyzers):
    doc_list = DocumentList("", False, year)
    analyzer = analyzers[concept]
    return analyzer.judge_list(doc_list)
