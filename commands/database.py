import json
import logging

from pymongo.errors import DuplicateKeyError

from information_value.models import odm_session
from information_value.models import Document


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
