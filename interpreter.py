#! coding utf-8
"""
  Run this before opening a console
"""
import ming
import config

ming_config = {'ming.document_store.uri': config.DATABASE_URL}
ming.configure(**ming_config)

from information_value.models import Document, DocumentList, InformationValueResult, doc_for
from analyzers.wn_analyzer import WordNetAnalyzer, year_vs_concept_data, wnas_for, wna_for
from nltk.corpus import wordnet as wn

from cccp import init_logging
from pymongo import MongoClient
init_logging()
client = MongoClient()
db = client[config.DATABASE_NAME]
