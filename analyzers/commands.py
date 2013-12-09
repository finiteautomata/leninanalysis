#! coding:utf-8
from information_value.models import DocumentList
from document_analyzer import DocumentAnalyzer
from guppy import hpy
def analyze_documents(concepts):
    docs = DocumentList()
    analyzer = DocumentAnalyzer(concepts=concepts)
    
    for doc in docs:

        res = analyzer.analyze_document(doc)
        print res
        h = hpy()
        print h.heap()
