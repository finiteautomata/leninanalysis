# This Python file uses the following encoding: utf-8
import json
import copy
import works_loader as wl


class Concatenator:
	
	def __init__(self):		
		self.works = wl.Works()
		
	def all_corpus(self):
		
		res = ""
		for work in self.works.works:
			 res = res + work['text']
		
		return res
		
	def year(self, year):
		dictionary = self.works.get_dictionary()
		res = ""
		for month in dictionary[year]:
			for work in dictionary[year][month]:
				res = res + work['text']
		
		return res
	
	def month(self, year, month):
		dictionary = self.works.get_dictionary()
		res = ""
		for work in dictionary[year][month]:
			res = res + work['text']
		
		return res			