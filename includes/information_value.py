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
				freq[word].append(window_fdist[word] / len(window))

		return freq
	
	def occurrence_probability(self, window_size, random=False, ret_freq = False):
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


		for i in range(0,P):
			window = get_window(tokenized_text, window_size=window_size, number_of_window=i)
			window_fdist = nltk.FreqDist(window)

			for word in self.words:
				freq[word].append(window_fdist[word] / len(window))
		
		if ret_freq:
			return freq
			
		p = {}		
		for word in self.words:
			p[word] = []
			for i in range(0,P):
				if sum_f[word] != 0:
					p[word].append(1.0*freq[word][i] / sum_f[word])
					

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
		for i in range(0,cant_randoms):
			random_entropy[i] = self.entropy(window_size, random=True)
		
		
		for word in self.words:
			random_mean[word] = 0
			for i in range(0,cant_randoms):
				random_mean[word] = random_mean[word] + random_entropy[i][word]
			random_mean[word] = 1.0 * random_mean[word] / cant_randoms


		information_value = {}
		alternar = True
		tokenized_text = self.tokens
		N = self.total_words
		for word in self.words:
			frec = 1.0* self.word_fdist[word] / N
			if alternar:  #Invierto el valor para que de positivo todo
				frec = -1.0*frec
			information_value[word] =  (frec * (ordered_entropy[word] - random_mean[word]))
			
		items = sorted(information_value.items(), key=get_count, reverse=alternar)
	
		#print 'Top 20 words (information values):'
		#for item in items[:20]:
			#print item[0]
	#		print item[0], item[1]	
	    
		return information_value

  #window_size = scale*len(text)
	def get_scales(self):
		#return [2500]
		if self.total_words < 2000:
			scales = [0.05, 0.1, 0.25, 0.5]
		else:
			scales = [x*0.01 for x in range(1,21)]
		return scales

	def get_window_sizes(self):
		return [200*i for i in range(1,20)]


	def get_results(self, number_of_words=20):
		results = {}
		results['ivs'] = [] 
		results['tried_windows'] = []
		results['total_words']= self.total_words
		ivs = {}

		window_sizes = self.get_window_sizes()

		window_sizes.extend([int(self.total_words * scale) for scale in self.get_scales()])
		window_sizes = filter(lambda x: x < 7000, window_sizes)
		window_sizes = set(window_sizes)

		for window_size in window_sizes:
			try:
				print "Probando tamaño de ventana = %s" % window_size
				if window_size >= 1:
					information_value = self.information_value(window_size)
					sorted_words = sorted(information_value.iteritems(), key=operator.itemgetter(1), reverse=True)
					ivs[window_size] = sorted_words[0][1]

					res = {
							'window_size' : window_size,
							'iv_per_word': ivs[window_size],
							'top_words': sorted_words[:number_of_words]
					}
					results['ivs'].append(res)
					results['tried_windows'].append(window_size)
			except WindowSizeTooLarge as e:
				# La ventana es demasiado grande => salir!
				break
		#Criterio: maximo de promedio de IV sobre todas las palabras
		results['best_window_size'] = max(ivs, key=ivs.get)
		results['best_iv_per_word'] = ivs[results['best_window_size']]
		for res in results['ivs']:
			if res['window_size'] == results['best_window_size']:
				results['top_words'] = res['top_words']
				if 'scale' in res.keys():
					results['best_scale'] = res['scale']
				break
		
		results.pop("ivs", None)
		return results
			
	def calculate_window_size(self):
		
		ivs = {}
		self.get_tokenized_text()
#		top = self.total_words / 2
#		if top > 6000:
#			top = 6000 #maximo segun paper
#			bottom = 1000
#			step = 500
#		elif top > 2000:
#			bottom = 500
#			step = 500
#		elif top < 500:
#			bottom = 50
#			step = 10
#		else:
#			bottom = 100
#			step = 100
					 
#		print 'Se evalua range('+str(bottom)+','+str(top)+','+str(step)+')'	 
#		windows = [int(self.total_words* 0.03), int(self.total_words* 0.02),int(self.total_words* 0.01), int(self.total_words*0.005)  ]
		print 'Longitud del texto: '+str(self.total_words)
		if self.total_words < 2000:
			scales = [0.05, 0.1, 0.25, 0.5]
		else:
			scales = [0.01, 0.025, 0.05, 0.1, 0.25, 0.33 ]
		for scale in scales:
			window_size = int(self.total_words* scale)
			if window_size >= 1:
				aux = self.information_value(window_size) 
				ivs[window_size] = sum([c for (w,c) in aux]) / len(aux)
				print '\t Ventana '+str(scale)+' '+str(window_size)+' '+str(ivs[window_size]) 
			else:
				print '\t Se omite la escala '+str(scale)
		
		max_window_size = max(ivs, key=ivs.get)
		iv_per_word = ivs[max_window_size]
		return max_window_size, iv_per_word		


def get_window(tokens, window_size, number_of_window):
	lower_bound = number_of_window * window_size
	upper_bound = (number_of_window+1) * window_size
	return tokens[lower_bound:upper_bound]