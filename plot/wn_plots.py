# coding: utf-8
import operator
import logging
from operator import itemgetter
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt



from matplotlib.pyplot import legend
from scipy import average
from scipy.interpolate import spline

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

    years = np.array(sorted(map(int, values.keys())))
    print years
    y_concepts = defaultdict(list)
    for year in years: #esto da orden, sino no andaba
    #for year, word_values in values.iteritems():
        word_values = values[year]
        for word, value in word_values.iteritems():
            #if value > 0.2:
                y_concepts[word].append(value)
            #else:
            #    y_concepts[word].append(0.0)

    for key, y_concept in y_concepts.iteritems():

        #xnew = np.linspace(years.min(),years.max(),300)
        #y_concept_smooth = spline(years,y_concept,xnew)        
        #plt.plot(xnew, y_concept_smooth)
        plt.plot(years, y_concept)

    legend(y_concepts.keys())

    ticks = np.arange(years.min(),years.max(), 1)
    labels = np.arange(years.min(),years.max(), 1)
    plt.xticks(ticks, labels)
    plt.title('Year vs Concept value')
    plt.xlabel('Year')
    plt.ylabel('Concept value')
    plt.show()