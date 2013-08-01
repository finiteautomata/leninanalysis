#Fake python file
#import config
#import logging
#import unittest
#import argparse
#import subprocess
#from commands.database import populate_database
#from commands.database import calculate_results
#from commands.database import cleandb
#from includes import preprocessor as pre
#from includes import wn_analyzer as wna
#from plot.window_sizes import plot_iv_things
#from pymongo import MongoClient
from information_value import models
from includes.tokenizer import tokenize
#from bson.objectid import ObjectId


class TextList(object):
  

  #--@param dict $mongo_search_criterion --- "deprecado"
  #@param string $mongo_search_criterion 
  def __init__(self, name = 'State', only_with_results = False):
    
    #Constructor mas debil
    #if mongo_search_criterion  != None:
    #  self.search_criterion = mongo_search_criterion
    #else:
    #  self.search_criterion = {'name': {'$regex': '.*State.*'}}
    
    #find completo de ejemplo: 
    # *el primer parametro es filtro (WHERE), 
    # *el segundo proyeccion (SELECT) 
    #mongo_it = models.Document.query.find(search_criterion, {"text":0})
    

    
    self.search_criterion =  {'name': {'$regex': '.*'+name+'.*' }}
    
    self.only_with_results = only_with_results

    if name == "":
      name = "All docs"
    self.name = name
    self.base_load()
    #print self

  
  def base_load(self):
    self.current = 0
    
    it = models.Document.query.find(self.search_criterion)
    
    if not self.only_with_results:
      res = it
    else:
        res = list()
        for doc in it:
          if len(doc.results) > 0:
            res.append( doc)  
            #print "%s" % len(doc.results)
          

    self.documents = res
    self.texts = map(Text, self.documents)  
    print self

  def add_month(self, month = None):
    if month is not None:
      self.search_criterion['month'] = month
      self.name += " %s" % month.capitalize()
    
    self.base_load()

  def add_year(self, year = None):
    
    if year is not None:
      self.search_criterion['year'] = year
      self.name += " %s" % year
    
    self.base_load()
    #return self


  def __iter__(self):
        self.current = 0
        return self

  def next(self):
    if self.current > len(self.texts)-1:
      self.current = 0
      raise StopIteration
    else:
        self.current += 1
        return self.texts[self.current-1]
  
  @property
  def total_texts(self):
    return len(self.texts)

  @property
  def total_tokens(self):
    total = 0
    for text in self:
      total += text.total_tokens

    return total

  @property
  def total_results(self):
    total = 0
    for text in self:
      total += text.total_results

    return total

  @property
  def mean_tokens(self):
    return int(self.total_tokens / self.total_texts)

    return total

  def get_all_iv_words(self):
    dict_k_v = {}
    for text in self:
      for w,c in text.iv_words.items():
        try:
          dict_k_v[w] += 1
        except:
          dict_k_v[w] = 1
    return dict_k_v

  def print_texts(self):
    for text in self.texts:
      print text
 
  def results(self):
    res = list()
    for text in self:
      res.append(text.result_list)
    return res

  def __repr__(self):
    params = ( self.name,
              self.total_texts,
              #self.total_tokens,
              self.mean_tokens,
              self.total_results)

    return "TextList(%s, %s txts, ~%s tks/txt, %s res)" % params
    #return "TextList(%s, %s txts, %s tks [~%s tk/txt], %s res)" % params
    #return "TextList("+self.name+": "+self.search_criterion.__str__()+") total: "+str(len(self.texts))
    #return "TextList("+self.name+", "+str(self.total_texts)+" texts, "+"pepe"+")"
    
  def __str__(self):
    return self.__repr__()
    #res = self.__repr__()
    #for text in self.texts:
    #  res+="\r\n"+text.__repr__()
    #return res+"\r\n"+self.__repr__()

    


class Text(object):

 

  def __init__(self, a_document):
    self.doc = a_document

    self._id = unicode(self.doc._id).encode('utf-8')
    self.url = unicode(self.doc.url).encode('utf-8')
    self.name = unicode(self.doc.name).encode('utf-8')
    self.text = unicode(self.doc.text).encode('utf-8')
    self.month = unicode(self.doc.month).encode('utf-8')
    self.year = unicode(self.doc.year).encode('utf-8')
    self.results = self.doc.results
    #tricky default
    self.clean_zeros()

  #trivial, removes 'Lenin: ' as prefix
  @property
  def short_name(self):
    
    ss = self.name.replace("Lenin: ", "")
    return ss[: 50 + ss[50:].find(" ")]+"..."

  def __repr__(self):
    if self.total_results > 0:
      params = ( self.year,
              self.month.capitalize(),
              self.short_name,
              self.total_tokens,
              self.total_results)
      res = "Text(%s, %s - %s, %s tks, %s res:" % params
      for iv_res in self.result_list():
        res+=" "+ iv_res.__repr__()
      res += ")"
      
      return res
    #"+str(self.total_results)+" results)"

    else:
      params = ( self.year,
              self.month.capitalize(),
              self.short_name,
              self.total_tokens,
              self.total_results)
      return "Text(%s, %s - %s, %s tks, %s res)" % params 
      
  @property
  def iv_words(self):
    if  self.total_results == 0:
      return dict()
    #if self.total_results != 1:
      #print 'ALARMA DE ARBITRARIEDAD INJUSTIFICADA: esta tomando uno de varios resultados'

    return self.results[0].iv_words

    
  def __str__(self):
    return self.__repr__()

  #def total_iv_word
  
  #generators test
  def result_list(self):
    for each in self.results:
      yield each

  #unset all words with 0.0 as value for iv_words of all IVResults
  def clean_zeros(self):
    for each in self.results:
      each = self.aux_clean_zeros(each)
  
  

  #Takes an IVResults and clean all iv_words with 0.0
  def aux_clean_zeros(self, result):
    res = dict()
    for w,c in result.iv_words.items():
        if c > 0.0:
          res[w] = c
    result.iv_words = res
    return result

  
  def print_results(self):
  
    x = dict()
    for res in self.result_list():
      print "res for ws=%s: %s iv-words " % (res.window_size, len(res.iv_words))
      for w,c in res.iv_words.items():
        print w,c
      
    return x

  @property
  def tokens(self):
    tokenizer_func = getattr(self, 'tokenizer', tokenize)
    return tokenizer_func(self.text)

  @property
  def total_results(self):
    return len(self.results)

  @property
  def total_tokens(self):
    return len(self.tokens)


#textos = TextList("Revolution", True)
#texto = textos.texts[0]