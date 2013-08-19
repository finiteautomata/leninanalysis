import logging

from collections import Counter

from nltk.tokenize import wordpunct_tokenize

log = logging.getLogger('lenin')


class WindowsHardCodedSizeGenerator(object):

    def __init__(self, document):
        self.document = document
        self.counter = Counter()

    def window_size(self):
        return xrange(100, 10000 , 100) 
        #return ( common[0] for common in self.counter.most_common() if common[0] > 1)


class WindowsScaleGenerator(object):

  def __init__(self, document):
    self.document = document
    self.counter = Counter()
    
  def window_size(self):
        #10 a 33
        #20 a 40
        lower_limit = 10
        upper_limit = 33
        if self.document.total_tokens > 3000:
            lower_limit = 20
            upper_limit = 40
        scales = [ i *  0.01 for i in range(10 , 33)]
        
        return [ int(self.document.total_tokens * scale) for scale in scales ]
