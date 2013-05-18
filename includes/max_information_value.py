# This Python file uses the following encoding: utf-8  
import operator
from copy import deepcopy
from information_value import InformationValueCalculator, WindowSizeTooLarge


def get_top_words(tokens, window_size, number_of_words):
    iv_calculator = InformationValueCalculator(tokens)
    information_value = iv_calculator.information_value(window_size)
    sorted_words = sorted(information_value.iteritems(), key=operator.itemgetter(1), reverse=True)
    

    res = {
            'window_size' : window_size,
            'iv_per_word': sorted_words[0][1],
            'top_words': sorted_words
    }

    return res



def get_results(tokens, window_sizes, number_of_words=20):
    results = {}
    results['ivs'] = [] 
    results['tried_windows'] = []
    ivs = {}

    
    window_sizes = set(window_sizes)

    for window_size in window_sizes:
        try:
            print "Probando tamaño de ventana = %s" % window_size
            res = get_top_words(tokens, window_size)
            ivs[window_size] = res['top_words'][0][1]
            if window_size >= 1:
                results['ivs'].append(res)
                results['tried_windows'].append(window_size)
        except WindowSizeTooLarge as e:
            # La ventana es demasiado grande => salir!
            break
    #Criterio: maximo de promedio de IV sobre todas las palabras
    results['best_window_size'] = max(ivs, key=ivs.get)
    results['best_iv_per_word'] = ivs[results['best_window_size']]
    for res in results['ivs']:
        if res['window_size'] == results['best_window_size']:
            results['top_words'] = res['top_words']
            if 'scale' in res.keys():
                results['best_scale'] = res['scale']
            break
    
    results.pop("ivs", None)
    return results
