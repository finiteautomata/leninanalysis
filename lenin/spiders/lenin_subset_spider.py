# coding: utf-8
from scrapy import log
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from work_assembler import WorkAssembler
from work_builder import SimpleWorkBuilder


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
      log.msg(self.lower_regex, level=log.INFO)
      self.upper_regex = r'/archive/lenin/works/(%s).+$' % upper_banned_years
      log.msg(self.upper_regex, level=log.INFO)

    def __init__(self, name=None, **kwargs):
      log.msg(kwargs, level=log.INFO)

      self.min_year = kwargs['min_year'] or 1893
      self.max_year = kwargs['max_year'] or 1924

      log.msg( self.min_year, level=log.INFO)
      log.msg(self.max_year, level=log.INFO)

      self.set_banned_years()
      self.rules += (
        Rule(SgmlLinkExtractor(allow=".+devel.+"), follow=False),
        Rule(SgmlLinkExtractor(allow=self.lower_regex), follow=False),
        Rule(SgmlLinkExtractor(allow=self.upper_regex), follow=False),
        Rule(SgmlLinkExtractor(allow=(self.INDEX_REGEX)), callback='parse_indexed_work'),
        # Si no es ninguna de las anteriores, es una obra y hay que parsearla!
        Rule(SgmlLinkExtractor(allow=(self.CHAPTER_REGEX)), callback='parse_unindexed_work')
      )
      log.msg(self.rules, level=log.INFO)
      # Esto va aca abajo PORQUE SCRAPY ASI LO QUIERE (https://groups.google.com/forum/?fromgroups=#!topic/scrapy-users/Z7PjHuBzmA8)
      CrawlSpider.__init__(self, name)


    def parse_indexed_work(self, response):
      """ This function parses a sample response. Some contracts are mingled
      with this docstring.

      @url http://www.marxists.org/archive/lenin/works/1917/staterev/index.htm
      @returns items 0 0
      @returns requests 8 8
      """
      log.msg("\n*************************************************", level=log.INFO)
      log.msg("Entrando a indice....:"+response.url, level=log.INFO)
      assembler = WorkAssembler(response)
      return assembler.get_requests()

    def parse_unindexed_work(self, response):
      log.msg("\nParseando obra : %s" % response.url, level=log.INFO)
      work = SimpleWorkBuilder(response).get_work()
      log.msg(("Titulo : %s" % work['name'].encode('ascii', 'ignore')), level=log.INFO)
      return work

