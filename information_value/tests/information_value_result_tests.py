#! coding: utf-8
# THIS IMPORT MUST BE THE FIRST IN EVERY tests.py FILE
from test import LeninTestCase
from factories import DocumentFactory, InformationValueResultFactory

class InformationValueResultTest(LeninTestCase):

    def test_create_information_value_result_and_sets_iv_sum_correctly(self):
        simple_doc = DocumentFactory()
        iv_result = InformationValueResultFactory(    
            window_size = 200,
            iv_words = {"sarasa" : 1.0},
            document = simple_doc,
            )

        self.assertEquals(iv_result.iv_sum, 1.0)

    def test_calculates_iv_sum_correctly_according_to_passed_threshold(self):
        simple_doc = DocumentFactory()

        iv_result = InformationValueResultFactory(
            iv_words = dict([("w%s" % i,0.001 * i) for i in range(100)]),
            sum_threshold = 0.03
        )

        """
         It should sum the three most valuable words... that's it:
            w99, w98, w97, which its sum is 
            0.099 + 0.098 + 0.097 
        """
        self.assertAlmostEqual(iv_result.iv_sum, 0.099 + 0.098 + 0.097)
    
