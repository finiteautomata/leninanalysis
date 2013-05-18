# coding: utf-8
from __future__ import division
import urllib2
import json
import math
import operator
from copy import deepcopy
import numpy
import nltk
import re
from BeautifulSoup import BeautifulStoneSoup
from numpy import array
from numpy.random import standard_normal, rand
import sys
from random import shuffle

def tokenize(raw_text, filters):
  #Primero hay que separar en sentencias
  tokens = [token.lower() for token in nltk.wordpunct_tokenize(raw_text) if re.match('\w+', token) and len(token) > 1]

  return filter(lambda t: all(f(t) for f in filters), tokens) 
  
class Tokenizer:
  def __init__(self, text):
    self.text = text
    self.tokens = []
    self.fdist = 0
    self.filters = []

  def add_filter(self, a_filter):
    self.filters.append(a_filter)

  def get_words(self):
    if len(self.tokens) == 0:
      self.tokens = tokenize(self.text, self.filters)
    return self.tokens

  def get_fdist(self):
    if self.fdist == 0:
      self.get_words()
      self.fdist = nltk.FreqDist(self.tokens)
    return self.fdist

def print_prob(str, prob):
  if rand() < prob:
    print(str)

def add_fdist(f1, f2):
  for tok in f2.samples():
    f1.inc(tok, f2[tok])


class EntropyCalculator:
  def __init__(self, chapters):
    self.chapters = chapters
    self.tokens = None
    self.reverse_tokens = None

    self.get_tokens()

  def get_tokens(self):
    if self.tokens:
      return
    
    self.tokens = []
    for chapter in self.chapters:
      chapter["fdist"] = nltk.FreqDist(chapter["text"])
      if chapter["fdist"].N() == 0:
        print "THERE IS AN ERROR HERE text=%s" % chapter["text"]
        raise Exception()
      self.tokens.extend(chapter["text"])
      
    self.reverse_tokens = dict(zip(self.tokens, range(len(self.tokens))))

  def get_frequencies_for(self, word):
    return map(lambda c: c["fdist"][word] / float(c["fdist"].N()),self.chapters)

  def get_chapter_probabilities_for(self, word):
    frequencies = self.get_frequencies_for(word)
    sum_freq = sum(frequencies)
    if round(sum_freq,5) == .0  or any([numpy.isnan(x) for x in frequencies]):
      print frequencies
      print word
      #print frequencies
      print u'Algo está jodido acá para %s' % word
      return [.0] * len(frequencies)
    probabilities = map(lambda f: f/sum_freq, frequencies)

    return probabilities

  def get_entropy_for(self, token):
    probabilities = self.get_chapter_probabilities_for(token)
    sum_prob = reduce(lambda s, pi: s+ pi * math.log(pi) if pi!=0 else s ,probabilities, 0)
    ret_val = -(1 / math.log(len(self.chapters))) * sum_prob

    return ret_val

  def calculate_entropies(self, words):
    entropies = {}
    for word in words:
      entropies[word] = self.get_entropy_for(word)
    return entropies

def get_tokens(text):
  tokenizer = Tokenizer(text)
  tokenizer.add_filter(lambda w: not w in string.punctuation)
  return tokenizer.get_words()


def split_into_chapters(tokens, window_size):
  chapters = []
  no_of_chapters = int(math.ceil(len(tokens) / window_size))
  for i in range(no_of_chapters):
    starting_token = i * window_size;
    tokens_in_window = tokens[starting_token:starting_token+window_size]
    chapters.append(tokens_in_window)

  #Este formato lo uso como "estándar" para almacenar capítulos
  chapters = map(lambda chapter:{'text':chapter}, chapters)
  return chapters

def get_entropy(tokens, words, window_size):
  chapters = split_into_chapters(tokens, window_size)
  calculator = EntropyCalculator(chapters)
  return calculator.calculate_entropies(words)

def get_frequencies(tokens, words, window_size):
  chapters = split_into_chapters(tokens, window_size)
  ret = {}
  calculator = EntropyCalculator(chapters)
  for word in words:
    ret[word] = calculator.get_frequencies_for(word)
  return ret
  
def get_occurrence_probability(tokens, words, window_size):
  chapters = split_into_chapters(tokens, window_size)
  ret = {}
  calculator = EntropyCalculator(chapters)
  for word in words:
    ret[word] = calculator.get_chapter_probabilities_for(word)
  return ret


def get_iv(tokens, window_size):
  words = list(set(tokens))
  fdist = nltk.FreqDist(tokens)
  entropies_of_normal_text = get_entropy(tokens, words, window_size)
  shuffled_tokens = deepcopy(tokens)
  shuffle(shuffled_tokens)

  entropies_of_shuffled_text = get_entropy(shuffled_tokens, words, window_size)
  information_values = {}
  for word in words:
    information_values[word] = fdist.freq(word)*abs(entropies_of_normal_text[word] - entropies_of_shuffled_text[word])
  return information_values


def get_top_words(tokens, window_size, number_of_words):
  information_values = get_iv(tokens, window_size)
  return sorted(information_values.iteritems(), key=operator.itemgetter(1), reverse=True)[:number_of_words]
