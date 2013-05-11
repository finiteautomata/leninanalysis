# This Python file uses the following encoding: utf-8  
from __future__ import division
import math       
import random                
import copy


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
		self.rand_tokenized_text = None
	
	def get_rand_tokenized_text(self):
		if not self.rand_tokenized_text:
			self.rand_tokenized_text = copy.deepcopy(self.tokens)
			random.shuffle(self.rand_tokenized_text)
		return self.rand_tokenized_text
		
	
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
		
		freq = {}
		sum_f = {}
		
		for word in self.words:
			sum_f[word] = 0
			freq[word] = {}
			for i in range(0,P):
				window = get_window(tokenized_text, window_size=window_size, number_of_window=i)
				freq[word][i] = window.count(word) / len(window) 
				sum_f[word] = sum_f[word] + freq[word][i] 	 
		
		print "Frequencies = %s" % freq
		if ret_freq:
			return freq
			
		p = {}		
		for word in self.words:
			p[word] = {}
			for i in range(0,P):
				if sum_f[word] != 0:
					p[word][i] = 1.0*freq[word][i] / sum_f[word]	
					

		return p
		
	def entropy(self, window_size, random = False):
		p = self.occurrence_probability(window_size, random)
		if not p:
			return False
		S = {}
		P = self.total_words / window_size
		
		for word in self.words:
			S[word] = 0
			for i in p[word]:
				if p[word][i] != 0:
					S[word] = S[word] + (p[word][i] * math.log(p[word][i]))
			
			S[word] = S[word] * (-1.0 / math.log(P))
			#print word+': '+ str(S[word])		
		
		return S		
		
	#Calcular la "information value" de las palabras seleccionadas,
	#Definicion de IV:
	# "The difference between the two entropies multiplied by the frequency of the word gives 
	# the word’s 'information value' in the text. 
	# Information value, just as in binary computing, is measured in bits."
	
	def information_value(self, window_size):
		#print 'information_value'
		ordered_entropy = self.entropy(window_size)
		if not ordered_entropy:
			return False
		
		random_entropy = {}
		random_mean = {}
		cant_randoms = 1
		for i in range(0,cant_randoms):
			#print 'Calculando entropias de texto randomizado '+ str(i+1)
			random_entropy[i] = self.entropy(window_size, random=True)
		
		
		for word in self.words:
			random_mean[word] = 0
			for i in range(0,cant_randoms):
				random_mean[word] = random_mean[word] + random_entropy[i][word]
			random_mean[word] = 1.0 * random_mean[word] / cant_randoms


		information_value = {}
		alternar = True
		tokenized_text = self.get_tokenized_text()
		N = self.total_words
		for word in self.words:
			frec = 1.0* tokenized_text.count(word) / N
			if alternar:  #Invierto el valor para que de positivo todo
				frec = -1.0*frec
			information_value[word] =  (frec * (ordered_entropy[word] - random_mean[word]))
			
		items = sorted(information_value.items(), key=get_count, reverse=alternar)
	
		#print 'Top 20 words (information values):'
		#for item in items[:20]:
			#print item[0]
	#		print item[0], item[1]	
	    
		return items

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
		
	def get_results(self):
		results = {}
		results['ivs'] = [] 
		results['tried_windows'] = []
		results['total_words']= self.total_words
		ivs = {}
		
		for window_size in self.get_window_sizes():
			try:
				print "Probando tamaño de ventana = %s" % window_size
				if window_size >= 1:
					aux = self.information_value(window_size)
					
	        #Criterio: promedio de todos los information values
					ivs[window_size] = max([c for (w,c) in aux])
					res = {
									'window_size' : window_size,
									'iv_per_word': ivs[window_size],
									'top_words': [w for (w,c) in aux[:n]],
									'top_words_with_iv': [(w,c) for (w,c) in aux[:n]],
									
								}
					results['ivs'].append(res)
					results['tried_windows'].append(window_size)
			except WindowSizeTooLarge as e:
				# La ventana es demasiado grande => salir!
				break

    #Generar datos de IV para cada escala de ventana 
		for scale in self.get_scales():
			try:
				window_size = int(self.total_words* scale)
				print str(work_index)+' evaluando escala '+str(scale)
				if window_size >= 1:
					aux = self.information_value(window_size)
					
	        #Criterio: promedio de todos los information values
					ivs[window_size] = max([c for (w,c) in aux])
					
					res = {
									'window_size' : window_size,
									'scale': scale,
									'iv_per_word': ivs[window_size],
									'top_words': [w for (w,c) in aux[:n]],
									'top_words_with_iv': [(w,c) for (w,c) in aux[:n]],
									
								}
					results['ivs'].append(res)
					results['tried_windows'].append(window_size) 
			except WindowSizeTooLarge as e:
				break
    
		#Criterio: maximo de promedio de IV sobre todas las palabras
		results['best_window_size'] = max(ivs, key=ivs.get)
		results['best_iv_per_word'] = ivs[results['best_window_size']]
		for res in results['ivs']:
			if res['window_size'] == results['best_window_size']:
				results['top_words'] = res['top_words']
				results['top_words_with_iv'] = res['top_words_with_iv']
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