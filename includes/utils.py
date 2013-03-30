# This Python file uses the following encoding: utf-8


import nltk                   
from nltk.corpus import stopwords
import json
import config


def to_file(data, outfile):
	handler = open(config.data_dir+outfile, 'w')
	handler.write(json.dumps(data, indent = 1))

def from_file(infile):
	return json.loads(open(config.data_dir+infile, 'r').read())
	
def load_year_data(year, zipf_resume = False):
	
	if not zipf_resume:
		zipf = from_file('years_zipf.json')
		for x in zipf:
			if x['name'] == year:
				zipf_resume = x
				break

	ivx = from_file('by_year/'+year+'_iv.json')
	for ivs in ivx:
		ivs['top_words_with_stop_words'] = ivs['top_words']
		ivs['top_words_with_iv_with_stop_words'] = ivs['top_words_with_iv']
		ivs['top_words'] = [w for w in ivs['top_words'] if w not in stopwords.words('english')]
		ivs['top_words_with_iv'] = [[x[0],x[1]] for x in ivs['top_words_with_iv'] if x[0] not in stopwords.words('english')]
	
	res= {
					'base' : from_file('by_year/'+year+'_works.json'),
					'zipf' : from_file('by_year/'+year+'_zipf.json'),
					'iv'  : ivx, 
					'zipf_resume': zipf_resume
				}
	return res
	
def load_data(y1, y2):
	data = {}
	zipf = from_file('years_zipf.json')
	for year in range(y1, y2):
		year = str(year)
		print 'Cargando datos para año: '+year
		
		for x in zipf:
			if x['name'] == year:
				zipf_resume = x
				break
		
		data[year] = load_year_data(year, zipf_resume)
	
	return data		