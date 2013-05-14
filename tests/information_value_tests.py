from __future__ import division
from unittest import TestCase
import random
from nltk.corpus import gutenberg
from includes.tokenizer import tokenize
from includes.information_value import InformationValueCalculator

class InformationValueCalculatorTest(TestCase):
    """
    Ocurrence Probability Test
    Remember p_i[word][i] stands for the probability of finding w in chapter i, assuming you've already chosen it.
    """
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

    """
    Entropy Tests
    Entropy of a word equals 1 => word homogeneously distributed across the text 
    Entropy of a word equals 0 => word concentred of a single division of text
    """
        

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

    """
    Information Value Tests

    Given a text T, and a random shuffle of T, called R, iv of a word w is the difference of 

    (S_T(w) - S_R(w)) * f(w)

    where S_T(w) is the entropy in T of w, S_R the entropy of w in R, and f(w) the frequency of w in the whole text
    
    This tests are the most odd, as some of them, so they will be purely probabilistic.

    In other cases I will try to do some mocking, so I can control more them.
    """
    def test_iv_for_single_word_text(self):
        tokens = ["foo"] * 100
        iv_calculator = InformationValueCalculator(tokens)

        information_value = iv_calculator.information_value(window_size=10)

        self.assertItemsEqual(information_value.keys(), ["foo"])
        self.assertAlmostEqual(information_value["foo"], 0.0)

    def test_iv_for_very_concentred_word(self):
        tokens = ["foo", "bar", "doe"] * 10 + ["john", "bar"] * 5 + ["foo", "bar", "doe"] * 10
        iv_calculator = InformationValueCalculator(tokens)

        information_value = iv_calculator.information_value(window_size=10)

        print "Iv = %s" % information_value
        self.assertItemsEqual(information_value.keys(), ["foo", "john", "bar", "doe"])
        self.assertNotAlmostEqual(information_value["john"], 0.0)

    XXX = 0.75
    def test_moby_dick_iv(self):
        tokens = get_moby_dick_tokens()[:40000]
        iv_calculator = InformationValueCalculator(tokens)

        res = iv_calculator.get_results()



def get_moby_dick_tokens():
    moby_dick = gutenberg.raw('melville-moby_dick.txt')
    tokens = tokenize(moby_dick, only_alphanum=True, clean_punctuation=True)
    return tokens

