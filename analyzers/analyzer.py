

class DocumentAnalyzer(object):

  def __init__(self, document):
    self.document = document
    self.top_words = document.top_words()

  def get_results(self):
    pass

  def judge_word(self, word):
    pass

