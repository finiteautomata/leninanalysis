#! encoding:utf-8
import synset_analyzer
from synset_analyzer import SynsetAnalyzer, maximum_judge_function
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
        self.synsets = synsets
        self.similarity_function = similarity_function
        self.prefix = similarity_function.func_name
        self.analyzers = dict(
            (synset, SynsetAnalyzer(
                synsets=[synset], 
                similarity_function=similarity_function, 
                judge_function=maximum_judge_function)
            ) for synset in self.synsets)
 
    @property
    def name(self):
        print self.similarity_function.func_name + " document analyzer"

    def analyze_document(self, document):
        document_analysis = {} #self.__get_analysis_for(document)[self.prefix]
        self.best_word_for = {}

        for synset in self.synsets:
            document_analysis[synset.name] = self.analyze_synset(synset=synset, document=document)
        
        #db.document_analysis.save(document_analysis)
        return document_analysis

   
    def analyze_synset(self, document, synset):
        # Only calculate in case there's no analysis done
        analyzer = self.analyzers[synset]
        doc_analysis = analyzer.judge_doc(document)
        self.best_word_for[synset.name] = synset_analyzer.best_word
        return doc_analysis
    
    def __get_analysis_for(self, document):
        document_analysis = db.document_analysis.find_one({"document_id": document._id}) or {"document_id": document._id}
        if not self.prefix in document_analysis.keys():
            document_analysis[self.prefix] = {}
        return document_analysis
