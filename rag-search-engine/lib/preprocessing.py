import string
from nltk.stem import PorterStemmer

from lib.data_loader import load_stop_words

STOP_WORDS_DATA = load_stop_words()
TABLE_PUNCTUATION = str.maketrans("", "", string.punctuation)
STEMMER = PorterStemmer()


def preprocess(input: str):
    input = input.lower()
    input = input.translate(TABLE_PUNCTUATION)
    arr = input.split()
    arr = filter(lambda x: x not in STOP_WORDS_DATA, arr)
    arr = map(lambda x: STEMMER.stem(x), arr)

    return list(arr)


def single_token(input: str):
    result = preprocess(input)

    if len(result) != 1:
        raise ValueError("Should only one token")

    return result[0]
