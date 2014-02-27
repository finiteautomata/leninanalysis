#! coding:utf-8
import logging
from information_value.models import DocumentList
from document_analyzer import DocumentAnalyzer
from guppy import hpy

log = logging.getLogger('lenin')


def analyze_documents(concepts):
    docs = DocumentList()
    analyzer = DocumentAnalyzer(concepts=concepts)

    for doc in docs:

        res = analyzer.analyze_document(doc)
        log.info(res)
        h = hpy()
        log.info(h.heap())
