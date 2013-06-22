# This Python file uses the following encoding: utf-8
from __future__ import division
from copy import deepcopy
from random import shuffle
import math
import random
import operator
import nltk

def print_probabilty(str, prob):
	if random.random() < prob:
		print str


def get_count(ctuple):
	return ctuple[1]

class WindowSizeTooLarge(Exception):
	pass


class InformationValueCalculator:

	def __init__(self, tokens):
		#se carga la lista de tokens
		self.tokens = tokens
		self.randomized_text = deepcopy(self.tokens)
		shuffle(self.randomized_text)
		self.word_fdist = nltk.FreqDist(self.tokens)

	def number_of_windows(self, window_size):
		return int(math.ceil(self.word_fdist.N() / window_size))
	
	def get_words_positions(self, tokenized_text):
		word_positions = dict((word, []) for word in self.word_fdist.samples())
		for position, word in enumerate(tokenized_text):
			word_positions[word].append(position)
		return word_positions 

	def get_frequencies(self, tokenized_text, window_size):
		"""
			Return the frequency of a word within a window
		"""
		left_index = 0
		P = self.number_of_windows(window_size) 
		positions = self.get_words_positions(tokenized_text)
		freq = dict((word, []) for word in self.word_fdist.samples())

		for window in range(left_index, P):

			right_index = left_index + window_size -1
			for word in self.word_fdist.samples():
				_len = len(filter(lambda x: x >= left_index and x <= right_index, positions[word]))
				freq[word].append(_len / window_size)

			left_index = right_index + 1 
		return freq
	
	def occurrence_probability(self, window_size, tokenized_text):
		"""
			The quantity pi stands for the probability of finding the word in part i, given that
			it is present in the corpus. 
		"""
		P = self.number_of_windows(window_size)
		if P == 0 or P == 1:
			raise WindowSizeTooLarge("Windows size %s for text size %s" % (window_size, self.word_fdist.N()))
		p = {}
		for word, frequencies_list in self.get_frequencies(tokenized_text, window_size).iteritems():
			p[word] = []
			for i in range(0,P):
				sum_f_word = sum(frequencies_list)
				if sum_f_word != 0:
					p[word].append(frequencies_list[i] / sum_f_word)#sum_f[word])
				else:
					p[word].append(.0)
		return p


	def entropy(self, tokenized_text, window_size):
		p = self.occurrence_probability(window_size, tokenized_text)
		if not p:
			return False
		S = {}
		P = self.number_of_windows(window_size)

		for word in self.word_fdist.samples():
			S[word] = 0
			for prob in p[word]:
				if prob:
					S[word] = S[word] + (prob * math.log(prob))
			S[word] = (-1)* S[word] / math.log(P)
			#print word+': '+ str(S[word])
		return S

	#Calcular la "information value" de las palabras seleccionadas,
	#Definicion de IV:
	# "The difference between the two entropies multiplied by the frequency of the word gives
	# the word’s 'information value' in the text.
	# Information value, just as in binary computing, is measured in bits."

	def information_value(self, window_size):
		ordered_entropy = self.entropy(self.tokens, window_size)

		random_entropy = self.entropy(self.randomized_text, window_size)

		information_value = {}
		for word in self.word_fdist.samples():
			freq = self.word_fdist.freq(word)
			information_value[word] =  freq * abs(ordered_entropy[word] - random_entropy[word])

		return information_value

	def get_window_size_analysis(self, window_size, number_of_words=20):
		information_value = self.information_value(window_size)
		# sort the words according to their information value
		sorted_words = sorted(information_value.iteritems(), key=operator.itemgetter(1), reverse=True)
		max_iv = sorted_words[0][1]
		# Sum the reverse of sorted_words to improve numerical stability
		iv_sum = reduce(lambda x,y: x+y[1], reversed(sorted_words), 0)
		iv_average = iv_sum / self.word_fdist.N()

		return {
			'window_size' : window_size,
			'words' : sorted_words[:number_of_words],
			'average_iv' : iv_average,
			'iv_sum' : iv_sum,
			'max_iv' : max_iv
		}


def get_window(tokens, window_size, number_of_window):
    from information_value.window import Window
    return Window(tokens, window_size, number_of_window)
#    lower_bound = number_of_window * window_size
#    upper_bound = (number_of_window+1) * window_size
#    window = tokens[lower_bound:upper_bound]
#    if len(window) < window_size:
#        window += ['#'] * (window_size-len(window))
#	return window


