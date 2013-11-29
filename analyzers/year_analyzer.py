#! coding: utf-8
from information_value.models import DocumentList
from wn_analyzer import wna_for
import logging
from interpreter import db

log = logging.getLogger('lenin')

class YearAnalyzer(object):
    def __init__(self, concepts):
        self.concepts = concepts
        self.analyzers = dict((concept, wna_for(concept)) for concept in concepts)
 
    def analyze_year(self, year):
        year_analysis = db.year_analysis.find_one({"year": year}) or {"year": year}
        documents = DocumentList(year=year)
        
        for concept in self.concepts:
            self.__analyze_year_against_concept(documents=documents, concept=concept, year_analysis=year_analysis)
        
        db.year_analysis.save(year_analysis)
        return year_analysis

    def __analyze_year_against_concept(self, documents, concept, year_analysis):
        # Only calculate in case there's no analysis done
        if concept in year_analysis.keys():
            return
        analyzer = self.analyzers[concept]
        year_analysis[concept] = analyzer.judge_list(documents)
    
