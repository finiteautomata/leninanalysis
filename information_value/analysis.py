import logging
import operator
import multiprocessing

from calculator import InformationValueCalculator, WindowSizeTooLarge
import config

# The amount of words that will be counted on the total sum

log = logging.getLogger('lenin')

SUM_THRESHOLD = config.SUM_THRESHOLD


class WindowAnalysis(object):
    def __init__(self, window_size, iv_words, number_of_words):
        self.window_size = window_size
        amount_to_be_taken = int(len(iv_words) * SUM_THRESHOLD) or 10
        sorted_words = sorted(iv_words.iteritems(), key=operator.itemgetter(1), reverse=True)[:amount_to_be_taken]
        self.max_iv = sorted_words[0][1]
        # Sum the reverse of sorted_words to improve numerical stability
        self.iv_sum = reduce(lambda x, y: x + y[1], reversed(sorted_words), 0)
        self.top_words = sorted_words[:number_of_words]

    def encode(self):
        return {
            "window_size": self.window_size,
            "top_words": self.top_words,
            "sum_iv": self.iv_sum,
            "max_iv": self.max_iv,
        }




# This global variable is shared across the threads
__information_value_calculator = None
__number_of_words = 20


def get_window_size_analysis(window_size):
    try:
        log.info("Checking window_size = %s" % window_size)
        iv_words = __information_value_calculator.information_value(window_size)
        return (window_size, WindowAnalysis(window_size, iv_words, number_of_words=__number_of_words))
    except WindowSizeTooLarge:
        return (window_size, None)


def get_all_analysis(tokens, window_sizes, number_of_words=20):
    global __information_value_calculator
    global __number_of_words
    __number_of_words = number_of_words
    __information_value_calculator = InformationValueCalculator(tokens)
    pool = multiprocessing.Pool(processes=config.NUMBER_OF_THREADS)
    return dict(pool.map(get_window_size_analysis, window_sizes))


def get_optimal_window_size(tokens, window_sizes, number_of_words=20, sum_threshold=config.SUM_THRESHOLD):
    results_per_window_size = get_all_analysis(tokens, window_sizes, number_of_words)
    #Criterio: maximo de promedio de IV sobre todas las palabras
    best_result = max(results_per_window_size.iteritems(),
        key= lambda res: res[1].iv_sum
        )

    return best_result
