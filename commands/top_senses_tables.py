import string
import logging

from analyzers import similarity
from interpreter import Document, wn
from analyzers.document_analyzer import DocumentAnalyzer

SIMILARITY_FUNCS = similarity.functions

log = logging.getLogger('lenin')

synsets = [wn.synset(word) for word in [
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


def document_list():
    state_and_revolution = Document.query.find({"name": {"$regex": "State and Revolution"}}).next()
    imperialism_capitalism = Document.query.find({"name": {"$regex": "Imperialism.*Capitalism.*"}}).next()
    materialism_criticism = Document.query.find({"name": "Lenin: MATERIALISM and EMPIRIO-CRITICISM"}).next()
    what_is_to_be_done = Document.query.find({"name": {"$regex": ".*What Is To Be Done.*"}}).next()
    agrarian_programme = Document.query.find({"name": u'Lenin: The Agrarian Programme of Social-Democracy in the First Russian Revolution, 1905-1907'}).next()
    return [state_and_revolution, imperialism_capitalism, materialism_criticism, what_is_to_be_done, agrarian_programme]


def create_top_sense_tables():
    documents = document_list()
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

        with open("paper/top_senses_%s.tex" % document.name.replace(' ', '_').replace(':', '').replace(',', '').lower(), "w") as tex_table:
            tex_table.write("""
    \\begin{center}
      \\begin{tabular}{ | l | l | }
        \hline
        \multicolumn{2}{|c|}{%s} \\\\ \hline
        \# & Word  \\\\ \hline\n""" % document.name[:30])
            top_senses = document.top_senses()
            last = len(top_senses)
            for index, sense in enumerate(top_senses, start=1):
                log.info("Sense %s --  %s " % (string.rjust(sense.name, 35), string.rjust(sense.definition, 55)))
                tex_table.write("%s & %s \\\\ \hline" % (index, string.rjust(sense.name, 35).split('.')[0].strip().replace('_', '\_')))
                if index != last:
                    tex_table.write("\n")

            tex_table.write("""\end{tabular}\n\end{center}""")


def create_analysis_tables():

    analyzers = [DocumentAnalyzer(synsets=synsets, similarity_function=sim_fun) for sim_fun in SIMILARITY_FUNCS]

    documents = document_list()

    for doc in documents:
        full_analysis = {}
        for analyzer in analyzers:
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
                                                    analyzer.best_word_for[synset].name))

        doc_name = doc.name.replace(' ', '_').replace(':', '').replace(',', '').lower()[:30]
        with open('paper/analysis_%s.tex' % (doc_name), 'w') as analysis_output:
            analysis_output.write("""
    \\begin{center}
      \\begin{tabular}{ | l | l | l |}
        \hline
        Choosen Sensens & Closest Top Sense & similarity  \\\\ \hline\n""")
            for key in full_analysis.keys():
                analysis_output.write("\multicolumn{3}{|c|}{%s - %s} \\\\ \hline\n" % (doc.name[:30], key.replace('_', ' ')))
                for value in full_analysis[key]:
                    analysis_output.write("%s & %s & %s \\\\ \hline\n" % (value[0].replace('_', ' '), value[2].replace('_', ' '), value[1].replace('_', ' ')))
            analysis_output.write("""\end{tabular}\n\end{center}""")


def create_tables():
    create_top_sense_tables()
    create_analysis_tables()
