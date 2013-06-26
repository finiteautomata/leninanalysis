import json
import logging

from pymongo.errors import DuplicateKeyError

from information_value.models import odm_session
from information_value.models import Document
from includes.tokenizer import tokenize
from information_value.analysis import get_all_analysis
from information_value.models import InformationValueResult


log= logging.getLogger('lenin')


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
                    year=int(raw_work['year'])
                )
                odm_session.flush()
            except DuplicateKeyError:
                log.info("Duplicate found skipping...")
        log.info("Done")

def calculate_results():
    log.info("Calculating information values...")
    for document in Document.query.find().all():
        tokens = tokenize(document.text)
        window_sizes = xrange(100, 3000, 100)
        results = get_all_analysis(tokens, window_sizes, number_of_words=5000)
        for result in results.iteritems():
            print result
            log.info("Storing results for document %s..." % document.name)
            analisys = result[1]
            if analisys:
                print analisys.top_words
                InformationValueResult(
                    window_size=result[0],
                    iv_words = analisys.top_words,
                    document= document,
                    )
            odm_session.flush()
