from __future__ import division
import random
import math
from unittest import TestCase, skip
from nltk.corpus import gutenberg
from includes.tokenizer import tokenize
from information_value.calculator import InformationValueCalculator
import information_value.calculator as information_value
from tests import iv_oracle

class InformationValueCalculatorTest(TestCase):
    """ 
    Frequency calculations
    """
    def test_frequency_for_single_word_single_windows(self):
        tokens = ["foo", "foo", "foo"]
        iv_calculator = InformationValueCalculator(tokens)

        freq = iv_calculator.get_frequencies(tokens, window_size=3)

        self.assertItemsEqual(freq.keys(), ["foo"])
        self.assertEqual(len(freq["foo"]), 1)
        self.assertAlmostEqual(freq["foo"][0], 1)


    def test_frequency_for_single_word_many_windows(self):
        tokens = ["foo", "foo", "foo"]
        iv_calculator = InformationValueCalculator(tokens)

        freq = iv_calculator.get_frequencies(tokens, 1)

        self.assertItemsEqual(freq.keys(), ["foo"])
        self.assertEqual(len(freq["foo"]), 3)
        for i in range(3):
            self.assertAlmostEqual(freq["foo"][i], 1)


    def test_frequency_for_many_words_one_window(self):
        tokens = ["one", "two", "three", "four", "five"]
        window_size = 5
        iv_calculator = InformationValueCalculator(tokens)

        freq = iv_calculator.get_frequencies(tokens, window_size=window_size)
        
        self.assertItemsEqual(freq.keys(), tokens)
        for token in tokens:
            self.assertEqual(len(freq[token]), 1)
            self.assertAlmostEqual(freq[token][0], 1/window_size)

    def test_frequency_for_many_words_many_windows(self):
        amount_of_windows = 10
        window_size = 5
        words = ["one", "two", "three", "four", "five"]
        tokens = ["one", "two", "three", "four", "five"] * amount_of_windows
        iv_calculator = InformationValueCalculator(tokens)
        freq = iv_calculator.get_frequencies(tokens, window_size=window_size)
        
        self.assertItemsEqual(freq.keys(), words)
        for token in words:
            self.assertEqual(len(freq[token]), amount_of_windows)
            for window_no in range(amount_of_windows):
                self.assertAlmostEqual(freq[token][window_no], 1/window_size)

    def test_frequency_non_homogeneous_distribution(self):
        words = ["foo", "bar", "doe"]
        window_size = 3
        tokens = ["foo", "foo", "bar", "doe", "bar", "foo", "doe", "doe", "doe"]

        iv_calculator = InformationValueCalculator(tokens)
        freq = iv_calculator.get_frequencies(tokens, window_size=window_size)

        self.assertAlmostEqual(freq["foo"][0], 2/3)
        self.assertAlmostEqual(freq["bar"][0], 1/3)
        self.assertAlmostEqual(freq["doe"][0], 0/3)

        self.assertAlmostEqual(freq["foo"][1], 1/3)
        self.assertAlmostEqual(freq["bar"][1], 1/3)
        self.assertAlmostEqual(freq["doe"][1], 1/3)

        self.assertAlmostEqual(freq["foo"][2], 0)
        self.assertAlmostEqual(freq["bar"][2], 0)
        self.assertAlmostEqual(freq["doe"][2], 1)

    def test_all_frequencies_for_a_given_window_sum_1(self):
        words = ["foo", "bar", "john", "doe", "random"]
        tokens = words * 20
        random.shuffle(tokens)
        window_size = 5
        number_of_windows = int(math.ceil(len(tokens)/window_size))

        iv_calculator = InformationValueCalculator(tokens)
        freq = iv_calculator.get_frequencies(tokens, window_size=window_size)

        
        for window_no in range(number_of_windows):
            sum_for_window = sum([freq[word][window_no] for word in words])
            self.assertAlmostEqual(sum_for_window, 1.0)

    @skip("Not used")
    def test_frequencies_against_oracle(self):
        tokens = get_moby_dick_tokens()
        words = list(set(tokens))
        iv_calculator = InformationValueCalculator(tokens)
        
        freq = iv_calculator.get_frequencies(tokens, window_size=1000)
        freq_oracle = iv_oracle.get_frequencies(tokens, words, window_size=1000)
        for word in words:
            self.assertEqual(len(freq[word]), len(freq_oracle[word]))
            for i in xrange(len(freq[word])):
                if round(freq[word][i]-freq_oracle[word][i], 6) >.0:
                    self.fail("Frequency differs for %s = %s oracle = %s" % (word, freq[word], freq_oracle[word]))



    """
    Ocurrence Probability Test
    Remember p_i[word][i] stands for the probability of finding w in chapter i, assuming you've already chosen it.
    """
    def test_occurrence_probability_for_single_word_in_vocabulary(self):
        tokens = ["foo", "foo", "foo"]
        iv_calculator = InformationValueCalculator(tokens)

        p_i = iv_calculator.occurrence_probability(window_size=1, tokenized_text=tokens)
        self.assertItemsEqual(p_i.keys(), ["foo"])

        for i in range(3):
            self.assertAlmostEqual(p_i["foo"][i], 1/3)

    def test_occurrence_probability_for_two_words_in_vocabulary(self):
        tokens = ["foo", "bar"] * 3
        iv_calculator = InformationValueCalculator(tokens)

        p_i = iv_calculator.occurrence_probability(window_size=2, tokenized_text=tokens)

        self.assertItemsEqual(p_i.keys(), ["foo", "bar"])
        for i in range(3):
            self.assertAlmostEqual(p_i["foo"][i], 1/3)
            self.assertAlmostEqual(p_i["bar"][i], 1/3)

    def test_occurrence_probability_for_separated_text(self):
        tokens = ["foo"] * 3 + ["bar"] * 3 + ["doe"] * 3
        iv_calculator = InformationValueCalculator(tokens)

        p_i = iv_calculator.occurrence_probability(window_size=3, tokenized_text=tokens)

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
    
    @skip("Not used")
    def test_occurrence_probability_against_oracle(self):
        tokens = get_moby_dick_tokens()
        words = list(set(tokens))
        iv_calculator = InformationValueCalculator(tokens)
        
        occ_prob = iv_calculator.occurrence_probability(window_size=1000, tokenized_text=tokens)
        occ_prob_oracle = iv_oracle.get_occurrence_probability(tokens, words, window_size=1000)
        for word in words:
            ours = occ_prob[word]
            theirs= occ_prob_oracle[word]
            self.assertEqual(len(ours), len(theirs))
            for i in xrange(len(ours)):
                if round(ours[i]-theirs[i], 6) >.0:
                    self.fail("occurrence_probability differs for %s = %s oracle = %s" % (word, ours, theirs))
    """
    Entropy Tests
    Entropy of a word equals 1 => word homogeneously distributed across the text 
    Entropy of a word equals 0 => word concentred of a single division of text
    """
        

    def test_entropy_for_single_word_text(self):
        tokens = ["foo", "foo", "foo"]
        iv_calculator = InformationValueCalculator(tokens)

        entropy_dict = iv_calculator.entropy(window_size=1, tokenized_text=tokens)
        self.assertItemsEqual(entropy_dict.keys(), ["foo"])
        self.assertAlmostEqual(entropy_dict["foo"], 1.0)

    def test_entropy_for_localized_word(self):
        tokens = ["foo"] * 2 + ["bar"] * 6
        iv_calculator = InformationValueCalculator(tokens)

        entropy_dict = iv_calculator.entropy(window_size=2, tokenized_text=tokens)
        self.assertItemsEqual(entropy_dict.keys(), ["foo", "bar"])
        self.assertAlmostEqual(entropy_dict["foo"], 0.0)

    def test_entropy_for_localized_word(self):
        tokens = ["foo"] * 2 + ["bar"] * 6
        iv_calculator = InformationValueCalculator(tokens)

        entropy_dict = iv_calculator.entropy(window_size=2, tokenized_text=tokens)
        self.assertAlmostEqual(entropy_dict["foo"], 0.0)

    def test_entropy_calculation_is_stable(self):
        #Fixture
        tokens = ["foo"] * 10000
        iv_calculator = InformationValueCalculator(tokens)
        #Stimulus
        entropy_dict = iv_calculator.entropy(window_size=10, tokenized_text=tokens)
        #Check
        self.assertAlmostEqual(entropy_dict["foo"], 1.0)

    def test_entropy_for_non_localized_nor_homogeneous_word(self):
        tokens = ["foo", "bar"] * 100 + ["doe"] * 50
        random.shuffle(tokens)

        iv_calculator = InformationValueCalculator(tokens)
        entropy_dict = iv_calculator.entropy(window_size=10, tokenized_text=tokens)

        self.assertNotAlmostEqual(entropy_dict["doe"], 1.0)
        self.assertNotAlmostEqual(entropy_dict["doe"], 0.0)
    
    @skip("Not used")
    def test_entropy_against_oracle(self):
        tokens = get_moby_dick_tokens()[:60000]
        words = list(set(tokens))
        iv_calculator = InformationValueCalculator(tokens)

        res = iv_calculator.entropy(window_size=1000, tokenized_text=tokens)
        expected = iv_oracle.get_entropy(tokens, words, 1000)
        
        print "Imprimiendo diferencias entre entropias"
        for word in iv_calculator.words:
            abs_err = res[word]-expected[word]
            if res[word] > .0:
                rel_err = abs_err / res[word]
            if abs_err > .0:
                print "%s has rel_err %s got = %s expected = %s" % (word, rel_err, res[word], expected[word])

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

    @skip("Not used")
    def test_iv_against_oracle(self):        
        tokens = get_moby_dick_tokens()
        iv_calculator = InformationValueCalculator(tokens)

        res = iv_calculator.information_value(window_size=1000)
        expected = iv_oracle.get_iv(tokens, 1000)
        
        test_words = ["whale", "you", "ahab", "is", "ye", "queequeg", 
        "thou", "me", "of", "he", "captain", "boat", "the", "stubb", "his", "jonah", "was", "whales", "my"]
        for word in test_words:
            abs_err = abs(res[word]-expected[word]) 
            rel_err = abs_err / res[word]
            self.assertLessEqual(rel_err, 0.25, "%s has difference %s got = %s expected = %s" % (word, rel_err, res[word], expected[word]))

    window_sizes = range(200, 1500, 100)
    def test_top_words_for_moby_dick(self):
        tokens = get_moby_dick_tokens()

        print information_value.get_optimal_window_size(tokens, self.window_sizes, 20)
    
    @skip("Not used")
    def test_top_words_for_origin(self):
        tokens = get_origin_of_species_tokens()

        print information_value.get_optimal_window_size(tokens, self.window_sizes, 20)

    @skip("Not used")
    def test_top_words_for_analysis_of_the_mind(self):
        tokens = get_analysis_of_the_mind_tokens()

        print information_value.get_optimal_window_size(tokens, self.window_sizes, 20)


def get_moby_dick_tokens():
    moby_dick = gutenberg.raw('melville-moby_dick.txt')
    tokens = tokenize(moby_dick, only_alphanum=True, clean_punctuation=True)
    return [token.lower() for token in tokens]

def get_origin_of_species_tokens():
    with file("tests/origin.txt") as f:
        raw_text = f.read()
        tokens = tokenize(raw_text, only_alphanum=True, clean_punctuation=True)
        return [token.lower() for token in tokens]

def get_analysis_of_the_mind_tokens():
    with file("tests/analysis_of_the_mind.txt") as f:
        raw_text = f.read()
        tokens = tokenize(raw_text, only_alphanum=True, clean_punctuation=True)
        return [token.lower() for token in tokens]
