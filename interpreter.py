#! coding utf-8
"""
  Run this before opening a console
"""
from ming import Session
from ming.odm import ODMSession
import ming
import config
import logging


ming_config = {'ming.document_store.uri': config.DATABASE_URL}
ming.configure(**ming_config)

from information_value.models import Document, DocumentList, InformationValueResult, doc_for
from analyzers.synset_analyzer import SynsetAnalyzer
from nltk.corpus import wordnet as wn
from analyzers import similarity

from pymongo import MongoClient

def init_logging():
    logger = logging.getLogger('lenin')
    logger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('lenin.log')
    fh.setLevel(logging.INFO)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

init_logging()

client = MongoClient()
db = client[config.DATABASE_NAME]

session = Session.by_name('document_store')
odm_session = ODMSession(doc_session=session)
