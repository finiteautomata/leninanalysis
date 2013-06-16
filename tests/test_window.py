import math
from unittest import TestCase

from includes.tokenizer import tokenize
from nltk.corpus import gutenberg
from information_value.window import Window

class TestWindow(TestCase):

    def test_moby_dick_window(self):
        #just make sure we
        window_sizes = xrange(100, 6000, 100)
        text = gutenberg.raw('melville-moby_dick.txt')
        tokens = tokenize(text, only_alphanum=True, clean_punctuation=True)
        total_number_of_tokens = len(tokens)
        for window_size in window_sizes:
            count = 0
            number_of_windows = int(math.ceil( total_number_of_tokens / window_size))
            for current_window in range(0, number_of_windows+1):
                word_window = Window(tokens, window_size, current_window)
                for word in word_window:
                    count += 1
            self.assertEquals(count, total_number_of_tokens)
