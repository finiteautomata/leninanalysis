import multiprocessing
import operator
from calculator import InformationValueCalculator, WindowSizeTooLarge

class WindowAnalysis(object):
    def __init__(self, window_size, iv_words, number_of_words):
        self.window_size = window_size
        sorted_words = sorted(iv_words.iteritems(), key=operator.itemgetter(1), reverse=True)
        self.max_iv = sorted_words[0][1]
        # Sum the reverse of sorted_words to improve numerical stability
        self.iv_sum = reduce(lambda x,y: x+y[1], reversed(sorted_words), 0)
        self.iv_average = self.iv_sum / len(sorted_words)
        self.top_words = sorted_words[:20],



# This global variable is shared across the threads
information_value_calculator = None
number_of_words = 20


def get_window_size_analysis(window_size):
    try:
        print "Probando window_size = %s" % window_size
        iv_words = information_value_calculator.information_value(window_size)
        return (window_size, WindowAnalysis(window_size, iv_words, number_of_words))
    except WindowSizeTooLarge as e:
        return (window_size, None)

def get_all_analysis(tokens, window_sizes, number_of_words=20):
    global information_value_calculator
    information_value_calculator = InformationValueCalculator(tokens)
    pool = multiprocessing.Pool(processes=5)
    return dict(pool.map(get_window_size_analysis, window_sizes))

def get_optimal_window_size(tokens, window_sizes, number_of_words=20):
    results_per_window_size = get_all_analysis(tokens, window_sizes, number_of_words)
    
    #Criterio: maximo de promedio de IV sobre todas las palabras
    best_result = max(results_per_window_size.iteritems(),
        key= lambda res: res[1].max_iv
        )
    
    return best_result
