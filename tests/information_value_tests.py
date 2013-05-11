from __future__ import division
from unittest import TestCase
from nltk.corpus import gutenberg
from includes.tokenizer import tokenize
from includes.information_value import InformationValueCalculator

class InformationValueCalculatorTest(TestCase):
    def test_for_moby_dick(self):
        tokens = get_moby_dick_tokens()
        iv_calculator = InformationValueCalculator(tokens)
    # Ocurrence Probability Test
    def test_occurrence_probability_for_single_word_in_vocabulary(self):
        tokens = ["foo", "foo", "foo"]
        iv_calculator = InformationValueCalculator(tokens)

        p_i = iv_calculator.occurrence_probability(window_size=1)
        print "The shit = %s" % p_i
        self.assertItemsEqual(p_i.keys(), ["foo"])

        for i in range(3):
            self.assertAlmostEqual(p_i["foo"][i], 1/3)

    def test_occurrence_probability_for_two_words_in_vocabulary(self):
        tokens = ["foo", "bar"] * 3
        iv_calculator = InformationValueCalculator(tokens)

        p_i = iv_calculator.occurrence_probability(window_size=2)

        self.assertItemsEqual(p_i.keys(), ["foo", "bar"])
        for i in range(3):
            self.assertAlmostEqual(p_i["foo"][i], 1/3)
            self.assertAlmostEqual(p_i["bar"][i], 1/3)

    def test_occurrence_probability_for_null_entropy(self):
        tokens = ["foo"] * 3 + ["bar"] * 3 + ["doe"] * 3
        iv_calculator = InformationValueCalculator(tokens)

        p_i = iv_calculator.occurrence_probability(window_size=3)

        self.assertItemsEqual(p_i.keys(), ["foo", "bar", "doe"])
        for i in range(3):
            self.assertAlmostEqual(p_i["foo"][i], 0)
            self.assertAlmostEqual(p_i["bar"][i], 0)
            self.assertAlmostEqual(p_i["doe"][i], 0)


    def test_entropy_for_single_word_text(self):
        tokens = ["foo", "foo", "foo"]
        iv_calculator = InformationValueCalculator(tokens)

        entropy_dict = iv_calculator.entropy(window_size=1)
        self.assertItemsEqual(entropy_dict.keys(), ["foo"])
        self.assertAlmostEqual(entropy_dict["foo"], 1.0)




def get_moby_dick_tokens():
    moby_dick = gutenberg.raw('melville-moby_dick.txt')
    tokens = tokenize(moby_dick, only_alphanum=True, clean_punctuation=True)
    return tokens

