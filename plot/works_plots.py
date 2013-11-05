# coding: utf-8
from interpreter import *
import operator
import logging
import matplotlib.pyplot as plt
from information_value.models import Document

log = logging.getLogger('lenin')


def plot_length_histogram(docs, title, **kwargs):
    num_tokens = [doc.number_of_words for doc in docs]
    plt.title(title)
    plt.xlabel("Number of words")
    plt.ylabel("Amount of works")
    plt.hist(num_tokens, **kwargs)


def plot_small_documents():
    docs = Document.query.find({'number_of_words': {'$gte': 2000, '$lte': 20000}})
    plot_length_histogram(
        docs,
        bins=9,
        range=(2000, 20000),
        title="Histogram for works with <20k words")


def plot_big_documents():
    docs = Document.query.find({'number_of_words': {'$gte': 20000}})
    plot_length_histogram(
        docs,
        range=(20000, 140000),
        title="Histogram for works with >20k words",
        bins=12)


def plot_tokens_per_year():
    data = db.document.aggregate([
        {"$group": {"_id": "$year", "number_of_works": {"$sum": 1}}}
    ])['result']
    data = sorted(data, key=lambda x: int(x["_id"]))
    years = map(lambda x: int(x["_id"]), data)
    number_of_works = map(operator.itemgetter("number_of_works"), data)

    plt.title("Number of works per year")
    plt.plot(years, number_of_works)


BASE_DIR = "paper/figures/"


def plot_all():
    plot_small_documents()
    plt.savefig(BASE_DIR + "hist_tokens_small_works.eps")
    plt.close()

    plot_big_documents()
    plt.savefig(BASE_DIR + "hist_tokens_big_works.eps")
    plt.close()

    plot_tokens_per_year()
    plt.savefig(BASE_DIR + "tokens_per_year.eps")
    plt.close()
