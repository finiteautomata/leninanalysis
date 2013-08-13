#! coding:utf-8
from information_value.models import Document
from includes.factories import BaseFactory


class DocumentFactory(BaseFactory):
    model = Document
    url="http://www.sarasa.com.ar"
    text="sarasa sarasa sarasa sarasa sarasa!"
    name="test02"
    month="Mar"
    year='2013'

