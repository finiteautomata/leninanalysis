# coding: utf-8
import operator
import logging
import matplotlib.pyplot as plt
from scipy import average

from information_value.models import Document
log = logging.getLogger('lenin')


# Scatter plot de X los window sizes y en Y las palabras totales
def plot_scatter_total_words_vs_window_sizes(documents):
    window_sizes = []
    total_words = []
    for document in documents:
        best_iv = document.get_information_value_result()
        if best_iv:
            window_sizes.append(best_iv.window_size)
            total_words.append(len(document.text))

    plt.scatter(window_sizes, total_words, label="Best window size with total words for each text")
    plt.xlabel("Best Window Size")
    plt.ylabel("Total words")
    plt.show()

    log.debug("Best window size = %s" % max(window_sizes))
    log.debug("Max total words = %s" % max(total_words))
    log.debug("Average window size = %s" % average(window_sizes))


def get_max_ivs(documents):
    res = []
    document_with_results = []
    for document in documents:
        for result in document.results:
            sorted_words = sorted(result.iv_words.iteritems(), key=operator.itemgetter(1), reverse=True)
            for word in sorted_words:
                res.append(word[1])
                document_with_results.append(document)
    # we need to return docs and res in order for plotting!
    return document_with_results, res


def plot_histogram_of_max_ivs(documents):
    ivs = get_max_ivs(documents)[1]
    if ivs == []:
        log.debug("Empty results. please execute ./cccp --calculate-results")
        return
    plt.hist(ivs)
    plt.title("Histogram of Maximum information value per work")
    plt.show()

    log.debug("Average max iv of all works = %s" % average(ivs))


def plot_histogram_of_max_ivs_of_long_works(documents):
    long_works = filter(lambda document: len(document.text) > 5000, documents)
    long_ivs = get_max_ivs(long_works)[1]
    if long_ivs == []:
        log.debug("Empty results. please execute ./cccp --calculate-results")
        return

    plt.hist(long_ivs)
    plt.title("Histogram of Maximum Information Value for Long Works")
    plt.show()
    log.debug("Average max iv of long works = %s" % average(long_ivs))


def plot_scatter_max_ivs_vs_total_words(works):
    documents_with_results, ivs = get_max_ivs(works)
    total_words = map(lambda doc: len(doc.text), documents_with_results)
    if ivs == []:
        log.debug("Empty results. please execute ./cccp --calculate-results")
        return

    plt.scatter(total_words, ivs)
    plt.title("Maximum IV per word vs Total Words")
    plt.xlabel("Total words")
    plt.ylabel("Maximum Information Value")
    plt.show()

    log.debug("Average max iv = %s" % average(ivs))


def plot_scatter_max_ivs_vs_window_sizes(documents):
    ivs = get_max_ivs(documents)[1]
    window_sizes = [iv.window_size for iv in ivs]
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
    documents = list(Document.query.find())#{'year': { "$gte" : MIN_YEAR, "$lt": MAX_YEAR }}))
    plot_scatter_total_words_vs_window_sizes(documents)
    plot_information_value_things(documents)


def plot_xy(x_label, x, y_label, y):
    #works = filter(lambda w: w['total_words'] < 500, works)
    #works = filter(lambda w: w['best_window_size'] < 100, works)

    plt.scatter(x, y, label=(x_label+" vs "+y_label))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()

def plot_scale_vs_information(documents):
    for index, document in enumerate(documents):
        x = []; y= []
        #TODO        sorted_results =
        for result in document.results:
            x.append(result.window_size)
            iv_sum = sum(sorted(map(operator.itemgetter(1), result.iv_words), reverse=True))
            y.append(iv_sum)
        plt.plot(x, y, 'o')
        plt.title('Document: %s' % document.name)
        plt.ylabel('Information [bits/word]')
        plt.xlabel('Scale [words]')
        plt.show()


def plot_len_vs_most_informative(documents=None):
    if documents is None:
        documents = Document.query.find().all()
    x = []; y = []
    for document in documents:
        x.append(len(document.tokens))
        y.append(document.get_information_value_result().window_size)

    plt.plot(x, y, 'o')
    plt.title('All text in Database')
    plt.ylabel('Most informative scale [words]')
    plt.xlabel('Text length [words]')
    plt.show()
