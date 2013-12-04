#! encoding:utf-8
from wn_analyzer import wna_for
import logging
from interpreter import db

log = logging.getLogger('lenin')

class DocumentAnalyzer(object):
    def __init__(self, concepts):
        self.concepts = concepts
        self.analyzers = dict((concept, wna_for(concept)) for concept in concepts)
 
    def analyze_document(self, document):
        document_analysis = db.document_analysis.find_one({"document_id": document._id}) or {"document_id": document._id}
        
        for concept in self.concepts:
            self.__analyze_document_against_concept(concept=concept,
                document=document,
                document_analysis=document_analysis)
        
        db.document_analysis.save(document_analysis)
        return document_analysis

    def __analyze_document_against_concept(self, document, concept, document_analysis):
        # Only calculate in case there's no analysis done
        if concept in document_analysis.keys():
            return
        analyzer = self.analyzers[concept]
        document_analysis[concept] = analyzer.judge_doc(document)
    
