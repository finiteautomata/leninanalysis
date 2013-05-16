import nltk
import re
def tokenize(raw_text, filters):
  #Primero hay que separar en sentencias
  tokens = [token.lower() for token in nltk.wordpunct_tokenize(raw_text) if re.match('\w+', token) and len(token) > 1]

  return filter(lambda t: all(f(t) for f in filters), tokens) 
  
class Tokenizer:
  def __init__(self, text):
    self.text = text
    self.tokens = []
    self.fdist = 0
    self.filters = []

  def add_filter(self, a_filter):
    self.filters.append(a_filter)

  def get_words(self):
    if len(self.tokens) == 0:
      self.tokens = tokenize(self.text, self.filters)
    return self.tokens

  def get_fdist(self):
    if self.fdist == 0:
      self.get_words()
      self.fdist = nltk.FreqDist(self.tokens)
    return self.fdist
 