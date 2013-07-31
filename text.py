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
from information_value.models import Document
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

  def print_texts(self):
    for text in self.texts:
      print text
  
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

  @property
  def short_name(self):
    return self.name.replace("Lenin: ", "")

  def __repr__(self):
    params = ( self.year,
              self.month.capitalize(),
              self.short_name,
              self.total_tokens,
              self.total_results)

    return "Text(%s, %s - %s, %s tokens, %s results)" % params
    #"+str(self.total_results)+" results)"
    
  def __str__(self):
    return self.__repr__()

  def __init__(self, a_document):
    self.doc = a_document

    self._id = unicode(self.doc._id).encode('utf-8')
    self.url = unicode(self.doc.url).encode('utf-8')
    self.name = unicode(self.doc.name).encode('utf-8')
    self.text = unicode(self.doc.text).encode('utf-8')
    self.month = unicode(self.doc.month).encode('utf-8')
    self.year = unicode(self.doc.year).encode('utf-8')
    self.results = self.doc.results

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