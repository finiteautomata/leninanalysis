# coding: utf-8
from information_value.models import Document
import config
import matplotlib.pyplot as plt
from scipy import average

JSON_SUBSET_NAME = "lenin_work.subset.json"
MIN_YEAR = config.MIN_YEAR
MAX_YEAR = config.MAX_YEAR


# Scatter plot de X los window sizes y en Y las palabras totales
def plot_scatter_total_words_vs_window_sizes(documents):
    window_sizes = [getattr(document.get_information_value_result(0.01), 'window_size', 0) for document in documents]
    total_words = [len(document.text) for document in documents]
    print 'win %s total %s' % (len(window_sizes), len(total_words))
    plt.scatter(window_sizes, total_words, label="Best window size with total words for each text")
    plt.xlabel("Best Window Size")
    plt.ylabel("Total words")
    plt.show()


    print "Best window size = %s" % max(window_sizes)
    print "Max total words = %s" % max(total_words)
    print "Average window size = %s" % average(window_sizes)


def get_max_ivs(documents):
    res = []
    for document in documents:
        for result in document.results:
            res.append(result.iv_words[0][1])
    #return [work['top_words_with_iv'][0][1] for work in works]
    return res


def plot_histogram_of_max_ivs(documents):
    ivs = get_max_ivs(documents)

    plt.hist(ivs)
    plt.title("Histogram of Maximum information value per work")
    plt.show()

    print "Average max iv of all works = %s" % average(ivs)


def plot_histogram_of_max_ivs_of_long_works(documents):
    long_works = filter(lambda document: len(document.text) > 5000, documents)
    long_ivs = get_max_ivs(long_works)

    plt.hist(long_ivs)
    plt.title("Histogram of Maximum Information Value for Long Works")
    plt.show()
    print "Average max iv of long works = %s" % average(long_ivs)


def plot_scatter_max_ivs_vs_total_words(works):
    ivs = get_max_ivs(works)
    total_words = [len(work.text) for work in works]

    plt.scatter(total_words, ivs)
    plt.title("Maximum IV per word vs Total Words")
    plt.xlabel("Total words")
    plt.ylabel("Maximum Information Value")
    plt.show()

    print "Average max iv = %s" % average(ivs)

def plot_scatter_max_ivs_vs_window_sizes(works):
    window_sizes = [document.get_information_value_result(0.01).window_size for document in documents]
    ivs = get_max_ivs(works)

    plt.scatter(window_sizes, ivs)
    plt.title("Maximum IV per word vs Best Window Size")
    plt.xlabel("Best Window Size")
    plt.ylabel("Maximum Information Value per word")
    plt.show()

#Plots histogram of information values from the top words of the works
def plot_information_value_things(works):
    plot_histogram_of_max_ivs(works)
    plot_histogram_of_max_ivs_of_long_works(works)
    plot_scatter_max_ivs_vs_total_words(works)
    plot_scatter_max_ivs_vs_window_sizes(works)

def plot_iv_things():
    #works = utils.load_ivs(MIN_YEAR, MAX_YEAR-1)
    works = list(Document.query.find({'year': { "$gte" : MIN_YEAR, "$lt": MAX_YEAR }}))
    plot_scatter_total_words_vs_window_sizes(works)
    plot_information_value_things(works)


def plot_xy(x_label, x,y_label, y):
    #works = filter(lambda w: w['total_words'] < 500, works)
    #works = filter(lambda w: w['best_window_size'] < 100, works)


    points = zip(x, y)
    plt.scatter(x, y, label=(x_label+" contra "+y_label))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
