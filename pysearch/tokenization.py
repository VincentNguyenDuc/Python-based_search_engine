import re
import hashlib

STOP_WORDS = set([
       'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by',
       'for', 'if', 'in', 'into', 'is', 'it',
       'no', 'not', 'of', 'on', 'or', 's', 'such',
       't', 'that', 'the', 'their', 'then', 'there', 'these',
       'they', 'this', 'to', 'was', 'will', 'with'
   ])
PUNCTUATION = re.compile('[~`!@#$%^&*()+={\[}\]|\\:;"\',<.>/?]')

def make_tokens(blob: str, STOP_WORDS=STOP_WORDS, PUNCTUATION=PUNCTUATION) -> list:
    """
    Given a string of text, return a list of tokens
    """
    blob = PUNCTUATION.sub(' ', blob)
    tokens = []

    # Split on spaces
    for token in blob.split():
        token = token.lower().strip()
        if token not in STOP_WORDS:
            tokens.append(token)

    return tokens


def make_ngrams(tokens: list, min_gram=3, max_gram=6):
    """Convert a iterable of tokens into n-grams

    Args:
        min_gram (int, optional): the minimum gram length. Defaults to 3.
        max_gram (int, optional): the maximum gram length. Defaults to 6.
    """
    terms = {}

    for position, token in enumerate(tokens):
        for window_length in range(min_gram, min(max_gram + 1, len(token) + 1)):
            gram = token[:window_length]
            terms.setdefault(gram, [])

            if position not in terms[gram]:
                terms[gram].append(position)

    return terms


def hash_name(term, length=6):
    """
        Hash the term and returns a string of the first N letters
    """
    encoded_term = term.encode('ascii', errors='ignore')
    hashed_term = hashlib.md5(encoded_term).hexdigest()
    return hashed_term[:length]


if __name__ == '__main__':

    blob = 'Hello, My name is vincent'

    # EXECUTE
    tokens = make_tokens(blob)
    terms = make_ngrams(tokens)
    print(tokens)
    print(terms)
