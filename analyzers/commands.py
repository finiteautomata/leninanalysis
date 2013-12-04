#! coding:utf-8
from information_value.models import DocumentList
from document_analyzer import DocumentAnalyzer

def analyze_documents(concepts):
    docs = DocumentList()
    analyzer = DocumentAnalyzer(concepts=concepts)
    
    for doc in docs:
        print analyzer.analyze_document(doc)
