#! encoding:utf-8
from wn_analyzer import WordNetAnalyzer
import logging
from similarity import path_similarity
from interpreter import db

log = logging.getLogger('lenin')

class DocumentAnalyzer(object):
    """
    @concepts = The words that are going to be analyzed 
    @similarity_function = A similarity function from similarity module
    """
    def __init__(self, concepts, similarity_function=path_similarity):
        self.concepts = concepts
        self.similarity_function = similarity_function
        self.prefix = similarity_function.func_name
        self.analyzers = dict((concept, WordNetAnalyzer(concept, similarity_function=similarity_function)) for concept in concepts)
 
    def analyze_document(self, document):
        document_analysis = self.__get_analysis_for(document)

        for concept in self.concepts:
            document_analysis[self.prefix][concept] = self.__analyze_document_against_concept(concept=concept,
                document=document, document_analysis=document_analysis)
        
        db.document_analysis.save(document_analysis)
        return document_analysis[self.prefix]

    def __get_analysis_for(self, document):
        document_analysis = db.document_analysis.find_one({"document_id": document._id}) or {"document_id": document._id}
        if not self.prefix in document_analysis.keys():
            document_analysis[self.prefix] = {}
        return document_analysis

    def __analyze_document_against_concept(self, document, concept, document_analysis):
        # Only calculate in case there's no analysis done
        if concept in document_analysis[self.prefix].keys():
            return document_analysis[self.prefix][concept]
        analyzer = self.analyzers[concept]
        return analyzer.judge_doc(document)
    
