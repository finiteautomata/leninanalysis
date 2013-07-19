# This Python file uses the following encoding: utf-8
from __future__ import division
import logging
import sys
from pymongo import MongoClient
# This hack is to replace config module with the other config...
from moby_dick import config as moby_dick_config
sys.modules["config"] = moby_dick_config

from nose.plugins.attrib import attr
from unittest import TestCase
from nltk.corpus import gutenberg
from includes.tokenizer import tokenize
from information_value.analysis import get_optimal_window_size
from information_value.models import Document
from information_value.models import odm_session



log= logging.getLogger('lenin')

class MobyDickTests(TestCase):
    window_sizes = xrange(100, 3000, 100)
    sum_threshold = 0.01

    def setUp(self):
        client = MongoClient()
        client.drop_database('moby_dick')

    @attr('slow')
    def test_top_words_for_moby_dick(self):
        document = get_moby_dick_document()
        
        # This are the words that Zanette show up as the result of analysis
        zanette_top_words = ["i", "whale", "you", "ahab", "is",
                     "ye", "queequeg", "thou", "me", "of",
                     "he", "captain", "boat", "the", "stubb",
                     "his", "jonah", "was", "whales", "my"]
        window_size, analysis = get_optimal_window_size(document, self.window_sizes, 20, sum_threshold=self.sum_threshold)
        top_words = [word for (word, iv_value) in analysis.top_words]

        log.info("Window size = %s" % window_size)
        log.info("top words = %s" % top_words)
        log.info("zanette words = %s" % zanette_top_words)

        amount_of_matching_words = len([word for word in zanette_top_words if word in top_words])
        self.assertGreaterEqual(amount_of_matching_words, 15)


def get_moby_dick_document():
    moby_dick = gutenberg.raw('melville-moby_dick.txt')
    document = Document(
        url = 'melville-moby_dick.txt',
        name = 'Moby dick',
        text = moby_dick,
        month = 'Oct',
        year = '1851'
    )
    # document uses tokenizer func for create tokens, since we need to enforce
    # only_alphanum and clean_punct we need a wrapper
    def tokenizer_wrapper(raw_text):
        return map(str.lower, tokenize(raw_text, only_alphanum=True, clean_punctuation=True))
    document.tokenizer = tokenizer_wrapper

    odm_session.flush()
    
    return document
