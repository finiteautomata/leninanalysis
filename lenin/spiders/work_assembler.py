# coding: utf-8
import re
from work_builder import SimpleWorkBuilder, WorkBuilder
from scrapy import log
from scrapy.http import Request
from lenin.items import LeninWork


class WorkAssembler(WorkBuilder):
  def __init__(self, response, parent=None):
    WorkBuilder.__init__(self, response)
    self.parent = parent

  def create_callback_for_chapter(self, i):
    return lambda aResponse:self.chapter_received(aResponse, i)


  def is_url_from_same_work(self, link):
    if link[:2] == '..':
      return False
    return True


  def get_requests(self):
    # Saco todos los links que haya debajo de alguna table (Esperemos que todos tengan este formato... :-D)
    # PD: Esto no ocurrio
    all_links = self.hxs.select("//table//a/@href").extract()
    # Todos los adhocs para cada tipo de indice distinto que encontramos
    all_links.extend(self.hxs.select("//p[contains(@class, 'contents') or contains(@class, 'toc') or contains(@class, 'index')]//a/@href").extract())

    log.msg( ("===== %s ======"  % unicode(self.get_title())).encode('ascii', 'ignore'), level=log.INFO)
    log.msg("URL = %s" % self.response.url, level=log.INFO)
    log.msg((u"Primeros links... %s " % unicode(all_links)).encode('ascii', 'ignore'), level=log.INFO)
    our_links = filter(lambda link: self.is_url_from_same_work(link), all_links)
    our_links = [link.rsplit('#')[0] for link in our_links]

    links = []
    for link in our_links:
      if not link in links:
        links.append(link)


    log.msg( (u"Segundos links... %s" % unicode(links)).encode('ascii', 'ignore'), level=log.INFO)
    # Saco el directorio de la obra en cuestión...
    base_url = self.response.url.rpartition('/')[0] + '/'

    self.chapters = [None] * len(links)

    self.requests = []
    for i, link in enumerate(links):
      #ésto es para evitar el problema de la última referencia (si creo la lambda a mano referenciando a i, cuando llame va a ser siempre el último valor)
      self.requests.append(Request(base_url+link, callback=self.create_callback_for_chapter(i)))
    #return self.requests
    return []

  def get_text(self):
    #Esto hace el join respetando el orden de los capitulos?
    ret = u""
    for chapter in self.chapters:
      ret += u"\n Capitulo %s \n" % chapter['name']
      ret += chapter['text']
    return ret

  def get_work(self):
    work = LeninWork()
    work['year'] = self.get_year()
    work['month'] = self.get_month()
    work['name'] = self.get_title()
    work['url'] = self.response.url
    work['text'] = self.get_text()

    return work

  def process_simple_chapter(self, response, number):
    partial_work = SimpleWorkBuilder(response).get_work()
    self.chapters[number] = partial_work

    #log.msg( u"%s obtuvo capítulo %d de %d" %(self.get_title(), number, len(self.chapters)), level=log.INFO)
    if (all(chapter != None for chapter in self.chapters)):
      #log.msg(u'%s todos los capitulos!' %(self.get_title()), level=log.INFO)
      work = self.get_work()
      #log.msg(work['text'].encode('ascii', 'ignore'), level=log.INFO)
      return work
    else:
      return None

  def chapter_received(self, response, number):
      # Si me llego un capitulo...que en realidad es un índice...
      if (re.match(INDEX_REGEX,response.url)):
          log.msg("ALERTA: Parseando %s" % self.get_title(), level=log.WARNING)
          log.msg("ALERTA: me llegó un capítulo que es un INDICE = "+response.url, level=log.WARNING)
      else:
          return self.process_simple_chapter(response, number)
