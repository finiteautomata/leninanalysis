from unittest import TestCase
import pymongo
from tests import LeninTestCase
from pymongo.errors import DuplicateKeyError
from information_value.models import odm_session
from information_value.models import Document
from information_value.models import InformationValueResult


class TestModels(LeninTestCase):

    def test_simple_document_pesistence(self):
        simple_doc = Document(
                url="http://www.sarasa.com.ar",
                text="sarasa sarasa sarasa sarasa sarasa!",
                name="test01",
                month="Mar",
                year=2013
                )
        odm_session.flush()
        from_db = Document.query.get(name="test01")
        self.assertEquals(simple_doc.name, from_db.name)
        self.assertEquals(simple_doc.text, from_db.text)
        self.assertEquals(simple_doc.url, from_db.url)
        self.assertEquals(simple_doc.month, from_db.month)
        self.assertEquals(simple_doc.year, from_db.year)

    def test_simple_iv_result_persistence(self):
        simple_doc = Document(
                url="http://www.sarasa.com.ar",
                text="sarasa sarasa sarasa sarasa sarasa!",
                name="test02",
                month="Mar",
                year=2013
                )
        InformationValueResult(
                window_size=500,
                document=simple_doc,
                results=[]
                )

        odm_session.flush()
        from_db = InformationValueResult.query.find({"document_id":simple_doc._id}).first()
        self.assertEquals(from_db.window_size, 500)
        self.assertEquals(from_db.document, simple_doc)
        self.assertEquals(from_db.results, [])

    def test_duplicate_result_raises_exception(self):
        simple_doc = Document(
                url="http://www.sarasa.com.ar",
                text="sarasa sarasa sarasa sarasa sarasa!",
                name="test02",
                month="Mar",
                year=2013
                )
        InformationValueResult(
                window_size=500,
                document=simple_doc,
                results=[]
                )

        odm_session.flush()
        with self.assertRaises(DuplicateKeyError):
            InformationValueResult(
                window_size=500,
                document=simple_doc,
                results=[]
                )
            odm_session.flush()
        count = InformationValueResult.query.find({"document_id":simple_doc._id}).count()
        self.assertEquals(count, 1)
