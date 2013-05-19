# This Python file uses the following encoding: utf-8  
from __future__ import division
import copy
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
		self.total_words = len(tokens)
		self.words = set(tokens)
		self.word_fdist = nltk.FreqDist(self.tokens)
		self.rand_tokenized_text = None
	

	def get_rand_tokenized_text(self):
		if not self.rand_tokenized_text:
			self.rand_tokenized_text = copy.deepcopy(self.tokens)
			random.shuffle(self.rand_tokenized_text)
		return self.rand_tokenized_text
		
	def get_frequencies(self, tokenized_text, window_size):
		freq = dict((word, []) for word in self.words)
		P = int(math.ceil(self.total_words / window_size))
		for i in range(0,P):
			window = get_window(tokenized_text, window_size=window_size, number_of_window=i)
			window_fdist = nltk.FreqDist(window)

			for word in self.words:
				freq[word].append(window_fdist.freq(word))

		return freq
	
	def occurrence_probability(self, window_size, tokenized_text):
		P = int(math.ceil(self.total_words / window_size))
		if P == 0 or P == 1:
			raise WindowSizeTooLarge("Ventana de tamaño %s para texto de tamaño %s" % (window_size, self.total_words))			
		
		freq = self.get_frequencies(tokenized_text, window_size)
		sum_f = dict((word, sum(freq[word])) for word in self.words)
			
		p = {}		
		for word in self.words:
			p[word] = []
			for i in range(0,P):
				if sum_f[word] != 0:
					p[word].append(freq[word][i] / sum_f[word])
					

		return p
		
	def entropy(self, tokenized_text, window_size):
		p = self.occurrence_probability(window_size, tokenized_text)
		if not p:
			return False
		S = {}
		P = self.total_words / window_size
		
		for word in self.words:
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

		randomized_text = deepcopy(self.tokens)
		shuffle(randomized_text)
		
		random_entropy = self.entropy(randomized_text, window_size)
		
		information_value = {}
		for word in self.words:
			freq = self.word_fdist.freq(word)
			information_value[word] =  freq * abs(ordered_entropy[word] - random_entropy[word])
				    
		return information_value





def get_window(tokens, window_size, number_of_window):
	lower_bound = number_of_window * window_size
	upper_bound = (number_of_window+1) * window_size
	return tokens[lower_bound:upper_bound]

def get_top_words(tokens, window_size, number_of_words):
	ivc = InformationValueCalculator(tokens)
	res = ivc.information_value(window_size)

	return sorted(res.iteritems(), key=operator.itemgetter(1), reverse=True)[:number_of_words]


def get_optimal_window_size(tokens, window_sizes, number_of_words=20):
	results_per_window_size = {}

	max_iv_per_window_size = {}
	for window_size in window_sizes:
		try:
			print "Probando tamaño de ventana = %s" % window_size
			top_words = get_top_words(tokens, window_size, number_of_words)
			max_iv = top_words[0][1]
			max_iv_per_window_size[window_size] = max_iv
			if window_size >= 1:
				results_per_window_size[window_size] = {
					'words': top_words,
					'max_iv': max_iv
				}
		except WindowSizeTooLarge as e:
		# La ventana es demasiado grande => salir!
			break
#Criterio: maximo de promedio de IV sobre todas las palabras
	best_result = max(results_per_window_size.iteritems(),
		key= lambda res: res[1]['max_iv']
		)
	best_window_size = best_result[0]
	top_words = best_result[1]

	results = {
		'best_window_size' : best_window_size,
		'top_words' : top_words,
		'max_iv_per_window_size' : max_iv_per_window_size
	}

	return results

