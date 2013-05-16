# coding: utf-8
import urllib2
import json
from BeautifulSoup import BeautifulStoneSoup
from numpy import array
from numpy.random import standard_normal, rand
import sys
from tokenizer2 import Tokenizer
from random import shuffle
import math
import copy
import numpy
import nltk
import re

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
      self.tokens.extend(chapter["text"])
      
    self.reverse_tokens = dict(zip(self.tokens, range(len(self.tokens))))


  def get_chapter_probabilities_for(self, word):
    frequencies = map(lambda c: c["fdist"][word] / float(c["fdist"].N()),self.chapters)
    sum_freq = sum(frequencies)
    if sum_freq == 0 or any([numpy.isnan(x) for x in frequencies]):
      print frequencies
      print word
      #print frequencies
      print u'Algo está jodido acá para %s' % word

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
  no_of_chapters = len(tokens) / window_size + 1
  for i in range(no_of_chapters):
    starting_token = i * window_size;
    tokens_in_window = tokens[starting_token:starting_token+window_size]
    chapters.append(tokens_in_window)

  #Este formato lo uso como "estándar" para almacenar capítulos
  chapters = map(lambda chapter:{'text':chapter}, chapters)
  return chapters

def get_entropy(tokens, window_size):
  chapters = split_into_chapters(tokens, window_size)
  calculator = EntropyCalculator(chapters)
  words = list(set(tokens))
  return calculator.calculate_entropies(words)


def get_iv(tokens, window_size):
  fdist = nltk.FreqDist(tokens)
  entropies_of_normal_text = get_entropy(tokens, words, window_size)
  print entropies_of_normal_text
  shuffled_tokens = deepcopy(tokens)
  shuffle(shuffled_tokens)

  entropies_of_shuffled_text = [] #get_entropy(shuffled_tokens, words, window_size)
  print entropies_of_shuffled_text

  information_values = dict([(word, fdist.freq(word)*abs(entropies_of_normal_text[word] - entropies_of_shuffled_text[word])) for word in words])
  return information_values
