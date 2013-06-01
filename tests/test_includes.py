from unittest import TestCase

from includes.tokenizer import is_punctuation, tokenize

class TestTokenizer(TestCase):

    def test_is_punctuation_with_puncts(self):
        for c in "-.'?!,\":;()|-/":
            self.assertTrue(is_punctuation(c))
        self.assertTrue(is_punctuation('""'))
        self.assertTrue(is_punctuation('--'))
        self.assertTrue(is_punctuation(').'))
        self.assertTrue(is_punctuation('.""'))
        self.assertTrue(is_punctuation(''))

    def test_is_punctuation_is_false_for_letters(self):
        self.assertFalse(is_punctuation('a'))

    def test_tokenize_happy_path(self):
        result = tokenize("A written language is the representation of a language by means of a writing system. Written language is an invention in that it must be taught to children; children will pick up spoken language (oral or sign) by exposure without being specifically taught.")

        expected = ['written', 'language', 'is', 'the', 'representation', 'of', 'language', 'by', 'means', 'of', 'writing', 'system', 'Written', 'language', 'is', 'an', 'invention', 'in', 'that', 'it', 'must', 'be', 'taught', 'to', 'children', 'children', 'will', 'pick', 'up', 'spoken', 'language', 'oral', 'or', 'sign', 'by', 'exposure', 'without', 'being', 'specifically', 'taught']

        self.assertEquals(expected, result)

    def test_tokenize_clean_stop_words(self):
        result = tokenize("A written language is the representation of a language by means of a writing system. Written language is an invention in that it must be taught to children; children will pick up spoken language (oral or sign) by exposure without being specifically taught.", clean_stop_words=True)

        expected = ['written', 'language', 'representation', 'language', 'means', 'writing', 'system', 'Written', 'language', 'invention', 'must', 'taught', 'children', 'children', 'pick', 'spoken', 'language', 'oral', 'sign', 'exposure', 'without', 'specifically', 'taught']
        self.assertEquals(expected, result)

    def test_tokenize_clean_punct_false(self):

        result = tokenize("A written language is the representation of a language by means of a writing system. Written language is an invention in that it must be taught to children; children will pick up spoken language (oral or sign) by exposure without being specifically taught.", clean_punctuation=False, only_alphanum=False)

        expected = ['A', 'written', 'language', 'is', 'the', 'representation', 'of', 'a', 'language', 'by', 'means', 'of', 'a', 'writing', 'system', '.', 'Written', 'language', 'is', 'an', 'invention', 'in', 'that', 'it', 'must', 'be', 'taught', 'to', 'children', ';', 'children', 'will', 'pick', 'up', 'spoken', 'language', '(', 'oral', 'or', 'sign', ')', 'by', 'exposure', 'without', 'being', 'specifically', 'taught', '.']

        self.assertEquals(expected, result)

    def test_tokenize_only_alpha(self):
        result = tokenize("123 lalala 123 pepepe 4566 sarasaa", only_alpha = True)
        expected = ['lalala', 'pepepe', 'sarasaa']
        self.assertEquals(expected, result)
