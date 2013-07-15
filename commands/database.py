import json
import logging

from pymongo.errors import DuplicateKeyError

from information_value.models import odm_session
from information_value.models import Document
from includes.tokenizer import tokenize
from includes.segmentator import Segmentator
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


def calculate_results():
    for document in Document.query.find().all():
        log.info("Calculating information values for document %s" % document.name)
        document.tokenizer = tokenize
        segmentator = Segmentator(document)
        window_sizes = segmentator.window_size()
        results = get_all_analysis(document, window_sizes, number_of_words=5000)


def cleandb():
    from pymongo import MongoClient
    client = MongoClient()
    db = client.lenin
    db.drop_collection('document')
    db.drop_collection('information_value_result')
