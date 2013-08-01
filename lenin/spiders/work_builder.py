# This Python file uses the following encoding: utf-8
from scrapy import log
from scrapy.selector import HtmlXPathSelector
from lenin.items import LeninWork
from BeautifulSoup import BeautifulStoneSoup
import nltk

class WorkBuilder:
  def __init__(self, response):
    self.response = response
    self.hxs = HtmlXPathSelector(self.response)

  def get_title(self):
    return self.hxs.select('//title/text()').extract()[0]

  def clean_html(self, raw_text):
    clean_text = nltk.clean_html(raw_text)
    contents = BeautifulStoneSoup(clean_text, convertEntities=BeautifulStoneSoup.XML_SPECIAL_CHARS_TO_ENTITIES).contents
    if not contents or len(contents) == 0:
      log.msg( "ALERTA!!!!!!!!!!!", level=log.WARNING)
      log.msg( "%s me da contents nulos " % self.get_title().encode('ascii', 'ignore'), level=log.WARNING)
      log.msg(self.response.url, level=log.WARNING)
    clean_text = contents[0]
    clean_text = clean_text.lower()
    clean_text = clean_text.replace('&#x000a;','\n')

		#clean_text = re.sub(r'&#.+;', r'', clean_text)
    #clean_text = re.sub(r'\\u....', r' ', clean_text)
    return clean_text

  def get_year(self):
    url = self.response.url
    for y in range(1893,1924):
      if url.count(str(y)) > 0:
        return str(y)
    return "ind"

  def get_month(self):
    url = self.response.url
    for m in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
        if url.count(m) > 0 and ( not m == 'mar' or url.count(m) == 2) :
            return m
    return "ind"

  # Método abstracto
  def get_work(self):
    return None


class SimpleWorkBuilder(WorkBuilder):

  def __init__(self, response):
    WorkBuilder.__init__(self, response)

  def get_text(self):
    #paragraphs = self.hxs.select('//p').extract()
    paragraphs = self.hxs.select('//p[not(contains(@class, "information")) and not(contains(@class, "index"))]').extract()
    raw_text = u" ".join(paragraphs)
    return self.clean_html(raw_text)

  def get_work(self ):
    work = LeninWork()
    work['year'] = self.get_year()
    work['month'] = self.get_month()
    work['name'] = self.get_title()
    work['url'] = self.response.url
    work['text'] = self.get_text()

    return work
