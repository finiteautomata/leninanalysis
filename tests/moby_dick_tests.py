from __future__ import division
import logging
from nose.plugins.attrib import attr
from unittest import TestCase
from nltk.corpus import gutenberg
from includes.tokenizer import tokenize
from information_value.analysis import get_optimal_window_size

log= logging.getLogger('lenin')

class MobyDickTests(TestCase):
    window_sizes = xrange(100, 3000, 100)
    sum_threshold = 0.01

    @attr('slow')
    def test_top_words_for_moby_dick(self):
        tokens = get_moby_dick_tokens()
        # This are the words that Zanette show up as the result of analysis
        zanette_top_words = ["i", "whale", "you", "ahab", "is",
                     "ye", "queequeg", "thou", "me", "of",
                     "he", "captain", "boat", "the", "stubb",
                     "his", "jonah", "was", "whales", "my"]

        window_size, analysis = get_optimal_window_size(tokens, self.window_sizes, 20, sum_threshold=self.sum_threshold)
        top_words = [word for (word, iv_value) in analysis.top_words]
        
        log.info("Window size = %s" % window_size)
        log.info("top words = %s" % top_words)
        log.info("zanette words = %s" % zanette_top_words)

        amount_of_matching_words = len([word for word in zanette_top_words if word in top_words])
        self.assertGreaterEqual(amount_of_matching_words, 15)


def get_moby_dick_tokens():
    moby_dick = gutenberg.raw('melville-moby_dick.txt')
    tokens = tokenize(moby_dick, only_alphanum=True, clean_punctuation=True)
    return [token.lower() for token in tokens]
