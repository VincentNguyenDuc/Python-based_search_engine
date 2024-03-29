import unittest
import re
from pysearch import tokenization

class TokenizationTest(unittest.TestCase):

    STOP_WORDS = set([
        'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by',
        'for', 'if', 'in', 'into', 'is', 'it',
        'no', 'not', 'of', 'on', 'or', 's', 'such',
        't', 'that', 'the', 'their', 'then', 'there', 'these',
        'they', 'this', 'to', 'was', 'will', 'with'
    ])
    PUNCTUATION = re.compile('[~`!@#$%^&*()+={\[}\]|\\:;"\',<.>/?]')


    def test_make_tokens(self):
        self.assertEqual(tokenization.make_tokens('Hello world', self.STOP_WORDS, self.PUNCTUATION), ['hello', 'world'])
        self.assertEqual(tokenization.make_tokens("This is a truly splendid example of some tokens. Top notch, really.", self.STOP_WORDS, self.PUNCTUATION), [
                        'truly', 'splendid', 'example', 'some', 'tokens', 'top', 'notch', 'really'])

    def test_make_ngrams(self):
        self.assertEqual(tokenization.make_ngrams(['hello', 'world']), {
            'hel': [0],
            'hell': [0],
            'hello': [0],
            'wor': [1],
            'worl': [1],
            'world': [1],
        })
        self.assertEqual(tokenization.make_ngrams(['truly', 'splendid', 'example', 'some', 'tokens', 'top', 'notch', 'really']), {
            'tru': [0],
            'trul': [0],
            'truly': [0],
            'spl': [1],
            'sple': [1],
            'splen': [1],
            'splend': [1],
            'exa': [2],
            'exam': [2],
            'examp': [2],
            'exampl': [2],
            'som': [3],
            'some': [3],
            'tok': [4],
            'toke': [4],
            'token': [4],
            'tokens': [4],
            'top': [5],
            'not': [6],
            'notc': [6],
            'notch': [6],
            'rea': [7],
            'real': [7],
            'reall': [7],
            'really': [7],
        })


    def test_hash_name(self):
        self.assertEqual(tokenization.hash_name('hello'), '5d4140')
        self.assertEqual(tokenization.hash_name('world'), '7d7930')
        self.assertEqual(tokenization.hash_name('truly'), 'f499b3')
        self.assertEqual(tokenization.hash_name('splendid'), '291e4e')
        self.assertEqual(tokenization.hash_name('example'), '1a79a4')
        self.assertEqual(tokenization.hash_name('some'), '03d59e')
        self.assertEqual(tokenization.hash_name('tokens'), '25d718')
        self.assertEqual(tokenization.hash_name('top'), 'b28354')
        self.assertEqual(tokenization.hash_name('notch'), '9ce862')
        self.assertEqual(tokenization.hash_name('really'), 'd2d92e')
        self.assertEqual(tokenization.hash_name('notch', length=4), '9ce8')
        self.assertEqual(tokenization.hash_name('really', length=8), 'd2d92eb9')


if __name__ == '__main__':
    unittest.main()