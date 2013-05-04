# This Python file uses the following encoding: utf-8
from __future__ import division

import json
import tokenizer as t
import works as w
import config
import utils

def get_count(ctuple):
	return ctuple[1]


class Zipf:
	
	def __init__(self, text, name, run = False):
		self.text = text
		self.name = name
		if run:
			self.execute()
			self.print_results()
	 
	def execute(self):
		#tokenize(text, only_alpha = False, only_alphanum = True,  clean_stop_words = False, clean_punctuation = True):
		self.tokens = t.tokenize(self.text, clean_stop_words = True)
		self.total_words = len(self.tokens)
		self.total_vocab = len(set(self.tokens))
	
		word_count = {}  # Map each word to its count
		for word in self.tokens: 
			if not word in word_count:
				word_count[word] = 1
			else:
				word_count[word] = word_count[word] + 1
			
		items = sorted(word_count.items(), key=get_count, reverse=True)
		self.word_count = [(w,c, c/self.total_words) for (w,c) in items]


	def print_results(self, n = 20):
		print 'Analisis Zipf sobre: '+self.name
		print 'Palabras totales: '+str(self.total_words)
		print 'Vocabulario total: '+str(self.total_vocab)
		print 'Palabra'.ljust(20)+'\t\tTotal\t\tTasa de ocurrencia'
		i = 0
		for res in self.word_count:
			print res[0].ljust(20)+'\t\t'+str(res[1])+'\t\t'+str(res[2])
			i = i+1
			if i == n:
				break
			
	
	def get_results(self, n = 20):
		
		results = {
							'name': self.name, 
							'total_words': self.total_words,
							'total_vocab': self.total_vocab,
							'top_words': [w for (w,c,x) in self.word_count[:n]],
							'top_words_with_ocurrences': [(w,c) for (w,c,x) in self.word_count[:n]]
							}
		return results



class ZipfRunner:
	
	def __init__(self):
		self.works = w.Works()
		self.works.load_dictionary()
	
	
	def get_year(self, year, n = 20):
		year_works = self.works.get_year(year)
		year_text  = self.works.get_just_text(year_works)	
		z = Zipf(year_text, year)
		z.execute()
		return z.get_results(n)
		
	
	def get_all_years(self,min_year, max_year,  n = 20):
		res = {}
		for y in range(min_year, max_year):
			print 'Calculando año '+str(y)
			res[str(y)] =self.get_year(str(y), n)
		return res	
	
	#Necesita zipf_by_year.json
	def word_use_by_year(self, word):
		data =utils.from_file('zipf_by_year.json')
		for x in data:
			dat = data[x]
			if dat['top_words'].count(word):
				index = str(dat['top_words'].index(word)+1)
			else:
				index = 'No presente'
			print dat['name']+'	'+index
			 	
		
		
			