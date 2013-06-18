from __future__ import division
import logging
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
window_sizes = xrange(100, 6000, 100)
sum_thresholds = [0.0005, 0.001, 0.002, 0.003, 0.005, 0.006, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.2, 0.3 ]


def load_moby_dick_analysis():
    tokens = get_moby_dick_tokens()
    text = gutenberg.raw('melville-moby_dick.txt')
    try:
        moby_dick_doc = Document(
            url='gutenberg',
            name='moby dick',
            text=text,
            month='Jan',
            year=1851
            )
        odm_session.flush()
    except DuplicateKeyError:
        moby_dick_doc = Document.query.get(name='moby dick')

    for sum_threshold in sum_thresholds:
        log.info("Trying analysis for threshold = %s" % sum_threshold)
        window_size, analysis = get_optimal_window_size(tokens, window_sizes, 20, sum_threshold=sum_threshold)
        anal_dict = analysis.encode()
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
