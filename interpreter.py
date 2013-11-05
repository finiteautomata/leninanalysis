#! coding utf-8
"""
  Run this before opening a console
"""
import ming
import config

ming_config = {'ming.document_store.uri': config.DATABASE_URL}
ming.configure(**ming_config)

from information_value.models import Document, DocumentList, InformationValueResult
from analyzers.wn_analyzer import WordNetAnalyzer
from nltk.corpus import wordnet as wn

from pymongo import MongoClient
client = MongoClient()
db = client[config.DATABASE_NAME]
