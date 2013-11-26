#! coding:utf-8
from mock import Mock

def create_document_list(*docs):
    doc_list_mock = Mock()
    doc_list_mock.__iter__ = Mock()
    doc_list_mock.__iter__.return_value = iter(docs)

    return doc_list_mock

def document_returning_top_words(*ponderated_words):
    doc = Mock()
    doc.top_words.return_value = ponderated_words
    return doc
