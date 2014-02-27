import string
import logging

from interpreter import Document

log = logging.getLogger('lenin')


def create_top_sense_tables():
    state_and_revolution = Document.query.find({"name": {"$regex": "State and Revolution"}}).next()
    imperialism_capitalism = Document.query.find({"name": {"$regex": "Imperialism.*Capitalism.*"}}).next()
    materialism_criticism = Document.query.find({"name": "Lenin: MATERIALISM and EMPIRIO-CRITICISM"}).next()
    what_is_to_be_done = Document.query.find({"name": {"$regex": ".*What Is To Be Done.*"}}).next()
    agrarian_programme = Document.query.find({"name": u'Lenin: The Agrarian Programme of Social-Democracy in the First Russian Revolution, 1905-1907'}).next()
    documents = [state_and_revolution, imperialism_capitalism, materialism_criticism, what_is_to_be_done, agrarian_programme]

#   reset_senses()
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
                log.info("Sense %s --  %s " % (string.rjust(sense.name, 35),
                    string.rjust(sense.definition, 55)))
                tex_table.write("%s & %s \\\\ \hline" % (index, string.rjust(sense.name, 35).split('.')[0].strip().replace('_', '\_')))
                if index != last:
                    tex_table.write("\n")

            tex_table.write("""\end{tabular}\n\end{center}""")
