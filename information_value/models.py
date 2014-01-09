# coding: utf-8
import logging
import hashlib

from nltk.corpus import stopwords
from nltk import sent_tokenize

from pymongo.errors import DuplicateKeyError

import operator
import wisdom
from ming import Session, schema
from ming.odm import ODMSession, Mapper
from ming.odm.mapper import MapperExtension
from ming.odm.property import ForeignIdProperty, FieldProperty, RelationProperty
from ming.odm.declarative import MappedClass

import config
from includes.tokenizer import tokenize
from information_value.calculator import InformationValueCalculator


MIN_TOKENS = 2000


log = logging.getLogger('lenin')

session = Session.by_name('document_store')
odm_session = ODMSession(doc_session=session)


class DocumentWindowSizeDuplicateHash(MapperExtension):
    """
        Used as unique key for Document - WindowSize
    """
    def before_insert(self, instance, state, session):
        doc_window_hash = hashlib.sha1(str(instance.document_id) + str(instance.window_size)).hexdigest()
        if instance.__class__.query.find({'doc_window_hash': doc_window_hash}).count() > 0:
            raise DuplicateKeyError('Duplicate hash found ', doc_window_hash)
        instance.doc_window_hash = doc_window_hash


class InformationValueResult(MappedClass):

    def __init__(self, iv_words, sum_threshold=config.SUM_THRESHOLD, *args, **kwargs):
        if type(iv_words) is dict:
            iv_words = list(iv_words.iteritems())
        self.sum_threshold = sum_threshold
        super(InformationValueResult, self).__init__(*args, iv_words=iv_words, **kwargs)

    @property
    def iv_sum(self):
        # Todo: improve performance of this...
        sorted_ivs = sorted(map(operator.itemgetter(1), self.iv_words), reverse=True)
        self.max_iv = sorted_ivs[0]
        amount_to_be_taken = int(len(sorted_ivs) * self.sum_threshold) or 10
        sorted_ivs = sorted_ivs[:amount_to_be_taken]
        # Sum the reverse of sorted_words to improve numerical stability
        return reduce(lambda x, y: x + y, reversed(sorted_ivs), 0)

    class __mongometa__:
        session = odm_session
        name = 'information_value_result'
        unique_indexes = [('doc_window_hash', ), ]
        extensions = [DocumentWindowSizeDuplicateHash]

    def __repr__(self):
        return "IVR(%s window size, %s iv-words)" % (self.window_size, len(self.iv_words))

    def __str__(self):
        return self.__repr__()

    _id = FieldProperty(schema.ObjectId)
    doc_window_hash = FieldProperty(schema.String)
    window_size = FieldProperty(schema.Int)
    iv_words = FieldProperty(schema.Array(schema.Anything))  # Array or list
    document_id = ForeignIdProperty('Document')
    document = RelationProperty('Document')


class Document(MappedClass):

    class __mongometa__:
        session = odm_session
        name = 'document'

    _id = FieldProperty(schema.ObjectId)
    url = FieldProperty(schema.String, unique=True)
    name = FieldProperty(schema.String)
    text = FieldProperty(schema.String)
    month = FieldProperty(schema.String)
    year = FieldProperty(schema.Int)
    number_of_words = FieldProperty(schema.Int)
    results = RelationProperty(InformationValueResult)

    def top_words(self, total_words=20, stop_words=stopwords.words('english'), greater_than_zero=True, window_size=None):
        if window_size is None:
            window_size = self.get_information_value_result().window_size
        iv_words = self.get_iv_by_window_size(window_size)
        iv_words = [(t[0], t[1]) for t in iv_words if t[0] not in stop_words and (not greater_than_zero or t[1] > 0.0)][:total_words]

        effective_total_words = max(total_words, len(iv_words))
        return [(word, 1.0/effective_total_words) for (word, iv_value) in iv_words]


    def top_senses(self, total_senses=20):
        top_words = self.top_words()
        sentences = self.sentences

        senses = [wisdom.multi_sentence(sentences, word) for (word, _) in top_words]
        return senses

    # calculator_class is poor man's dependency injection :)
    def get_iv_by_window_size(self, window_size, calculator_class=InformationValueCalculator):
        sort = lambda iv_words: sorted(iv_words, key=operator.itemgetter(1), reverse=True)

        for res in self.results:
            if res.window_size == window_size:
                return sort(res.iv_words)

        iv_words = calculator_class(self.tokens).information_value(window_size)
        res = InformationValueResult(window_size=window_size, document=self, iv_words=iv_words)

        try:
            odm_session.flush()
        except DuplicateKeyError:
            pass
            return sort(res.iv_words)

    def get_information_value_result(self):
        iv_res = None
        best_iv = 0.0
        #sort = lambda iv_words: sorted(iv_words, key=operator.itemgetter(1), reverse=True)
        for one_iv in self.results:
            sum_iv = sum(map(lambda (w, iv): iv, one_iv.iv_words))
            if best_iv <= sum_iv:
                best_iv = sum_iv
                iv_res = one_iv
        #iv_res.iv_words = sort(iv_res.iv_words)
        return iv_res

    @property
    def tokens(self):
        tokenizer_func = getattr(self, 'tokenizer', tokenize)
        return tokenizer_func(self.text)
    #trivial, removes 'Lenin: ' as prefix

    @property
    def short_name(self):
        ss = self.name.replace("Lenin: ", "")
        return ss[: 40 + ss[40:].find(" ")]+"..."

    #generators test
    def result_list(self):
        for each in self.results:
            yield each

    @property
    def total_results(self):
        return len(self.results)

    @property
    def total_tokens(self):
        return len(self.tokens)

    @property
    def sentences(self):
        return sent_tokenize(self.text)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        params = (
            unicode(self.year).encode('utf-8'),
            unicode(self.month.capitalize()).encode('utf-8'),
            unicode(self.short_name).encode('utf-8'),
            unicode(self.total_tokens).encode('utf-8'),
            unicode(self.total_results).encode('utf-8')
        )
        if self.total_results > 0:
            res = "Doc(%s, %s - %s, %s tks, %s res:" % params
            for iv_res in self.result_list():
                res += " " + iv_res.__repr__()
                res += ")"
            return res
        else:
            return "Doc(%s, %s - %s, %s tks, %s res)" % params

    #unset all words with 0.0 as value for iv_words of all IVResults
    def no_zero_results(self):
        res = list()
        for each in self.results:
            res.append(self.aux_clean_zeros(each))
        return res

    #Takes an IVResults and clean all iv_words with 0.0
    def aux_clean_zeros(self, result):
        res = dict()
        for w, c in result.iv_words.items():
            if c > 0.0:
                res[w] = c
        result.iv_words = res
        #print result.iv_words
        return result


class DocumentList(object):

    def __init__(self, name = '', only_with_results = False, year = None):
        self.search_criterion = {
            'number_of_words': {'$gte': MIN_TOKENS}
        }
        if name and name != '': 
            self.search_criterion['name'] = {'$regex': '.*'+name+'.*'},

        if year is not None:
            self.year = year
            self.search_criterion['year'] = year

        self.only_with_results = only_with_results

        self.base_load()


    def base_load(self):
        print self.search_criterion
        self.documents_query = Document.query.find(self.search_criterion)

    def __iter__(self):
        return self.documents_query
        
    @property
    def total_docs(self):
        return self.documents_query.count()

    @property
    def total_results(self):
        total = 0
        for text in self:
            total += text.total_results
        return total

    def get_all_iv_words(self):
        dict_k_v = {}
        for doc in self:
            for w, c in doc.top_words():
                try:
                    dict_k_v[w] += 1
                except:
                    dict_k_v[w] = 1
        return dict_k_v

    def print_docs(self):
        for text in self.documents:
            print text

    def results(self):
        res = list()
        for text in self:
            res.append(text.result_list)
        return res

def doc_for(name):
  doc_list = DocumentList(name)
  if doc_list.total_docs == 0:
    return None
  else:
    return doc_list.first()

Mapper.compile_all()
