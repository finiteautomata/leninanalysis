from __future__ import division
import logging
import sys
# This hack is to replace config module with the other config...
from moby_dick import config as moby_dick_config
sys.modules["config"] = moby_dick_config

from nltk.corpus import gutenberg
from pymongo.errors import DuplicateKeyError
from cccp import init_logging
from includes.tokenizer import tokenize
from information_value.analysis import get_optimal_window_size
from information_value.models import odm_session
from information_value.models import InformationValueResult
from information_value.models import Document




log= logging.getLogger('lenin')
init_logging()
window_sizes = xrange(1000, 6000, 1000)
#sum_thresholds = [0.0005, 0.001, 0.002, 0.003, 0.005, 0.006, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.3 ]
sum_thresholds = [0.001]

def load_moby_dick_analysis():
    
    tokens = get_moby_dick_tokens()
    text = gutenberg.raw('melville-moby_dick.txt')
    try:
        moby_dick_doc = Document(
            url='gutenberg',
            name='moby dick',
            text=text,
            month='Jan',
            year='1851'
            )
        odm_session.flush()
    except DuplicateKeyError:
        moby_dick_doc = Document.query.get(name='moby dick')

    for sum_threshold in sum_thresholds:
        log.info("Trying analysis for threshold = %s" % sum_threshold)
        analysis = get_optimal_window_size(tokens, window_sizes, 20, sum_threshold=sum_threshold)[1]
        anal_dict = analysis.encode()
        window_size = anal_dict['window_size']

        log.debug("Best result = %s" % window_size)
        InformationValueResult(
            window_size = window_size,
            threshold = sum_threshold,
            document = moby_dick_doc,
            iv_words = anal_dict['top_words'],
            max_iv = anal_dict['max_iv'],
            sum_iv = anal_dict['sum_iv']
        )
        odm_session.flush()


def get_moby_dick_tokens():
    moby_dick = gutenberg.raw('melville-moby_dick.txt')
    tokens = tokenize(moby_dick, only_alphanum=True, clean_punctuation=True)
    return [token.lower() for token in tokens]

if __name__ == '__main__':
    load_moby_dick_analysis()
