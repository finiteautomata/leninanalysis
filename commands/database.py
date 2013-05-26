import json
from pymongo import MongoClient

client = MongoClient()
db = client.lenin_database


def populate_database():
    print "Populating database..."
    works = db.works
    with file('lenin_work.json') as f:
        raw_works = json.load(f)
        print "Inserting %s works to database..." % (len(raw_works))
        for raw_work in raw_works:
            works.insert(raw_work)
        print "Done"

