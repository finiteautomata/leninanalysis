# This Python file uses the following encoding: utf-8  
import math       
import random                
import tokenizer
import copy

def get_count(ctuple):
	return ctuple[1]

class InformationValue:
	
	def __init__(self, text, words = False):
		#text es el texto como string
		self.text = text
		#words es un array de palabras sobre las que se van a realizar los calculos
		self.words = words
		#se carga la lista de tokens
		self.tokenized_text = False
		self.total_words = 0
		self.rand_tokenized_text = False
	
	def get_tokenized_text(self):
		
		if not self.tokenized_text:
			self.tokenize_text()
		
		return self.tokenized_text
	
	def get_rand_tokenized_text(self):
		
		if not self.rand_tokenized_text:
			self.rand_tokenized_text = copy.deepcopy(self.get_tokenized_text())
			random.shuffle(self.rand_tokenized_text)
			
		return self.rand_tokenized_text
		
	def tokenize_text(self, only_alpha = False, only_alphanum = True,  clean_stop_words = False, clean_punctuation = True): 
		#print 'tokenize_text'
		self.tokenized_text = tokenizer.tokenize(self.text, only_alpha, only_alphanum, clean_stop_words, clean_punctuation)
		self.total_words = len(self.tokenized_text)
		self.rand_tokenized_text = False
		if not self.words:
			self.words = set(self.tokenized_text)     
		
	
	def occurrence_probability(self, window_size, random=False, ret_freq = False):
		#print 'occurrence_probability'
		if random:
			#print 'random'
			tokenized_text = self.get_rand_tokenized_text()
		else:
			tokenized_text = self.get_tokenized_text()
		
		P = self.total_words / window_size
		if P == 0 or P == 1:
			print 'Ventana demasiado grande'
			return False			
		
		f = {}
		sum_f = {}
		
		for word in self.words:
			sum_f[word] = 0
			f[word] = {}
			for i in range(0,P):
				f[word][i] = 1.0 * tokenized_text[(i*window_size):(((i+1)*window_size)-1)].count(word) / window_size 
				sum_f[word] = sum_f[word] + f[word][i] 	 
		
		if ret_freq:
			return f
			
		p = {}		
		for word in self.words:
			p[word] = {}
			for i in range(0,P):
				if sum_f[word] != 0:
					p[word][i] = 1.0*f[word][i] / sum_f[word]	
					

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


	def get_scales(self):
		if self.total_words < 2000:
			scales = [0.05, 0.1, 0.25, 0.5]
		else:
			scales = [0.01, 0.025, 0.05, 0.1, 0.25, 0.33 ]
		return scales
		
	def get_results(self, n):
		self.get_tokenized_text()
		results = {}
		results['ivs'] = [] 
		results['tried_windows'] = []
		results['total_words']= self.total_words
		ivs = {}
		for scale in self.get_scales():
			window_size = int(self.total_words* scale)
			if window_size >= 1:
				aux = self.information_value(window_size)
				ivs[window_size] = sum([c for (w,c) in aux]) / len(aux)
				res = {
								'window_size' : window_size,
								'scale': scale,
								'iv_per_word': ivs[window_size],
								'top_words': [w for (w,c) in aux[:n]],
								'top_words_with_iv': [(w,c) for (w,c) in aux[:n]],
								
							}
				results['ivs'].append(res)
				results['tried_windows'].append(window_size) 
		
		results['best_window_size'] = max(ivs, key=ivs.get)
		results['best_iv_per_word'] = ivs[results['best_window_size']]
		for res in results['ivs']:
			if res['window_size'] == results['best_window_size']:
				results['top_words'] = res['top_words']
				results['top_words_with_iv'] = res['top_words_with_iv']
				results['best_scale'] = res['scale']
				break
		
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
					