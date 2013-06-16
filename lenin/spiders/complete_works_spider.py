# coding: utf-8
from scrapy import log
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from lenin.spiders.work_assembler import WorkAssembler
from lenin.spiders.work_builder import SimpleWorkBuilder


class CompleteWorksSpider(CrawlSpider):
    name = "complete_works"
    allowed_domains = ["marxists.org"]
    start_urls = [
    "https://www.marxists.org/archive/lenin/works/cw/"
    ]

    VOLUME_INDEX = r'.+volume\d\d\.htm?$'
    INDEX_REGEX = r'.+/archive/lenin/.*index\.htm$'
    CHAPTER_REGEX = r'.+/archive/lenin/works/.+/(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec).+\.htm'
    #Estas son las reglas que aplica a cada link que encuentra
    rules = (
      Rule(SgmlLinkExtractor(allow=".+devel.+"), callback='nada'),
      Rule(SgmlLinkExtractor(allow=VOLUME_INDEX), callback='parse_volume'),
      # Idem si es un indice (de una obra)
      Rule(SgmlLinkExtractor(allow=(INDEX_REGEX)), callback='parse_indexed_work'),
      # Si no es ninguna de las anteriores, es una obra y hay que parsearla!
      Rule(SgmlLinkExtractor(allow=(CHAPTER_REGEX)), callback='parse_unindexed_work')
    )

    def nada(self, response):
      log.msg( "llame nada" + response.url, level=log.WARNING)
      pass

    def parse_volume(self, response):
      log.msg("Parsing volume %s\n" % response.url, level=log.INFO)

    def parse_indexed_work(self, response):
      """ This function parses a sample response. Some contracts are mingled
      with this docstring.

      @url http://www.marxists.org/archive/lenin/works/1917/staterev/index.htm
      @returns items 0 0
      @returns requests 8 8
      """
      log.msg("*************************************************", level=log.INFO)
      log.msg("Entrando a indice....:"+response.url, level=log.INFO)
      assembler = WorkAssembler(response)
      return assembler.get_requests()

    def parse_unindexed_work(self, response):
      log.msg("Parseando obra : %s" % response.url, level=log.INFO)
      work = SimpleWorkBuilder(response).get_work()
      log.msg("Titulo : %s" % work['name'].encode('ascii', 'ignore'), level=log.INFO)
      return work
