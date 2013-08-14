# This Python file uses the following encoding: utf-8
import json
import copy
import config
import information_value as iv
import zipf as zf
import utils
from analyzers import wn_analyzer as wna

class Preprocessor:
	
	def __init__(self, infile = False, outfile = False):
		if not infile:
			infile = "lenin_work.json"
		if not outfile:
			outfile = "lenin_work.json.out"
			 
		self.infile = config.data_dir+infile
		self.outfile = config.data_dir+outfile
		self.out_works = []
		
	
	def load(self):	
		works_file = open(self.infile, 'r').read()
		self.works = json.loads(works_file)

	
	def write(self):
		handler = open(self.outfile, 'w')
		handler.write(json.dumps(self.out_works, indent = 1))
				
	def execute(self, method, params):
		self.load()
		method(params)
		self.write()
		
	def write_year(self, year):
		self.out_works = []
		i = 1
		for work in self.works:
			if work['year'] == year:
				work['yid'] = i
				i = i+1
				self.out_works.append( work)
 
 	def run_zipf(self,n):
		self.out_works = []
		i = 1
		for work in self.works:
				zipf = zf.Zipf(work['text'], work['name'])
				zipf.execute()
				aux = zipf.get_results(n)
				aux['wid'] = work['wid']
				aux['yid'] = work['yid']
				self.out_works.append( aux)
 	
 	def add_index(self, arg):
 		self.out_works = []
 		i = 1
 		for work in self.works:
 			work['wid'] = i
			i = i+1 
			self.out_works.append( work)
	
	def run_iv(self, n):
		self.out_works = []
		print 'Cantidad de trabajos: '+str(len(self.works))
		i = 1
		for work in self.works:
			ivx = iv.InformationValue(work['text'])
			aux = ivx.get_results(n, i)
			aux['wid'] = work['wid']
			aux['yid'] = work['yid']
			aux['name'] = work['name']
			self.out_works.append( aux)
			i= i+1
			 	

def split_years(min_year, max_year, infile = False):
		pre = Preprocessor(infile, False)
		for y in range(min_year, max_year):
			print 'Generando archivo para '+str(y)
			pre.outfile = config.data_dir+'by_year/'+str(y)+'_works.json'
			pre.execute(pre.write_year, str(y))

def add_window_size(infile=False):
	pre = Preprocessor(infile, 'lenin_work_with_window_size.json')
	pre.execute(pre.add_window_size, False)
		

def reload_base_files(min_year, max_year):
	print 'Creando archivo indexado...'
	pre =Preprocessor('lenin_work.json', 'id_lenin_work.json')
	pre.execute(pre.add_index, False)
	print 'Creando archivos por año...'
	split_years(min_year, max_year,'id_lenin_work.json')

def create_zipf_for_year(year, total_words = 200):
	pre =Preprocessor('by_year/'+year+'_works.json', 'by_year/'+year+'_zipf.json')
	pre.execute(pre.run_zipf, total_words)

def create_zipf_files(min_year, max_year, total_words = 200):
	for year in range(min_year, max_year):
		print 'Creando zipf para año '+str(year)
		create_zipf_for_year(str(year), total_words)
		
def create_zipf_resume(min_year, max_year, total_words = 200):
	 print 'Creando resumen de zipf por años....'
	 zipfRunner = zf.ZipfRunner()
	 res = zipfRunner.get_all_years(min_year, max_year, total_words)
	 utils.to_file(res, 'years_zipf.json')			

def create_iv_for_year(year, total_words = 200):
	pre =Preprocessor('by_year/'+year+'_works.json', 'by_year/'+year+'_iv.json')
	pre.execute(pre.run_iv, total_words)

def create_iv_files(min_year, max_year, total_words = 200):
	print 'Configure las escalas de ventanas en IV.get_scales()'
	for year in range(min_year, max_year):
		print 'Creando IV para año '+str(year)
		create_iv_for_year(str(year), total_words)

# Llamar esto para hacer todo el proceso del readme.txt 
def restart_database(min_year, max_year):
	reload_base_files(min_year, max_year)
	create_zipf_files(min_year, max_year)
	create_zipf_resume(min_year, max_year)
	# create_iv_files(min_year, max_year)
	# Estoy aca, tengo que correr wna.wn_write(1905, 1924)
	# wna.create_wn_files(min_year, max_year)