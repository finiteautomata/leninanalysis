# coding: utf-8
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from lenin.items import LeninWork
from work_assembler import WorkAssembler
from work_builder import SimpleWorkBuilder
import nltk

class LeninSubsetSpider(CrawlSpider):
    name = "lenin_subset"
    allowed_domains = ["marxists.org"]
    start_urls = [
    "http://www.marxists.org/archive/lenin/by-date.htm"
    ]


    INDEX_REGEX = r'.+/archive/lenin/.*index\.htm$'
    CHAPTER_REGEX = r'.+/archive/lenin/works/\d+/(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec).+\.htm'
    #Estas son las reglas que aplica a cada link que encuentra
    """
    rules = (Rule(SgmlLinkExtractor(allow=".+devel.+"), follow=False),)
    
    rules += (
        Rule(SgmlLinkExtractor(allow=(INDEX_REGEX)), callback='parse_indexed_work'),
        # Si no es ninguna de las anteriores, es una obra y hay que parsearla!
        Rule(SgmlLinkExtractor(allow=(CHAPTER_REGEX)), callback='parse_unindexed_work')
      )
    """
    def set_banned_years(self):
      # Creo dos regex, una que ponga los años banneados a izquierda, y los otros a derecha
      lower_banned_years = "|".join([str(year) for year in range(1893, int(self.min_year))])
      upper_banned_years = "|".join([str(year) for year in range(int(self.max_year)+1, 1924+1)])


      self.lower_regex = r'/archive/lenin/works/(%s).+$' % lower_banned_years
      print self.lower_regex
      self.upper_regex = r'/archive/lenin/works/(%s).+$' % upper_banned_years
      print self.upper_regex

    def __init__(self, name=None, **kwargs):
      print kwargs

      self.min_year = kwargs['min_year'] or 1893
      self.max_year = kwargs['max_year'] or 1924

      print self.min_year
      print self.max_year
      
      self.set_banned_years()
      self.rules += (
        Rule(SgmlLinkExtractor(allow=".+devel.+"), follow=False),
        Rule(SgmlLinkExtractor(allow=self.lower_regex), follow=False),
        Rule(SgmlLinkExtractor(allow=self.upper_regex), follow=False),
        Rule(SgmlLinkExtractor(allow=(self.INDEX_REGEX)), callback='parse_indexed_work'),
        # Si no es ninguna de las anteriores, es una obra y hay que parsearla!
        Rule(SgmlLinkExtractor(allow=(self.CHAPTER_REGEX)), callback='parse_unindexed_work')
      )
      print self.rules
      # Esto va aca abajo PORQUE SCRAPY ASI LO QUIERE (https://groups.google.com/forum/?fromgroups=#!topic/scrapy-users/Z7PjHuBzmA8)
      CrawlSpider.__init__(self, name)
      
  
    def parse_indexed_work(self, response):
      """ This function parses a sample response. Some contracts are mingled
      with this docstring.

      @url http://www.marxists.org/archive/lenin/works/1917/staterev/index.htm
      @returns items 0 0
      @returns requests 8 8
      """
      print "\n*************************************************"
      print "Entrando a indice....:"+response.url
      assembler = WorkAssembler(response)
      return assembler.get_requests()

    def parse_unindexed_work(self, response):
      print "\nParseando obra : %s" % response.url
      work = SimpleWorkBuilder(response).get_work()
      print("Titulo : %s" % work['name'].encode('ascii', 'ignore'))
      return work
     