#! coding:utf-8
from information_value.models import Document, InformationValueResult
from includes.factories import BaseFactory


class DocumentFactory(BaseFactory):
    model = Document
    url="http://www.sarasa.com.ar"
    text="sarasa sarasa sarasa sarasa sarasa!"
    name="test02"
    month="Mar"
    year='2013'


class InformationValueResultFactory(BaseFactory):
    model = InformationValueResult
    window_size = 100
    iv_words = {
            "sarasa" : 0.01
    }    
