#! encoding:utf-8
from wn_analyzer import WordNetAnalyzer, maximum_judge_function
import logging
from similarity import path_similarity
from interpreter import db

log = logging.getLogger('lenin')

class DocumentAnalyzer(object):
    """
    @concepts = A dict mapping words to synsets
    @similarity_function = A similarity function from similarity module
    """
    def __init__(self, synsets, similarity_function=path_similarity):
        self.word_to_synsets = synsets
        self.similarity_function = similarity_function
        self.prefix = similarity_function.func_name
        self.analyzers = dict((word, WordNetAnalyzer(synsets=synsets, 
                similarity_function=similarity_function, 
                judge_function=maximum_judge_function))
            for word, synsets in self.word_to_synsets.iteritems())
 
    @property
    def name(self):
        print self.similarity_function.func_name

    def analyze_document(self, document):
        document_analysis = self.__get_analysis_for(document)

        for word, synsets in self.word_to_synsets.iteritems():
            document_analysis[self.prefix][word] = self.__analyze_document_against_synsets(
                word=word, synsets=synsets,
                document=document, 
                document_analysis=document_analysis)
        
        db.document_analysis.save(document_analysis)
        return document_analysis[self.prefix]

    def __get_analysis_for(self, document):
        document_analysis = db.document_analysis.find_one({"document_id": document._id}) or {"document_id": document._id}
        if not self.prefix in document_analysis.keys():
            document_analysis[self.prefix] = {}
        return document_analysis

    def __analyze_document_against_synsets(self, document, word, synsets, document_analysis):
        # Only calculate in case there's no analysis done
        if word in document_analysis[self.prefix].keys():
            return document_analysis[self.prefix][word]
        analyzer = self.analyzers[word]
        return analyzer.judge_doc(document)
    
