# This Python file uses the following encoding: utf-8  
from __future__ import division
from copy import deepcopy
from random import shuffle
import math       
import multiprocessing
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
		self.words = set(tokens)
		self.word_fdist = nltk.FreqDist(self.tokens)

	def number_of_windows(self, window_size):
		return int(math.ceil(len(self.tokens) / window_size))
		
	def get_frequencies(self, tokenized_text, window_size):
		freq = dict((word, []) for word in self.words)
		P = self.number_of_windows(window_size)
		for i in range(0,P):
			window = get_window(tokenized_text, window_size=window_size, number_of_window=i)
			window_fdist = nltk.FreqDist(window)

			for word in self.words:
				freq[word].append(window_fdist.freq(word))

		return freq
	
	def occurrence_probability(self, window_size, tokenized_text):
		P = self.number_of_windows(window_size)
		if P == 0 or P == 1:
			raise WindowSizeTooLarge("Ventana de tamaño %s para texto de tamaño %s" % (window_size, len(tokens)))			
		
		freq = self.get_frequencies(tokenized_text, window_size)
		sum_f = dict((word, sum(freq[word])) for word in self.words)
			
		p = {}		
		for word in self.words:
			p[word] = []
			for i in range(0,P):
				if sum_f[word] != 0:
					p[word].append(freq[word][i] / sum_f[word])
				else:
					p[word].append(.0)
					

		return p
		
	def entropy(self, tokenized_text, window_size):
		p = self.occurrence_probability(window_size, tokenized_text)
		if not p:
			return False
		S = {}
		P = self.number_of_windows(window_size)
		
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

	def get_window_size_analysis(self, window_size, number_of_words=20):
		information_value = self.information_value(window_size)
		# sort the words according to their information value
		sorted_words = sorted(information_value.iteritems(), key=operator.itemgetter(1), reverse=True)
		max_iv = sorted_words[0][1]
		# Sum the reverse of sorted_words to improve numerical stability
		iv_sum = reduce(lambda x,y: x+y[1], reversed(sorted_words), 0)
		iv_average = iv_sum / len(self.tokens)

		return {
			'window_size' : window_size,
			'words' : sorted_words[:number_of_words],
			'average_iv' : iv_average,
			'iv_sum' : iv_sum,
			'max_iv' : max_iv
		}




def get_window(tokens, window_size, number_of_window):
	lower_bound = number_of_window * window_size
	upper_bound = (number_of_window+1) * window_size
	window = tokens[lower_bound:upper_bound]

	if len(window) < window_size:
		window += ['#'] * (window_size-len(window))
	return window

def get_top_words(tokens, window_size, number_of_words):
	ivc = InformationValueCalculator(tokens)
	res = ivc.information_value(window_size)

	return sorted(res.iteritems(), key=operator.itemgetter(1), reverse=True)[:number_of_words]

information_value_calculator = None

def get_window_size_analysis(window_size):
	try:
		print "Probando window_size = %s" % window_size
		return (window_size, information_value_calculator.get_window_size_analysis(window_size, 20))
	except WindowSizeTooLarge as e:
		return (window_size, None)

def get_optimal_window_size(tokens, window_sizes, number_of_words=20):
	global information_value_calculator
	results_per_window_size = {}

	information_value_calculator = InformationValueCalculator(tokens)


	pool = multiprocessing.Pool(processes=5)
	results_per_window_size = dict(pool.map(get_window_size_analysis, window_sizes))
	
	#Criterio: maximo de promedio de IV sobre todas las palabras
	best_result = max(results_per_window_size.iteritems(),
		key= lambda res: res[1]['max_iv']
		)
	
	return best_result

