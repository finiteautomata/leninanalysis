# coding: utf-8
import logging
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import legend

log = logging.getLogger('lenin')

def plot_year_vs_concept_value(values):
    """
        {
            1917: {"war" : 10.0, "revolution": 5.3 } ,
        }
    """
    years = np.array(sorted(map(int, values.keys())))
    print years
    y_concepts = defaultdict(list)
    for year in years: #esto da orden, sino no andaba
        word_values = values[year]
        for word, value in word_values.iteritems():
                y_concepts[word].append(value)

    for key, y_concept in y_concepts.iteritems():
        plt.plot(years, y_concept)

    legend(y_concepts.keys())

    ticks = np.arange(years.min(),years.max(), 1)
    labels = np.arange(years.min(),years.max(), 1)
    plt.xticks(ticks, labels)
    plt.title('Year vs Concept value')
    plt.xlabel('Year')
    plt.ylabel('Concept value')
    plt.show()