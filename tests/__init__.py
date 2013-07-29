import logging
import sys
# This hack is to replace config module with the other config...
from tests import config as test_config
sys.modules["config"] = test_config
import config
import unittest
from pymongo import MongoClient

def init_logging():
    logger = logging.getLogger('lenin')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('test.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)


init_logging()

class LeninTestCase(unittest.TestCase):
    def setUp(self):
        init_logging()
        client = MongoClient()
        print config.DATABASE_NAME
        client.drop_database(config.DATABASE_NAME)
