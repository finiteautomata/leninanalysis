

class Window(object):

    def __init__(self, tokens, window_size, number_of_window):
        self.lower_bound = number_of_window * window_size
        #print 'window iterator size %s nros %s' % (window_size, number_of_window)
        #print 'window iterator low %s upper %s' % (self.lower_bound, self.upper_bound)
        self.current = self.lower_bound
        self.tokens = tokens
        self.total_number_of_tokens = len(self.tokens)
    	self.upper_bound = min(self.total_number_of_tokens, (number_of_window + 1) * window_size)

    def __iter__(self):
        return self

    def next(self):
        if self.current >= self.upper_bound or self.current >= self.total_number_of_tokens:
            raise StopIteration
        else:
            res = self.tokens[self.current]
            self.current += 1
            return res

    def iteritems(self):
        for word in self:
            yield (word, 1)

	#if len(window) < window_size:
	#	window += ['#'] * (window_size-len(window))
	#return window


