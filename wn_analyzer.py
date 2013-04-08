# This Python file uses the following encoding: utf-8
from __future__ import division
from includes import utils
import nltk                   
from nltk.corpus import wordnet as wn


def generate_wn_data(data = False, year = False, n = 20):
	
	if not data:
		print 'Cargando archivos....'
		data = utils.load_year_data(year)
	
	res = {}
	res['zipf_resume'] = {}
	res['zipf'] = []
	res['iv'] = []
	
	res['theory_iv'] = 0
	res['theory_zipf'] =0
	res['praxis_iv'] = 0
	res['praxis_zipf'] = 0
	
	
	print 'Calculando Teoria y Praxis para resumen Zipf...('+year+')'
	
	res['zipf_resume']['distances'] = map(get_distances, data['zipf_resume']['top_words'][:n])
	res['zipf_resume']['theory'], res['zipf_resume']['praxis']= judge_total(res['zipf_resume']['distances'], data['zipf_resume']['top_words_with_ocurrences'])
	
	
	print 'Calculando Teoria y Praxis para cada texto..('+year+')'
	cant = len(data['base'])
	i = 0
	while i < cant:
		
		print '\tTexto '+str(i +1)+' de '+str(cant)
		if (data['base'][i]['wid'] != data['iv'][i]['wid']) or (data['base'][i]['wid'] != data['zipf'][i]['wid']):
			print 'Error al procesar'
			break
		res['iv'].append({})
		res['zipf'].append({})
		
		res['iv'][i]['distances'] = map(get_distances, data['iv'][i]['top_words'][:n])
		res['zipf'][i]['distances'] = map(get_distances, data['zipf'][i]['top_words'][:n])
		res['iv'][i]['theory'],res['iv'][i]['praxis'] = judge_iv(data['iv'][i]['best_iv_per_word'],res['iv'][i]['distances'], data['iv'][i]['top_words_with_iv'])
		res['zipf'][i]['theory'],res['zipf'][i]['praxis'] = judge_total(res['zipf'][i]['distances'], data['zipf'][i]['top_words_with_ocurrences']) 			
		res['theory_iv'] = res['theory_iv'] + res['iv'][i]['theory']
		res['praxis_iv'] = res['praxis_iv'] + res['iv'][i]['praxis']
		res['theory_zipf'] = res['theory_zipf'] + res['zipf'][i]['theory']
		res['praxis_zipf'] = res['praxis_zipf'] + res['zipf'][i]['praxis'] 
		i=i+1
	
	res['theory_iv'] = res['theory_iv'] / cant
	res['praxis_iv'] = res['praxis_iv'] / cant
	res['theory_zipf'] = res['theory_zipf'] / cant
	res['praxis_zipf'] = res['praxis_zipf']	/ cant
	
	return res
 
 
def judge_total( distances, totals):
	
	aux = []
	for (w,t,p) in distances:
		if t == None or p == None:
			continue
		for x in totals:
			if w == x[0]:
				aux.append((w,t,p,x[1]))
				break
			
	total_words = len(distances)
	teo = sum([theory*ocurrencias for (word,theory,praxis,ocurrencias) in aux])/total_words
	pra = sum([praxis*ocurrencias for (word,theory,praxis,ocurrencias) in aux])/total_words
	
	return teo,pra

def judge_iv(iv_mean, distances, ivs):
	
	aux = []
	for (w,t,p) in distances:
		if t == None or p == None:
			continue
		for x in ivs:
			if w == x[0]:
				aux.append((w,t,p,x[1]))
				break
	total_words = len(distances)
	teo = sum([t*iv for (w,t,p,iv) in aux])/total_words
	pra = sum([p*iv for (w,t,p,iv) in aux])/total_words
	
	return teo,pra

def get_distances(word):
	
	theory = wn.lemmas('theory')[0].synset
	praxis = wn.lemmas('praxis')[0].synset
	
	ss = wn.lemmas(word)
	if len(ss) == 0:
		wnl = nltk.WordNetLemmatizer()
		word2 = wnl.lemmatize(word)
		ss = wn.lemmas(word2)
		if len(ss) == 0:
			return (word, None, None)
		
	ss = ss[0].synset
	
	return (word, theory.path_similarity(ss), praxis.path_similarity(ss))


def wn_generate(y1, y2, n = 20):
	zipf = utils.from_file('years_zipf.json')
	data = {}
	
	for year in range(y1, y2):
		year = str(year)
		print 'Procesando año: '+year
		for x in zipf:
			if x['name'] == year:
				zipf_resume = x
				break
		
		data[year] = utils.load_year_data(year, zipf_resume)	
		data[year]['wn']= generate_wn_data(data[year], year, n)
	
	return data
	
def wn_write(y1=1893, y2= 1924, n=20):
	data = wn_generate(y1, y2, n)
	for year in data:
		utils.to_file(data[year]['wn'], 'by_year/'+year+'_wn.json')