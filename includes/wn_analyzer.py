# This Python file uses the following encoding: utf-8
from __future__ import division
from includes import utils
from plot import window_sizes as plotter
import nltk                   
from nltk.corpus import wordnet as wn
import config
reload(config)

import matplotlib.pyplot as plt           
import pylab

if config.WNA_VERBOSE:
	VERBOSE = config.WNA_VERBOSE
else:
	VERBOSE = 0


#Parametros del modulo

#Normaliza teoricidad y practicidad 
NORMALIZE_WORDS = 0
NORMALIZE_YEARS = 0

#Aca se puede eliminar algun criterio de distancia
def distances_mean(path, lch, wup):
	return (path + lch + wup) / 3
 
def normalize(theory, praxis):
	if theory > praxis:
		t = 1.0
		p = praxis / theory
	elif praxis > theory:
		p = 1.0
		t = theory / praxis
	else:
		p = None
		t = None
	return t,p

#Estos son los synsets ("sentidos") contra los que comparamos distancia. 
#Uno para distancia a teoria y otro a praxis
#	Formato: (synset, ponderacion)
# Cada synset descomentado habilita 1.0 puntos a distribuir en la ponderacion

theoretical_synsets = [
								(wn.synset('entity.n.01'), 1.0)
								#(wn.synset('politics.n.05'), 1.0), #'the activities and affairs involved in managing a state or a government''the study of government of states and other political units'
								#(wn.synset('abstraction.n.06'), 1.0),
								#(wn.synset('physical_entity.n.01'), 1.0)
								#(wn.synset("philosophy.n.02"), 1.0), #'the rational investigation of questions about existence and knowledge and ethics'
								#wn.synset('theory.n.01'),     #a well-substantiated explanation of some aspect of the natural world; an organized system of accepted knowledge that applies in a variety of circumstances to explain a specific set of phenomena
								#(wn.synset('theorization.n.01'), 1.0),  #the production or use of theories
								#(wn.synset('politics.n.02'), 1.0),#   'the study of government of states and other political units'
								#(wn.synset('hypothesis.n.02'), 0.8),    #a tentative insight into the natural world; a concept that is not yet verified but that if true would explain certain facts or phenomena
								#wn.synset('theory.n.03'),       #a belief that can guide behavior
												
												
]	
											
practical_synsets = [	
						(wn.synset('politics.n.05'), 1.0),
						(wn.synset('politics.n.02'), 1.0),
						#(wn.synset('military_action.n.01'), 1.0),	
						#(wn.synset("revolution.n.02"), 1.0)										
						#(wn.synset('physical_entity.n.01'), 1.0),
						#(wn.synset("revolution.n.01"), 1.0), # 'a drastic and far-reaching change in ways of thinking and behaving'
						#(wn.synset("revolution.n.02"), 1.0), #'the overthrow of a government by those who are governed'
						#(wn.synset('practice.n.03'), 0.4), # 'translating an idea into action'
						#(wn.synset('action.n.01'), 1.4),  #   something done (usually as opposed to something said)
						#(wn.synset('politics.n.05'), 1.0), #'the activities and affairs involved in managing a state or a government''the study of government of states and other political units'
						#wn.synset('action.n.02')  #   the state of being active
						#(wn.synset('military_action.n.01'), 1.0),  #   a military engagement
						#wn.synset('action.n.05'),  #   the series of events that form a plot
						#wn.synset('action.n.06'),  #   the trait of being active and energetic and forceful
						##wn.synset('action.n.07'),  #   the operating part that transmits power to a mechanism
						#(wn.synset('legal_action.n.01'), 1.6),  #   a judicial proceeding brought by one party against another; one party prosecutes another for a wrong done or for protection of a right or for prevention of a wrong
						#wn.synset('action.n.09'),  # an act by a government body or supranational organization																								
											];


 
def judge_word(word, use_synset_num = 0 , synset_in = False):    
	
	all_synsets = {"theory":theoretical_synsets, "praxis": practical_synsets}
	
	if synset_in:
		all_synsets['praxis'] = synset_in
												
	#La semantica de la relacion entre synset y lemma es confusa y no es importante.
	#Un synset puede tener varios lemmas, un lemma tiene un synset. (Con eso basta)
 	#O sea, donde se itere sobre lemmas debe leerse iteraciones sobre synsets de word
	lemmas = wn.lemmas(word)
	if len(lemmas) == 0:
		wnl = nltk.WordNetLemmatizer()
		word2 = wnl.lemmatize(word)
		lemmas = wn.lemmas(word2)
		if len(lemmas) == 0:
			return (word, None, None)
	
	if not use_synset_num:
		if VERBOSE > 2:  print word+', synsets asociados: '+str(len(lemmas))
	
	#Cruzo los synsets validos word contra theoretical_synsets y practical_synsets
	
	i = 0
	total = {'theory' : 0.0, 'praxis': 0.0, 'iterations': 0}
	
	#Iteracion sobre distintos synsets de word
	for lemma in lemmas:
		
		i = i + 1
		
		#Si use_synset_num viene seteado, saltea todos los loops menos uno
		if use_synset_num:
			if i != use_synset_num:
				continue
				
		 
		synset = lemma.synset
		
		
		if VERBOSE > 2: print synset.name+ ": "+synset.definition
		
		
		if synset.name.split('.')[1] != 'n':
			if VERBOSE > 2: print ' synset de tipo '+synset.name.split('.')[1]+', distancia no definida'
			continue
		
		
		
		#KEY es teoria y praxis
		for key in all_synsets:
		
			pathAcum = 0.0
			lchAcum = 0.0
			wupAcum = 0.0
			k = 0
			
			#Para cada synset de KEY (teoria o praxis), comparo contra el actual synset de word
			#K puede valer distinto para teoria y praxis 
			for (syn, ponderacion) in all_synsets[key]:
				
				#Tomo tres distancias distintas
				path = ponderacion * syn.path_similarity(synset)
				lch  = ponderacion * syn.lch_similarity(synset)		
				wup  = ponderacion * syn.wup_similarity(synset)
				
				
				pathAcum = pathAcum + path
				lchAcum = lchAcum + lch
				wupAcum = wupAcum + wup
				k = k + 1
				#print "  "+syn.name+" {path: "+str("{0:.2f}".format(path))+", lch: "+str("{0:.2f}".format(lch))+", wup: "+str("{0:.2f}".format(wup))+" }"
			
			
			 
			path = pathAcum / k
			lch = lchAcum / k
			wup = wupAcum / k
			
			#Valor de teoria y praxis para este significado de word 
			mean = distances_mean(path, lch, wup) 
			
			#Valor de teoria y praxis para todos los significados de word
			total[key] = total[key] + mean
			total['iterations'] = total['iterations'] + 1
			
			if VERBOSE > 2: print " "+key+": "+"{0:.2f}".format(mean)+" {path: "+"{0:.2f}".format(path)+", lch: "+str("{0:.2f}".format(lch))+", wup: "+str("{0:.2f}".format(wup))+" }"	 
			
	if total['iterations'] > 0:
		#Multiplico por 2 porque iterations se conto dos veces (una por teoria y otra por praxis)
		total['theory'] = total['theory'] * 2.0 / total['iterations']
		total['praxis'] = total['praxis'] * 2.0 / total['iterations']
	else:
		total['theory'] = None
		total['praxis'] = None
	
	if NORMALIZE_WORDS:
			total['theory'], total['praxis'] = normalize(total['theory'], total['praxis'])
				
	return (word, total['theory'], total['praxis'])



	
#Asigna teoricidad y practicidad a un año desde resumen zipf general
def judge_year(year, zipf_data = False, synset_in = False):
	
	if not zipf_data:
		zipf_data = utils.from_file('years_zipf.json')
	
	n = 200
	use_synset_num = 0
	top_words = zipf_data[year]['top_words_with_ocurrences'][:n]
	total_words = zipf_data[year]['total_words']
	total_vocab = zipf_data[year]['total_vocab'] 
	all_words_ocurrences =  sum([c for [w, c] in top_words])
	#Totales para el año.
	#t = valor de teoricidad del año
	#p = valor de practicidad del año
	#i = cantidad de palabras con valor valido (<= n)
	t = 0.0
	p = 0.0
	i = 0
	

	for [word, word_ocurrences] in top_words:
		
		(word, teoricidad, practicidad) = judge_word(word, use_synset_num, synset_in)
		
		if teoricidad == None:
			continue;
		
		#Diferentes formas de ponderar palabras
		#Ocurencias sobre el total de ocurrencias de todas las top_words (zipf genera las 200 mas pesadas)
		#		No sirve
		#ponderacion = word_ocurrences / all_words_ocurrences
		
		#Ponderacion constante
		ponderacion = 1.0
		
		# Ponderar lo practico
		#if practicidad > teoricidad:
		#	ponderacion = 2.0		
		#else:
		#	ponderacion = 0.1
		
		# Ponderar segun este criterio
		#if abs(practicidad - teoricidad) < 0.1:
		#	ponderacion = 1.0		
		#else:
		#	continue;
			#ponderacion = 0.1
		
		teoricidad = ponderacion * teoricidad
		practicidad = ponderacion * practicidad
			
		i = i + 1
		t = t + teoricidad
		p = p + practicidad
		if VERBOSE > 1: print "{0:.2f}".format(teoricidad)+ " "+ "{0:.2f}".format(practicidad)+ " "+word+" (ponderada="+"{0:.2f}".format(ponderacion)+")" 
	
	
	t = t / i
	p = p / i
	
	if NORMALIZE_YEARS:
		t, p = normalize(t,p)
		
	if VERBOSE > 0: print year+" {0:.2f}".format((p-t))+ " " +"{0:.2f}".format(t)+ " "+ "{0:.2f}".format(p)
	#if VERBOSE > 0: print year+ " {0:.2f}".format(p)
	return (t, p)	
	
def judge_years(min_year, max_year, graph_label = False, synset_in = False):
	
	zipf_data = utils.from_file('years_zipf.json')
	years = []
	ts = []
	ps = []
	ys = []
	for year in range(min_year, max_year):
		( t, p) = judge_year(str(year), zipf_data, synset_in)
		years.append(year)
		ts.append(t)
		ps.append(p)
		ys.append((t-p))	
		
	pylab.xticks(years,  rotation=90)		
	#pylab.plot(years, ys, label='revolution - abstraccion')
	pylab.plot(years, ps, label="politics 2 y 5")
	#pylab.plot(years, ts, label='abstracto')
	pylab.legend()
	pylab.show()		
		


'''

#Ejecuta judge_word con palabras que deberian ser claramente categorizadas	
def test_judgement():
	
	all_words = {
	            		"theory": [
															"concept",
															"relations",
															"logic",
															"inference",
															"topic",
															"sociology",
															"philosophy",
															"science",
															"structure",
															"representation",
															"think"	
									],
									"praxis": [
									 						"war",
									 						"legislation",
									 						"parlament",
									 						"must",
									 						"government",
									 						"work",
									 						"fight"
									]
							}
	
	for key in all_words:
		print 'Cercanas a '+ key
		print ''
		for word in all_words[key]:
			judge_word(word, 1)
			print ''






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
	
	res['zipf_resume']['distances'] = map(judge_word, data['zipf_resume']['top_words'][:n])
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
'''

''' 
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
'''

'''
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
'''

'''
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
'''

'''
def wn_generate(y1, y2, n = 20):
	zipf = utils.from_file('years_zipf.json')
	data = {}
	
	for year in range(y1, y2):
		year = str(year)
		print 'Procesando año: '+year
		for x in zipf:
			if zipf[x]['name'] == year:
				zipf_resume = zipf[x]
				break
		
		data[year] = utils.load_year_data(year, zipf_resume)	
		data[year]['wn']= generate_wn_data(data[year], year, n)
	
	return data
	
#Entry point
def create_wn_files(y1=1893, y2= 1924, n=20):
	data = wn_generate(y1, y2, n)
	for year in data:
		utils.to_file(data[year]['wn'], 'by_year/'+year+'_wn.json')
'''

