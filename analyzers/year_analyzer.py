#! coding: utf-8
from information_value.models import Document, DocumentList
from wn_analyzer import wna_for
import logging

log = logging.getLogger('lenin')

class YearAnalyzer(object):
    def __init__(self, concepts):
        self.concepts = concepts
        self.analyzers = dict((concept, wna_for(concept)) for concept in concepts)
 
    def analyze_year(self, year):
        year_res = {}

        documents = Document.query.find({"year": year})
        number_of_documents = documents.count()
        output = ""
        
        for concept in self.concepts:
            analyzer = self.analyzers[concept]
            year_res[concept] = analyzer.judge_list(documents)
            log.info("{2:.2f} = year-distance('{1}', '{0}') ".format(year, concept, year_res[concept]))
            output += "{0}: {1:.2f} ".format(concept, year_res[concept])
      
        print "year: {0}, #doc: {1}, res: {2}".format(year, number_of_documents, output)
        return year_res

    def _year_vs_concept_analysis(self, concept, year):
        analyzer = self.analyzers[concept]
        return analyzer.judge_list(doc_list)