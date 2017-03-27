""""
Project 1 for CS 4740
Fred Callaway, Kang-Li Chen
"""
import bisect
from collections import Counter, defaultdict
import itertools
import math
import random
import time
#from typing import Dict

from preprocess import parse_book
from utils import get_text_files


class CounterMatrix(dict):
    """A two dimensional matrix with default 0 values."""
    def __init__(self, tokens):
        super(CounterMatrix, self).__init__()
        
        for i in range(len(tokens) - 1):
            self[tokens[i]][tokens[i+1]] += 1

        print('unique tokens: %s' % len(set(self)))
        self.count_counts = self.get_count_counts()
        self.good_turing_mapping = self.get_good_turing_mapping()
        self.distributions = self.get_distributions()

    def __missing__(self, key):
        self[key] = Counter()
        return self[key]

    def get_count_counts(self) :#-> Dict[str, Dict[int, int]]:
        """The number of bigrams beginning with each token.

        value_counts[token][c] = number of bigrams beginning with token
        that were seen c times"""
        count_counts = defaultdict(Counter)
        for token, followers in self.items():
            for f, count in followers.items():
                count_counts[token][count] += 1
            count_counts[token][0] = len(self) - sum(count_counts[token].values())
        return count_counts

    def get_good_turing_mapping(self, threshold=5) :#-> Dict[int, float]:
        """A dictionary mapping counts to good_turing smoothed counts."""
        total_count_counts = sum(self.count_counts.values(), Counter())
        def good_turing(c): 
            return (c+1) * (total_count_counts[c+1]) / total_count_counts.get(c, 1)
        gtm = {c: good_turing(c) for c in range(threshold)}
        return {k: v for k, v in gtm.items() if v > 0}  # can't have 0 counts

    def get_distributions(self):
        """Returns next-token probability distributions for each token.

        distributions['the'].sample() gives words likely to occur after 'the'"""
        return {token: Distribution(self[token], self.count_counts[token], 
                                    smoothing_dict=self.good_turing_mapping)
                for token in self}


class Distribution(object):
    """A statistical distribution based on a dictionary of counts."""
    def __init__(self, counter, count_counts, smoothing_dict={}):
        assert 0 in count_counts

        self.counter = counter
        self.smoothing_dict = smoothing_dict

        # While finding the total, we also track each
        # intermediate total to make sampling faster.
        self._acc_totals = list(itertools.accumulate(counter.values()))
        self.total = self._acc_totals[-1]
        self.items = list(self.counter.keys())

        # Smoothing only applies to surprisal, not sampling so we maintain
        # a separate total that accounts for the smoothed counts
        self.smooth_total = sum(smoothing_dict.get(count, count) * N_count 
                                      for count, N_count in count_counts.items())

    def sample(self):
        """Returns an element from the distribution.

        Based on ideas from the following article:
        http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python"""
        rand = random.random() * self.total

        # Perform a binary search for index of highest number below rand.
        # index will thus be chosen with probability =
        # (self._acc_totals[i] - self._acc_totals[i-1]) / self.total
        index = bisect.bisect_right(self._acc_totals, rand)
        return self.items[index]
    
    def surprisal(self, item):
        """The negative log probability of an item being sampled."""
        count = self.counter[item]
        smooth_count = self.smoothing_dict.get(count, count)
        return - math.log(smooth_count / self.smooth_total)


class BigramModel(object):
    """A bigram language model."""
    def __init__(self, tokens, smoothing=False):
        self.tokens = tokens
        self.smoothing = smoothing
        self.words_Seen = set()
        for i in range(len(self.tokens)):
                word = self.tokens[i]
                if word not in self.words_Seen and word != '<s>':
                    self.tokens[i] = 'UNKNOWN_TOKEN'
                self.words_Seen.add(word)

        self.cooccurrence_matrix = CounterMatrix(self.tokens)           

    def predict_next(self, token) :#-> str:
        """Returns a token from distribution of tokens that follow the given token."""
        return self.cooccurrence_matrix.distributions[token].sample()

    def surprisal(self, token: str, follower: str):
        """Returns the negative log probability of `follower` following `token`

        -log p(follower_i | token_{i-1})"""
        try:    
            dist = self.cooccurrence_matrix.distributions[token]
        except KeyError:
            dist = self.cooccurrence_matrix.distributions['UNKNOWN_TOKEN']
        return dist.surprisal(follower)
        

    def generate_sentence(self, initial="") -> str:
        """Returns a randomly generated sentence.

        Optionally, the beginning of the sentence is given."""
        words = initial.split()
        if not words:
            words.append(self.predict_next('SENTENCE_BOUNDARY'))
        for i in range(30):  # 30 is max sentence length
            next_word = self.predict_next(words[-1])
            if next_word == 'SENTENCE_BOUNDARY':
                break
            else:
                words.append(next_word)
            if i == 29:
                words.append('...')

        return ' '.join(words) + '\n'

    def perplexity(self, tokens):
        """Average surprisal or something."""
        first_surprisal = self.surprisal('SENTENCE_BOUNDARY', tokens[0])
        total_surprisal = first_surprisal + sum(self.surprisal(tokens[i], tokens[i+1])
                                                for i in range(len(tokens) - 1))

        return math.exp(total_surprisal / (len(tokens)))


def get_corpus(subject, test=False):


    test_files=get_text_files('books/%s_books/%s' 
                              % ('test' if test else 'train', subject))
    tokenized_books2= [parse_book(af) for af in test_files  ]
    corpus= [token for tt in tokenized_books2 for token in tt]
    return corpus

def classify(genre):

    bm = BigramModel(get_corpus(genre, test=False))
    history=(bm.perplexity(get_corpus('history', test=True)))
    crime=(bm.perplexity(get_corpus('crime', test=True)))
    children=(bm.perplexity(get_corpus('children', test=True)))
   
    perplexities=[history, crime, children]
    
def main():
    #train_files = get_text_files('books/train_books/crime')
    #tokenized_books = [parse_book(tf) for tf in train_files]
    #training_corpus = [token for tb in tokenized_books for token in tb]
    #training_corpus = training_corpus


    bm = BigramModel(get_corpus('crime', test=False))#training 
    
    #print(bm.generate_sentence('A'))
   # print(bm.generate_sentence())
    #print(bm.generate_sentence('I'))

    
    # lower perplexity because overfitting
    #bm = BigramModel(training_corpus[-1000:]) #last thousand
    #print(bm.perplexity(training_corpus[-1000:]))
    

def test():
    tokens = 'the dog . the cat . a cat . the dog the dog the dog the dog'.split()
    bm = BigramModel(tokens)
    print(bm.surprisal('the', 'dog'))
    print(bm.surprisal('cat', '.'))
    print(bm.surprisal('the', '.'))



"""
a dog bit a

"""


""" 
We have them the signal for a large proportion of stories about in the
city of Clodius , the administrator of peoples , fought with liabilities
through the battle-field .

THEODORIC THE VISIGOTH ( Velleius Paterculus , distinguished for reform , time
; but the south , and effeminate youths of the stories about 200 horse born
free men , few ...

Clovis resolved to the greatest ages of sixty without result would be struck
the Nile , devoured by speaking , where the agrarian law were made himself had
a collective : ...

At this the translators render itself , p.

Enviously, she cried out their fortune ; [ 1091 ] The Carthaginians were the
affairs of the governing and bitter period , _Cæsar_ , and Antemnæ , did a
tender his son Edward . ...

Lurking in the shadows , _Topogr .

She paints Roman colonies -- Festus , which , _Letters to contest if one hand
was led his rival .
"""


if __name__ == '__main__':
    print('\n\n')
    main()
    #test()