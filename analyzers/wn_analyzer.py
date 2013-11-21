# This Python file uses the following encoding: utf-8
from __future__ import division
import nltk
from nltk.corpus import wordnet as wn
from information_value.models import *


import config
reload(config)


# Similarity definitions:
# http://nltk.googlecode.com/svn/trunk/doc/api/nltk.corpus.reader.wordnet.Synset-class.html#path_similarity
class WordNetAnalyzer:

    @classmethod
    def create_analyzer_for(cls, word):
        ponderated_synsets = cls.get_init_synsets_for_word(word)
        return cls(ponderated_synsets)  

    # ponderated_synsets is a list((synset, ponderation))
    # sum(ponderation) must be 1

    def __init__(self, ponderated_synsets, use_similarity='path'):
        self.document = None
        self.ponderated_synsets = ponderated_synsets
        self.use_similarity = use_similarity

    def set_similarity(self, use_similarity):
        self.use_similarity = use_similarity

    # creates the trivial synsets set for a given word
    @staticmethod
    def get_init_synsets_for_word(word, take_only_first=False):
        synsets = WordNetAnalyzer.get_word_synsets(word, take_only_first)
        return [(synset, 1.0 / len(synsets)) for synset in synsets]

    # return list((word, ponderation [between 0 and 1], result [between 0 and
    # 1]))
    def get_words_results(self):
        return [(word, ponderation, self.judge_word(word)) for (word, ponderation) in self.top_words]

    # return a value between 0 and 1
    def judge_doc(self, document):
        self.document = document

        self.top_words = self.document.top_words(20)
        return sum([ponderation * result for (word, ponderation, result) in self.get_words_results()])

    # get all synsets for a given word
    @staticmethod
    def get_word_synsets(word, take_only_first=False):
        lemmas = wn.lemmas(word)
        # si no me da lemmas, intento algo
        if len(lemmas) == 0:
            wnl = nltk.WordNetLemmatizer()
            lemmatized_word = wnl.lemmatize(word)
            lemmas = wn.lemmas(lemmatized_word)
            if len(lemmas) == 0:
                return []

        # some distances doesn't handle not-noun words
        synsets = [
            lemma.synset for lemma in lemmas if lemma.synset.name.split('.')[1] == 'n']
        if take_only_first:
            return synsets[:1]
        return synsets

    def judge_synset(self, synset):
        if self.use_similarity == 'lch':
            lchs = (syn.lch_similarity(synset) for (syn, ponderacion) in self.ponderated_synsets)
            return max(lchs)
        elif self.use_similarity == 'wup':
            wups = (syn.wup_similarity(synset) for (syn, ponderacion) in self.ponderated_synsets)
            return max(wups)
        else:
            synsets = (s[0] for s in self.ponderated_synsets)
            return similarity_synsets_to_synset(synsets, synset)

    # judge a word according to criterion
    #@return double a value between 1.0 and 0.0
    def judge_word(self, word, take_only_first_synset=False):
        synsets_results = [self.judge_synset(synset)
                           for synset in self.get_word_synsets(word, take_only_first_synset)]
        if len(synsets_results) != 0:
            return max(synsets_results)
        else:
            return 0

"""
Returns the similarity between a set of synsets, and a particular synset
"""
def similarity_synsets_to_synset(list_of_synsets, synset):
    similarities = [synset.path_similarity(_synset) for _synset in list_of_synsets]
    return max(similarities)



def get_wnas():
    #war_docs = DocumentList("War")
    #politic_docs = DocumentList("Politic")
    war_synsets = [(wn.synset('war.n.01'), 1.0)]
    politics_synsets = [(wn.synset('politics.n.01'), 1.0)]
    praxis_synsets = [(wn.synset('practice.n.03'), 1.0)]
    theory_synsets = [(wn.synset('theory.n.01'), 1.0)]
    rev_synsets = [(wn.synset('revolution.n.02'), 1.0)]
    # (wn.synset('theorization.n.01'), 0.5),  #the production or use of theories

    return {
        'war': WordNetAnalyzer(war_synsets),
        'civil_war': WordNetAnalyzer([(wn.synset("civil_war.n.01"), 1.0)]),
        'ww': WordNetAnalyzer([(wn.synset("world_war.n.01"), 1.0)]),
        'politics': WordNetAnalyzer(politics_synsets),
        'theory': WordNetAnalyzer(theory_synsets),
        'praxis': WordNetAnalyzer(praxis_synsets),
        'revolution': WordNetAnalyzer(rev_synsets),
    }


def example_analyzer():
    state_list = DocumentList("State and Rev")
    d = state_list.documents[0]
    abstraction_synsets = [(wn.synset('abstraction.n.06'), 1.0)]
    wna = WordNetAnalyzer(abstraction_synsets)
    return wna


def state_rev_distances():
    state_list = DocumentList("State and Rev")
    state_doc = state_list.documents[0]
    war = WordNetAnalyzer(WordNetAnalyzer.get_init_synsets_for_word("war"))
    idealism = WordNetAnalyzer(WordNetAnalyzer.get_init_synsets_for_word("idealism"))
    rev = WordNetAnalyzer(WordNetAnalyzer.get_init_synsets_for_word("revolution"))
    filo = WordNetAnalyzer(WordNetAnalyzer.get_init_synsets_for_word("philosophy"))
    war.judge_doc(state_doc)


def test():
    general_docs = DocumentList("")
    war_docs = DocumentList("War")
    politic_docs = DocumentList("Politic")
    war_synsets = [(wn.synset('war.n.01'), 1.0)]
    politics_synsets = [(wn.synset('politics.n.01'), 1.0)]

    war_wna = WordNetAnalyzer(war_synsets)
    politics_wna = WordNetAnalyzer(politics_synsets)

    war_wna_war_docs = sum([war_wna.judge_doc(doc)
                           for doc in war_docs]) / war_docs.total_docs
    war_wna_politic_docs = sum([war_wna.judge_doc(doc)
                               for doc in politic_docs]) / politic_docs.total_docs
    war_wna_general_docs = sum([war_wna.judge_doc(doc)
                               for doc in general_docs]) / general_docs.total_docs

    print "WAR-Analyzer: war docs: %s, politics docs: %s, general docs: %s" % (war_wna_war_docs, war_wna_politic_docs, war_wna_general_docs)

    politic_wna_war_docs = sum([politics_wna.judge_doc(doc)
                               for doc in war_docs]) / war_docs.total_docs
    politic_wna_politic_docs = sum([politics_wna.judge_doc(doc)
                                   for doc in politic_docs]) / politic_docs.total_docs
    politic_wna_general_docs = sum([politics_wna.judge_doc(doc)
                                   for doc in general_docs]) / general_docs.total_docs

    print "POLITICS-Analyzer: war docs: %s, politics docs: %s, general docs: %s" % (politic_wna_war_docs, politic_wna_politic_docs, politic_wna_general_docs)


def judge_list(doc_list, analyzer):
    print "Judging..."
    if doc_list.total_docs == 0:
        return None
    print "Judging %s for %s" % (doc_list, analyzer)
    return (sum([analyzer.judge_doc(doc) for doc in doc_list]) / doc_list.total_docs) * 100


def wna_for(word):
    return WordNetAnalyzer(WordNetAnalyzer.get_init_synsets_for_word(word))


def year_vs_concept_data():
    war = WordNetAnalyzer(WordNetAnalyzer.get_init_synsets_for_word("war"))
    idealism = WordNetAnalyzer(
        WordNetAnalyzer.get_init_synsets_for_word("idealism"))
    rev = WordNetAnalyzer(
        WordNetAnalyzer.get_init_synsets_for_word("revolution"))
    filo = WordNetAnalyzer(
        WordNetAnalyzer.get_init_synsets_for_word("philosophy"))
    toilette = wna_for("toilette")
    filo = WordNetAnalyzer(
        WordNetAnalyzer.get_init_synsets_for_word("philosophy"))

    maximum = 0.0
    res = dict()
    for year in range(1899, 1923):
        print "Retrieving documents for %s..." % year
        doc_list = DocumentList("", False, year)
        print "Judging..."
        res[year] = {
            'rev': (judge_list(doc_list, rev) - 7),
            'filo': (judge_list(doc_list, filo) - 7),
            'war': (judge_list(doc_list, war) - 7),
            'idea': (judge_list(doc_list, idealism) - 7),
        }
        print "year: %s, total docs: %s, war res: %s" % (year, doc_list.total_docs, res[year])
    return res


def compare_obvious():
    wnas = get_wnas()
    prac = DocumentList("Two Tactics").documents[0]  # Two Tactics
    # Concluding Remarks to the Symposium Marxism and Liquidationism'
    theo = DocumentList("arxism").documents[0]
    docs = [prac, theo]
    for doc in docs:
        print "praxis: %.2f, theory:  %.2f, rev: %.2f, war: %.2f, politics: %.2f  %s" % (
            wnas["praxis"].judge_doc(doc) * 100,
            wnas["theory"].judge_doc(doc) * 100,
            wnas["revolution"].judge_doc(doc) * 100,
            wnas["war"].judge_doc(doc) * 100,
            wnas["politics"].judge_doc(doc) * 100,
            doc.short_name
        )


def normalize(theory, praxis):
    if theory > praxis:
        t = 1.0
        p = praxis / theory
    elif praxis > theory:
        p = 1.0
        t = theory / praxis
    else:
        p = None
        t = None
    return t, p


theoretical_synsets = [
    #(wn.synset('entity.n.01'), 1.0),
    # (wn.synset('politics.n.05'), 1.0), #'the activities and affairs involved in managing a state or a government''the study of government of states and other political units'
    (wn.synset('abstraction.n.06'), 1.0),
    #(wn.synset('physical_entity.n.01'), 1.0)
    # (wn.synset("philosophy.n.02"), 1.0), #'the rational investigation of questions about existence and knowledge and ethics'
    # wn.synset('theory.n.01'),     #a well-substantiated
    # explanation of some aspect of the natural world; an organized
    # system of accepted knowledge that applies in a variety of
    # circumstances to explain a specific set of phenomena
    # the production or use of theories
    (wn.synset('theorization.n.01'), 1.0),
    # (wn.synset('politics.n.02'), 1.0),#   'the study of government of states and other political units'
    # a tentative insight into the natural world; a concept that is
    # not yet verified but that if true would explain certain facts
    # or phenomena
    (wn.synset('hypothesis.n.02'), 0.8),
    # a belief that can guide behavior
    (wn.synset('theory.n.03'), 1.2)
]

practical_synsets = [
    (wn.synset('politics.n.05'), 1.0),
    (wn.synset('politics.n.02'), 1.0),
    (wn.synset('military_action.n.01'), 1.0),
    #(wn.synset("revolution.n.02"), 1.0)
    #(wn.synset('physical_entity.n.01'), 1.0),
    # (wn.synset("revolution.n.01"), 1.0), # 'a drastic and far-reaching change in ways of thinking and behaving'
    # (wn.synset("revolution.n.02"), 1.0), #'the overthrow of a government by those who are governed'
    # (wn.synset('practice.n.03'), 0.4), # 'translating an idea into action'
    # (wn.synset('action.n.01'), 1.4),  #   something done (usually as opposed to something said)
    #'the activities and affairs involved in managing a state or a government''the study of government of states and other political units'
    (wn.synset('politics.n.05'), 1.0),
    # wn.synset('action.n.02')  #   the state of being active
    #   a military engagement
    (wn.synset('military_action.n.01'), 1.0),
    # wn.synset('action.n.05'),  #   the series of events that form a plot
    # wn.synset('action.n.06'),  #   the trait of being active and energetic and forceful
    # wn.synset('action.n.07'),  #   the operating part that transmits power to a mechanism
    # (wn.synset('legal_action.n.01'), 1.6),  #   a judicial proceeding brought by one party against another; one party prosecutes another for a wrong done or for protection of a right or for prevention of a wrong
    # wn.synset('action.n.09'),  # an act by a government body or
    # supranational organization
]
