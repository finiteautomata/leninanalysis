#! coding: utf-8
import sys
import json
import inspect
import logging

from pymongo.errors import DuplicateKeyError

from information_value.models import odm_session
from information_value.models import Document
from information_value.models import DocumentList
from includes.tokenizer import tokenize
import includes.ws_generator
from information_value.analysis import get_all_analysis


log = logging.getLogger('lenin')


def populate_database():
    log.info("Populating database...")
    with file('lenin_work.json') as f:
        raw_works = json.load(f)
        log.info("Inserting %s works to database..." % (len(raw_works)))
        for raw_work in raw_works:
            try:
                Document(
                    url=raw_work['url'],
                    text=raw_work['text'],
                    name=raw_work['name'],
                    month=raw_work['month'],
                    year=raw_work['year']
                )
                odm_session.flush()
            except DuplicateKeyError:
                log.info("Duplicate found skipping...")
        log.info("Done")

def _get_windows_size_generators(class_name):
  # used for search classes by name in ws_generator
  res = []
  for name, obj in inspect.getmembers(sys.modules['includes.ws_generator']):
    if inspect.isclass(obj):
        if name == class_name:
            return obj

def calculate_results(documents=None, window_size_algorithm='WindowsHardCodedSizeGenerator', store_only_best = False):
  algorithm_class = _get_windows_size_generators(window_size_algorithm)
  if documents is None:
      documents = Document.query.find().all()
  log.info("Selected window size generator %s" % window_size_algorithm)
  i = 1
  for document in documents:
    log.info("Calculating information values for document %s (%i/%i)" % (document.name, i,len(documents)))
    i = i+1

    
    if document.text:
        document.tokenizer = tokenize
        win_size_generator = algorithm_class(document)
        window_sizes = win_size_generator.window_size()
        get_all_analysis(document, window_sizes, number_of_words=5000)
        if store_only_best:
          _delete_non_best_analysis(document, window_sizes)

def _delete_non_best_analysis(document, window_sizes):
  best_res = document.get_information_value_result()
  log.info("Best window size for %s: %s" % (document.name, best_res.window_size))
  log.info("Removing other results from mongo")
  for one_res in document.results:
    if one_res.window_size !=  best_res.window_size:
      log.info("Removing window size %s" % one_res.window_size)
      one_res.delete()
  log.info("Flushing")
  odm_session.flush()

def reset_senses():
  log.info("Resetting all senses")
  for doc in Document.query.find():
    doc.related_sense = {}
  odm_session.flush()
