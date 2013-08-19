# This Python file uses the following encoding: utf-8
from __future__ import division
import nltk
from nltk.corpus import wordnet as wn
from information_value.models import *


import config
reload(config)

class WordNetAnalyzer:

  #synsets is a list((synset, ponderation))
  #sum(ponderation) must be 1
  def __init__(self, synsets, document = None):
    self.document = document
    self.synsets = synsets
    assert sum([ponderation for (synset, ponderation) in self.synsets]) == 1.0

  #return list((word, ponderation [between 0 and 1], result [between 0 and 1]))
  def get_words_results(self):
    return [(word, ponderation, self.judge_word(word) )  for (word, ponderation) in self.top_words]

  #return a value between 0 and 1
  def judge_doc(self, document = None):
    if document != None:
       self.document = document
    self.top_words = self.document.top_words(20)
    return sum([ponderation * result for (word, ponderation, result) in self.get_words_results()])
  


  #get all synsets for a given word
  def get_word_synsets(self, word, take_only_first = True):
    lemmas = wn.lemmas(word)
    #si no me da lemmas, intento algo
    if len(lemmas) == 0:
      wnl = nltk.WordNetLemmatizer()
      lemmatized_word = wnl.lemmatize(word)
      lemmas = wn.lemmas(lemmatized_word)
      if len(lemmas) == 0:
        return []
    
    #some distances doesn't handle not-noun words
    synsets =  [lemma.synset for lemma in lemmas if lemma.synset.name.split('.')[1] == 'n']
    if take_only_first:
      return synsets[:1]
    return synsets

  def judge_synset(self, synset):

    paths = [syn.path_similarity(synset)*ponderacion for (syn, ponderacion) in self.synsets]
    path = sum(paths) / len(paths)
    
    lchs = [syn.lch_similarity(synset)*ponderacion for (syn, ponderacion) in self.synsets]
    lch = sum(lchs) / len(lchs)

    wups = [syn.wup_similarity(synset)*ponderacion for (syn, ponderacion) in self.synsets]
    wup = sum(wups) / len(wups)
    return self.distance_measure(path, lch, wup)

  def distance_measure(self, path, lch, wup):
      #return (path + lch + wup) / 3
      return path #others are not between 0 and 1

  #judge a word according to criterion
  #@return double a value between 1.0 and 0.0
  def judge_word(self, word):
    synsets_results = [self.judge_synset(synset) for synset in self.get_word_synsets(word)]
    if len(synsets_results) != 0: return  sum(synsets_results) / len(synsets_results) 
    else: return 0


def get_wnas():
  war_docs = DocumentList("War")
  politic_docs = DocumentList("Politic")
  war_synsets = [(wn.synset('war.n.01'), 1.0)]
  politics_synsets = [(wn.synset('politics.n.01'), 1.0)]
  praxis_synsets = [(wn.synset('practice.n.03'), 1.0)]
  theory_synsets = [(wn.synset('theory.n.01'), 1.0)]
  rev_synsets = [(wn.synset('revolution.n.02'), 1.0)]
  #(wn.synset('theorization.n.01'), 0.5),  #the production or use of theories

  return {'war': WordNetAnalyzer(war_synsets), 
          'politics': WordNetAnalyzer(politics_synsets), 
          'theory': WordNetAnalyzer(theory_synsets),
          'praxis': WordNetAnalyzer(praxis_synsets),
          'revolution': WordNetAnalyzer(rev_synsets),
        }

def example_analyzer():
  state_list = DocumentList("State and Rev")
  state_doc = state_list.documents[0]
  abstraction_synsets = [(wn.synset('abstraction.n.06'), 1.0)]
  wna = WordNetAnalyzer(abstraction_synsets)
  return wna

def test():
  general_docs = DocumentList("")
  war_docs = DocumentList("War")
  politic_docs = DocumentList("Politic")
  war_synsets = [(wn.synset('war.n.01'), 1.0)]
  politics_synsets = [(wn.synset('politics.n.01'), 1.0)]

  war_wna = WordNetAnalyzer(war_synsets)
  politics_wna = WordNetAnalyzer(politics_synsets)

  war_wna_war_docs= sum([war_wna.judge_doc(doc)  for doc in war_docs]) / war_docs.total_docs
  war_wna_politic_docs = sum([war_wna.judge_doc(doc)  for doc in politic_docs]) / politic_docs.total_docs
  war_wna_general_docs = sum([war_wna.judge_doc(doc)  for doc in general_docs]) / general_docs.total_docs
  
  print "WAR-Analyzer: war docs: %s, politics docs: %s, general docs: %s" % (war_wna_war_docs, war_wna_politic_docs,war_wna_general_docs )
  
  politic_wna_war_docs = sum([politics_wna.judge_doc(doc)  for doc in war_docs]) / war_docs.total_docs
  politic_wna_politic_docs = sum([politics_wna.judge_doc(doc)  for doc in politic_docs]) / politic_docs.total_docs
  politic_wna_general_docs = sum([politics_wna.judge_doc(doc)  for doc in general_docs]) / general_docs.total_docs

  print "POLITICS-Analyzer: war docs: %s, politics docs: %s, general docs: %s" % (politic_wna_war_docs, politic_wna_politic_docs, politic_wna_general_docs)

def judge_list(doc_list, analyzer):
  return (sum([analyzer.judge_doc(doc)  for doc in doc_list]) / doc_list.total_docs)*100
 
def write_tp():
  wnas = get_wnas()

  maximum = 0.0
  res = dict()
  for year in range(1893, 1924):
    doc_list = DocumentList("", False, str(year))
    aux  = (year, 
                          judge_list(doc_list, wnas["praxis"]),
                          judge_list(doc_list, wnas["theory"]), 
                          judge_list(doc_list, wnas["revolution"]),
                          judge_list(doc_list, wnas["war"]),
                          judge_list(doc_list, wnas["politics"])
                  )
    maximum = max(maximum, aux[1], aux[2], aux[3], aux[4], aux[5])
    res[year] = aux
  
  for year in range(1893, 1924):
    print "%s  praxis: %.2f, theory:  %.2f, rev: %.2f, war: %.2f, politics: %.2f" %  (year, 
                                                                                        res[year][1] / maximum, 
                                                                                        res[year][2] / maximum, 
                                                                                        res[year][3] / maximum,
                                                                                        res[year][4] / maximum,
                                                                                        res[year][5] / maximum,
                                                                                        )

                                                

  
def compare_obvious():
  wnas = get_wnas()
  prac = DocumentList("Two Tactics").documents[0] #Two Tactics
  theo = DocumentList("arxism").documents[0] # Concluding Remarks to the Symposium Marxism and Liquidationism'
  docs = [prac, theo]
  for doc in docs:
    print "praxis: %.2f, theory:  %.2f, rev: %.2f, war: %.2f, politics: %.2f  %s" % (
                                                                                      wnas["praxis"].judge_doc(doc)*100,
                                                                                      wnas["theory"].judge_doc(doc)*100,
                                                                                      wnas["revolution"].judge_doc(doc)*100,
                                                                                      wnas["war"].judge_doc(doc)*100,
                                                                                      wnas["politics"].judge_doc(doc)*100,
                                                                                      doc.short_name
                                                                                    )





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


theoretical_synsets = [
                #(wn.synset('entity.n.01'), 1.0),
                #(wn.synset('politics.n.05'), 1.0), #'the activities and affairs involved in managing a state or a government''the study of government of states and other political units'
                (wn.synset('abstraction.n.06'), 1.0),
                #(wn.synset('physical_entity.n.01'), 1.0)
                #(wn.synset("philosophy.n.02"), 1.0), #'the rational investigation of questions about existence and knowledge and ethics'
                #wn.synset('theory.n.01'),     #a well-substantiated explanation of some aspect of the natural world; an organized system of accepted knowledge that applies in a variety of circumstances to explain a specific set of phenomena
                (wn.synset('theorization.n.01'), 1.0),  #the production or use of theories
                #(wn.synset('politics.n.02'), 1.0),#   'the study of government of states and other political units'
                (wn.synset('hypothesis.n.02'), 0.8),    #a tentative insight into the natural world; a concept that is not yet verified but that if true would explain certain facts or phenomena
                (wn.synset('theory.n.03'), 1.2)      #a belief that can guide behavior
                        
                        
] 
                      
practical_synsets = [ 
            (wn.synset('politics.n.05'), 1.0),
            (wn.synset('politics.n.02'), 1.0),
            (wn.synset('military_action.n.01'), 1.0), 
            #(wn.synset("revolution.n.02"), 1.0)                    
            #(wn.synset('physical_entity.n.01'), 1.0),
            #(wn.synset("revolution.n.01"), 1.0), # 'a drastic and far-reaching change in ways of thinking and behaving'
            #(wn.synset("revolution.n.02"), 1.0), #'the overthrow of a government by those who are governed'
            #(wn.synset('practice.n.03'), 0.4), # 'translating an idea into action'
            #(wn.synset('action.n.01'), 1.4),  #   something done (usually as opposed to something said)
            (wn.synset('politics.n.05'), 1.0), #'the activities and affairs involved in managing a state or a government''the study of government of states and other political units'
            #wn.synset('action.n.02')  #   the state of being active
            (wn.synset('military_action.n.01'), 1.0),  #   a military engagement
            #wn.synset('action.n.05'),  #   the series of events that form a plot
            #wn.synset('action.n.06'),  #   the trait of being active and energetic and forceful
            ##wn.synset('action.n.07'),  #   the operating part that transmits power to a mechanism
            #(wn.synset('legal_action.n.01'), 1.6),  #   a judicial proceeding brought by one party against another; one party prosecutes another for a wrong done or for protection of a right or for prevention of a wrong
            #wn.synset('action.n.09'),  # an act by a government body or supranational organization                                               
                      ];
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
  res['praxis_zipf'] = res['praxis_zipf'] / cant
  
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

