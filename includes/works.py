# This Python file uses the following encoding: utf-8
import json
import copy
import config

class Works:
	
	def __init__(self, filename = False):
		if not filename:
			filename = "lenin_work.json"	
		
		filename = config.data_dir+filename
		works_file = open(filename, 'r').read()
		self.works = json.loads(works_file)
		self.dictionary = False
		
	def get_dictionary(self):
		if not self.dictionary:
			self.load_dictionary()
			
		return self.dictionary
	
	def load_dictionary(self, not_ind = False, just_titles = False):
		
		dictionary = {}
		
		for work in self.works:
			aux = {}
			if not_ind and (work["year"] == u'ind' or work["month"] == u'ind'):
				continue
				
			aux["name"] = copy.deepcopy(work["name"])
			if not just_titles:
				aux["text"] = copy.deepcopy(work["text"])
			
			aux["url"] = copy.deepcopy(work["url"])
			if not work["year"] in dictionary:
				dictionary[work["year"]] = {}
			
			if not work["month"] in dictionary[work["year"]]:
				dictionary[work["year"]][work["month"]] = []
			
			
			dictionary[work["year"]][work["month"]].append(aux) #= dictionary[work["year"]][work["month"]] + [aux] 	 
		
		self.dictionary = dictionary
	
#	def get_text_by_url(dictionary, needle):
#		res_texts = []
#		for y in dictionary:
#			for m in dictionary[y]:
#				for i in range(0, len(dictionary[y][m])-1):
#					if needle in dictionary[y][m][i]['url']:
#						print 'dictionary['+y+']['+m+']['+str(i)+']'
#						res_texts.append(dictionary[y][m][i])
#	
#		return res_texts					
	
	#Devuelve un array plano de textos de un año
	def get_year(self, year):
		ret = []
		d = self.get_dictionary()
		for m in d[year]:
			ret = ret + d[year][m]
		
		return ret
	
	
	
	def get_totals(self):
		total = {}
		total['total'] = 0
		d = self.get_dictionary()
		for year in d:
			total[year] = {}
			total[year]['total'] = 0
			for month in d[year]:
				total[year][month] = 0
				for art in d[year][month]:
					total[year][month] = total[year][month] + 1
					total[year]['total'] = total[year]['total'] + 1
					total['total'] = total['total'] + 1  
				
		return total			
		
	#Recibe un array de LeninWorks y devuelve un string de sus cuerpos concatenados	
	def get_just_text(self, works):
		res = ""
		for work in works:
			res = res + work['text']
	
		return res
	
	def print_year_totals(self):
		t = self.get_totals()
		for y in range(1893, 1923):
			print str(y)+'   '+str(t[str(y)]['total'])	