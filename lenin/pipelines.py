# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log
from pymongo.errors import DuplicateKeyError

from information_value.models import Document
from information_value.models import odm_session

class LeninPipeline(object):
    def process_item(self, item, spider):
        Document(
                name=item['name'],
                url=item['url'],
                text=item['text'],
                month=item['month'],
                year=item['year']
                )
        try:
            odm_session.flush()
        except DuplicateKeyError:
            log.msg('Duplicate found', level=log.WARNING)
        log.msg('Document saved', level=log.INFO)
        return item
