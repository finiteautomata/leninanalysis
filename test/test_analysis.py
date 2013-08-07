from unittest import TestCase

from information_value.analysis import WindowAnalysis

class TestWindowAnalysis(TestCase):

    def test_small_texts_causes_amount_to_be_taken_zero(self):
        iv_words = {u'lenin': 0.0, u'raised': 0.0, u'they': 0.0, u'politbureau': 0.0, u'being': 0.0, u'is': 0.0, u'sent': 0.0, u'period': 0.0, u'case': 0.0, u'single': 0.0, u'are': 0.0, u'questions': 0.0, u'in': 0.00464726704340654, u'writing': 0.0, u'any': 0.01223150409122808, u'pertaining': 0.0, u'absolute': 0.0, u'member': 0.0, u'thursdays': 0.0, u'from': 0.0, u'additional': 0.0, u'no': 0.01223150409122808, u'objection': 0.01223150409122808, u'latter': 0.0, u'outstanding': 0.0, u'brook': 0.0, u'written': 0.0, u'same': 0.01223150409122808, u'should': 0.01223150409122808, u'delay': 0.0, u'to': 0.036291435431524174, u'only': 0.0, u'which': 0.0, u'meeting': 0.0, u'monday': 0.0, u'new': 0.0, u'if': 0.0, u'conditions': 0.0, u'day': 0.0, u'be': 0.0, u'non': 0.0, u'material': 0.0, u'form': 0.0, u'may': 0.0, u'than': 0.0, u'friday': 0.0, u'within': 0.0, u'hours': 0.0, u'meets': 0.0, u'clock': 0.0, u'members': 0.0, u'not': 0.0, u'during': 0.0, u'cases': 0.0, u'with': 0.0, u'by': 0.0, u'condition': 0.0, u'forwarded': 0.0, u'11': 0.0, u'on': 0.04202934687113956, u'regarding': 0.0, u'12': 0.0, u'especially': 0.0, u'waived': 0.0, u'of': 0.0018899855726974587, u'later': 0.0, u'diplomatic': 0.01223150409122808, u'wednesday': 0.0, u'remain': 0.0, u'either': 0.0, u'agenda': 0.0, u'dealt': 0.0, u'following': 0.0, u'the': 0.011664991410230422, u'introduced': 0.01223150409122808, u'where': 0.0, u'or': 0.0, u'urgency': 0.0}
        WindowAnalysis(100, iv_words, 5000)
