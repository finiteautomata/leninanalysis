import string
import logging
from collections import defaultdict
from random import random

import networkx as nx
from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt
from nltk.corpus import wordnet_ic


from analyzers import similarity
from interpreter import Document
from analyzers.document_analyzer import DocumentAnalyzer

SIMILARITY_FUNCS = similarity.functions

log = logging.getLogger('lenin')

CORPUS = wordnet_ic.ic('ic-brown.dat')

SYNSETS = [wn.synset(word) for word in [
           "war.n.01",
           "capitalism.n.01",
           "theory.n.01",
           "toilet.n.04",
           "imperialism.n.02",
           "proletarian.n.01",
           "practice.n.03",
           "revolution.n.01",
           "money.n.01",
           "philosophy.n.02",
           "idealism.n.01",
           "strategy.n.02",
           "materialism.n.02",
           "lion.n.01",
           "television_receiver.n.01",
           "hair.n.01",
           "sugar.n.01",
           "car.n.01"]]

ANALYZERS = [DocumentAnalyzer(synsets=SYNSETS, similarity_function=sim_fun) for sim_fun in SIMILARITY_FUNCS]


def default_document_list():
    state_and_revolution = Document.query.find({"name": {"$regex": "State and Revolution"}}).next()
    imperialism_capitalism = Document.query.find({"name": {"$regex": "Imperialism.*Capitalism.*"}}).next()
    materialism_criticism = Document.query.find({"name": "Lenin: MATERIALISM and EMPIRIO-CRITICISM"}).next()
    what_is_to_be_done = Document.query.find({"name": {"$regex": ".*What Is To Be Done.*"}}).next()
    agrarian_programme = Document.query.find({"name": u'Lenin: The Agrarian Programme of Social-Democracy in the First Russian Revolution, 1905-1907'}).next()
    return [state_and_revolution, imperialism_capitalism, materialism_criticism, what_is_to_be_done, agrarian_programme]


def clean_name(name):
    return name.replace(' ', '_').replace(':', '').replace(',', '').replace('.', '_').replace('/', '_').lower()


def create_top_sense_tables(doc_list):
    documents = doc_list
    if documents is None:
        documents = default_document_list()

    log.info("Top words")
    log.info("=" * 80)
    for document in documents:
        log.info("=" * 80)
        log.info(document.name)
        try:
            for word, _ in document.top_words():
                log.info(word)
        except AttributeError:
            log.exception("No top words found. Trying to calculate them.")

        with open("paper/top_senses_%s.tex" % clean_name(document.name), "w") as tex_table:
            tex_table.write("""
    \\begin{center}
      \\begin{tabular}{ | l | l | l | }
        \hline
        \multicolumn{3}{|c|}{%s} \\\\ \hline
        \# & Word  \\\\ \hline\n""" % document.name[:30])
            top_senses = document.top_senses()
            last = len(top_senses)
            for index, sense in enumerate(top_senses, start=1):
                log.info("Sense %s --  %s " % (string.rjust(sense.name, 35), string.rjust(sense.definition, 55)))
                tex_table.write("%s & %s & %s \\\\ \hline" % (index, string.rjust(sense.name, 35).split('.')[0].strip().replace('_', '\_'), sense.definition))
                if index != last:
                    tex_table.write("\n")

            tex_table.write("""\end{tabular}\n\end{center}""")


def create_analysis_tables(doc_list):

    documents = doc_list
    if documents is None:
        documents = default_document_list()

    for doc in documents:
        full_analysis = {}
        for analyzer in ANALYZERS:
            analysis = analyzer.analyze_document(doc)
            sorted_words = sorted(analysis.iteritems(), key=lambda(word, similarity): similarity, reverse=True)
            log.info("=" * 30)
            full_analysis[analyzer.name] = []
            log.info('NAME ', analyzer.name)
            for synset, similarity in sorted_words:
                log.info("%s %s  --  %s " % (string.rjust(synset, 25),
                                             string.rjust(str(similarity), 25),
                                             string.rjust(analyzer.best_word_for[synset].name, 25)))
                full_analysis[analyzer.name].append((synset,
                                                    str(similarity),
                                                    analyzer.best_word_for[synset].name,
                                                    analyzer.best_word_for[synset].definition))

        doc_name = doc.name.replace(' ', '_').replace(':', '').replace(',', '').lower()[:30]
        with open('paper/analysis_%s.tex' % (clean_name(doc_name)), 'w') as analysis_output:
            analysis_output.write("""
    \\begin{center}
      \\begin{tabular}{ | l | l | l |}
        \hline
        Choosen Sensens & Closest Top Sense & similarity  \\\\ \hline\n""")
            for key in full_analysis.keys():
                analysis_output.write("\multicolumn{3}{|c|}{%s - %s} \\\\ \hline\n" % (doc.name[:30], key.replace('_', ' ')))
                for value in full_analysis[key]:
                    analysis_output.write("%s & %s & %s\\\\ \hline\n" % (value[0].replace('_', ' '), value[2].replace('_', ' '), value[1].replace('_', ' ')))
                    #analysis_output.write("%s & %s & %s & %s\\\\ \hline\n" % (value[0].replace('_', ' '), value[2].replace('_', ' '), value[1].replace('_', ' '), value[3].replace('_', ' ')))
            analysis_output.write("""\end{tabular}\n\end{center}""")


def create_graphs(doc_list):
    documents = doc_list
    if documents is None:
        documents = default_document_list()

    distance_functions = [
        (wn.lch_similarity(SYNSETS[0], SYNSETS[0]), 'lch', lambda sense_1, sense_2: wn.lch_similarity(sense_1, sense_2)),
        (1.0, 'lin', lambda sense_1, sense_2: wn.lin_similarity(sense_1, sense_2, CORPUS)),
        (10.636958516573292, 'res', lambda sense_1, sense_2: wn.res_similarity(sense_1, sense_2, CORPUS)),
        (wn.jcn_similarity(SYNSETS[0], SYNSETS[0], CORPUS), 'jcn', lambda sense_1, sense_2: wn.jcn_similarity(sense_1, sense_2, CORPUS)),
        (1.0, 'path', lambda sense_1, sense_2: wn.path_similarity(sense_1, sense_2)),
    ]
    all_senses = []
    for doc in documents:
        for sense in doc.top_senses():
            all_senses.append((sense, doc.name))
    against_colors = ['r', 'b', 'g']
    against_to = [wn.synset(word) for word in ["economy.n.01", "philosophy.n.02", "politics.n.01"]]
    create_against_graph('phyl_eco_pol', documents, all_senses, against_to, distance_functions, against_colors)

    against_to = SYNSETS

    against_colors = [(random(), random(), random()) for _i in range(0, len(SYNSETS))]
    create_against_graph('handpicked', documents, all_senses, against_to, distance_functions, against_colors)

    create_graph_top_senses(documents, all_senses, distance_functions)


def create_against_graph(file_prefix, documents, all_senses, against_to, distance_functions, against_colors):
    doc_senses = defaultdict(list)
    node_list_against_to = [sense.name for sense in against_to]

    for sense, doc_name in all_senses:
        #this is used for give colors that corresponds to each document
        doc_senses[doc_name].append(sense.name)

    for max_value, function_name, distance_function in distance_functions:
        G = nx.Graph()
        for sense, doc_name in all_senses:
            G.add_node(sense.name)
        for node_against_name in node_list_against_to:
            G.add_node(node_against_name)

        for sense_1, doc_name in all_senses:
            for sense_2 in against_to:
                if sense_1 != sense_2:
                    G.add_edge(sense_1.name, sense_2.name, weight=max_value - distance_function(sense_1, sense_2))

        pos = nx.spring_layout(G, iterations=50)
        # lets put the colors for each doc
        colors = [(random(), random(), random()) for _i in range(0, len(doc_senses.keys()))]
        for index, doc_name in enumerate(doc_senses):
            nx.draw_networkx_nodes(G, pos, node_size=60, linewidths=0, nodelist=doc_senses[doc_name], node_color=colors[index])
        for index, sense_name in enumerate(node_list_against_to):
            nx.draw_networkx_nodes(G, pos, node_size=120, linewidths=0, nodelist=[sense_name], node_color=against_colors[index])

        G.clear()
        #plt.axis('off')
        plt.savefig("paper/%s_%s_sim_graph.png" % (file_prefix, function_name))  # save as png
        plt.show()  # display
        plt.clf()


def create_graph_top_senses(documents, all_senses, distance_functions):
    doc_senses = defaultdict(list)

    for sense, doc_name in all_senses:
        doc_senses[doc_name].append(sense.name)

    for max_value, function_name, distance_function in distance_functions:
        G = nx.Graph()
        for sense, doc_name in all_senses:
            G.add_node(sense.name)
            G.add_node(sense.name)

        for sense_1, doc_name in all_senses:
            for sense_2, doc_name in all_senses:
                if sense_1 != sense_2:
                    G.add_edge(sense_1.name, sense_2.name, weight=max_value - distance_function(sense_1, sense_2))

        pos = nx.spring_layout(G, iterations=50)
        colors = [(random(), random(), random()) for _i in range(0, len(doc_senses.keys()))]
        for index, doc_name in enumerate(doc_senses.keys()):
            nx.draw_networkx_nodes(G, pos, node_size=60, linewidths=0, nodelist=doc_senses[doc_name], node_color=colors[index])
        G.clear()
        plt.savefig("paper/%s_sim_graph.png" % function_name)  # save as png
        plt.show()  # display
        plt.clf()


def create_tables(doc_list):
#    create_top_sense_tables(doc_list)
    create_analysis_tables(doc_list)
#    create_graphs(doc_list)
