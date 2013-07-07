import logging

from collections import Counter

from nltk.tokenize import wordpunct_tokenize

log = logging.getLogger('lenin')


class Segmentator(object):

    def __init__(self, document):
        self.document = document
        self.counter = Counter()

    def window_size(self):
        for sentence in wordpunct_tokenize(self.document.text):
            self.counter[len(sentence)] += 1
        log.debug(self.counter.most_common())
        return ( common[0] for common in self.counter.most_common() if common[0] > 1)
