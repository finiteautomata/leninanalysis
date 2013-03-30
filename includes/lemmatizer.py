import nltk
from nltk.corpus.reader.wordnet import POS_LIST
from nltk.corpus import stopwords

wnl = nltk.WordNetLemmatizer()

class Lemmatizer:
  def __init__(self, text):
    self.text = text
    self.stems = []
    self.fdist = 0


  def pos2wn(self, pos):
      if pos == 'JJ':
          return 'a'
      elif pos[0].lower() in set(POS_LIST):
          return pos[0].lower()
      else:
          return 'n'

  def lemmatize_sentence(self, sentence):
    stem_words = []
    tokens = nltk.wordpunct_tokenize(sentence)
    pos_tagged = nltk.pos_tag(tokens)
    for (w,p) in pos_tagged:
      stem_words.append(wnl.lemmatize(w,self.pos2wn(p)).lower())
    return stem_words

  def process_sentence(self, sentence):
    lemmas = self.lemmatize_sentence(sentence)

    english_stopwords = stopwords.words('english')
    non_stopword_lemmas = filter(lambda x: (not x in english_stopwords) and len(x)> 1, lemmas)
    self.stems.extend(non_stopword_lemmas)

    return lemmas

  def parse_text(self):
    sentences = nltk.sent_tokenize(self.text)
    for sentence in sentences:
      self.process_sentence(sentence)
    return self.stems

  def get_words(self):
    if len(self.stems) == 0:
      self.parse_text()
    return self.stems

  def get_fdist(self):
    if self.fdist != 0:
      self.get_stems()
      self.fdist = nltk.FreqDist(self.stems)
    return self.fdist
 