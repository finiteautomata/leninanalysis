from __future__ import division
from unittest import TestCase
import random
from nltk.corpus import gutenberg
from includes.tokenizer import tokenize
from includes.information_value import InformationValueCalculator

class InformationValueCalculatorTest(TestCase):
    # Ocurrence Probability Test
    def test_occurrence_probability_for_single_word_in_vocabulary(self):
        tokens = ["foo", "foo", "foo"]
        iv_calculator = InformationValueCalculator(tokens)

        p_i = iv_calculator.occurrence_probability(window_size=1)
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

    def test_occurrence_probability_for_separated_text(self):
        tokens = ["foo"] * 3 + ["bar"] * 3 + ["doe"] * 3
        iv_calculator = InformationValueCalculator(tokens)

        p_i = iv_calculator.occurrence_probability(window_size=3)

        self.assertItemsEqual(p_i.keys(), ["foo", "bar", "doe"])
        
        # P_i should be 1 only for first chapter
        self.assertAlmostEqual(p_i["foo"][0], 1.0)
        self.assertAlmostEqual(p_i["foo"][1], .0)
        self.assertAlmostEqual(p_i["foo"][2], .0)
        # 1 only for second...
        self.assertAlmostEqual(p_i["bar"][0], 0)
        self.assertAlmostEqual(p_i["bar"][1], 1.0)
        self.assertAlmostEqual(p_i["bar"][2], 0)
        # 1 only for the third
        self.assertAlmostEqual(p_i["doe"][0], .0)
        self.assertAlmostEqual(p_i["doe"][1], .0)
        self.assertAlmostEqual(p_i["doe"][2], 1.0)
        

    def test_entropy_for_single_word_text(self):
        tokens = ["foo", "foo", "foo"]
        iv_calculator = InformationValueCalculator(tokens)

        entropy_dict = iv_calculator.entropy(window_size=1)
        self.assertItemsEqual(entropy_dict.keys(), ["foo"])
        self.assertAlmostEqual(entropy_dict["foo"], 1.0)

    def test_entropy_for_localized_word(self):
        tokens = ["foo"] * 2 + ["bar"] * 6
        iv_calculator = InformationValueCalculator(tokens)

        entropy_dict = iv_calculator.entropy(window_size=2)
        self.assertItemsEqual(entropy_dict.keys(), ["foo", "bar"])
        self.assertAlmostEqual(entropy_dict["foo"], 0.0)

    def test_entropy_for_localized_word(self):
        tokens = ["foo"] * 2 + ["bar"] * 6
        iv_calculator = InformationValueCalculator(tokens)

        entropy_dict = iv_calculator.entropy(window_size=2)
        self.assertAlmostEqual(entropy_dict["foo"], 0.0)

    def test_entropy_calculation_is_stable(self):
        #Fixture
        tokens = ["foo"] * 10000
        iv_calculator = InformationValueCalculator(tokens)
        #Stimulus
        entropy_dict = iv_calculator.entropy(window_size=10)
        #Check
        self.assertAlmostEqual(entropy_dict["foo"], 1.0)

    def test_entropy_for_non_localized_nor_homogeneous_word(self):
        tokens = ["foo", "bar"] * 100 + ["doe"] * 50
        random.shuffle(tokens)

        iv_calculator = InformationValueCalculator(tokens)
        entropy_dict = iv_calculator.entropy(window_size=10)

        self.assertNotAlmostEqual(entropy_dict["doe"], 1.0)
        self.assertNotAlmostEqual(entropy_dict["doe"], 0.0)

def get_moby_dick_tokens():
    moby_dick = gutenberg.raw('melville-moby_dick.txt')
    tokens = tokenize(moby_dick, only_alphanum=True, clean_punctuation=True)
    return tokens

