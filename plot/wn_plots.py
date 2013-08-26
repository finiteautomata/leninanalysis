# coding: utf-8
import operator
import logging
from operator import itemgetter
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import legend
from scipy import average

import config
from information_value.models import Document
from information_value.models import DocumentList
log = logging.getLogger('lenin')

def plot_year_vs_concept_value(values):
    """
        {
            1917: {"war" : 10.0, "revolution": 5.3 } ,
        }
    """

    x = sorted(map(int, values.keys()))
    print x
    y_concepts = defaultdict(list)
    for year in x: #esto da orden, sino no andaba
    #for year, word_values in values.iteritems():
        word_values = values[year]
        for word, value in word_values.iteritems():
            y_concepts[word].append(value)

    for key, y_concept in y_concepts.iteritems():
        plt.plot(x, y_concept, '-o')

    legend(y_concepts.keys())

    ticks = np.arange(1899,1924, 6)
    labels = np.arange(1899,1924, 6)
    plt.xticks(ticks, labels)
    plt.title('Year vs Concept value')
    plt.xlabel('Year')
    plt.ylabel('Concept value')
    plt.show()
