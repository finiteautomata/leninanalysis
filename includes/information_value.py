# This Python file uses the following encoding: utf-8  
from __future__ import division
import copy
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
		self.word_fdist = nltk.FreqDist(self.words)

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
	
	def occurrence_probability(self, window_size, random=False):
		#print 'occurrence_probability'
		if random:
			#print 'random'
			tokenized_text = self.get_rand_tokenized_text()
		else:
			tokenized_text = self.tokens
		P = int(math.ceil(self.total_words / window_size))
		if P == 0 or P == 1:
			print 'Ventana demasiado grande'
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
		
	def entropy(self, window_size, random = False):
		p = self.occurrence_probability(window_size, random)
		if not p:
			return False
		S = {}
		P = self.total_words / window_size
		
		for word in self.words:
			S[word] = 0
			for prob in p[word]:
				if prob:
					S[word] = S[word] + (prob * math.log(prob))
			S[word] = S[word] * (-1.0 / math.log(P))
			#print word+': '+ str(S[word])		
		return S		
		
	#Calcular la "information value" de las palabras seleccionadas,
	#Definicion de IV:
	# "The difference between the two entropies multiplied by the frequency of the word gives 
	# the word’s 'information value' in the text. 
	# Information value, just as in binary computing, is measured in bits."
	
	def information_value(self, window_size):
		ordered_entropy = self.entropy(window_size)
		if not ordered_entropy:
			return False
		
		random_entropy = {}
		random_mean = {}
		cant_randoms = 1
		
		random_entropy = self.entropy(window_size, random=True)
		
		information_value = {}
		alternar = True
		tokenized_text = self.tokens
		N = self.total_words
		for word in self.words:
			frec = self.word_fdist[word] / N
			if alternar:  #Invierto el valor para que de positivo todo
				frec = -1.0*frec
			information_value[word] =  (frec * (ordered_entropy[word] - random_entropy[word]))
				    
		return information_value




def get_window(tokens, window_size, number_of_window):
	lower_bound = number_of_window * window_size
	upper_bound = (number_of_window+1) * window_size
	return tokens[lower_bound:upper_bound]