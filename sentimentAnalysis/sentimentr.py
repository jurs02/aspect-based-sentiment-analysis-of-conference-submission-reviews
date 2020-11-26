import re
import pandas as pd
import os
"""
    this is a custom implementation of the sentimentr algorithm
    the original algorithm can be found here https://github.com/trinker/sentimentr
"""
lexicon_dir = os.path.dirname(__file__)
negators = [line.rstrip('\n') for line in open(os.path.join(lexicon_dir, 'lexicons/negators.txt'))]
amplifiers = [line.rstrip('\n') for line in open(os.path.join(lexicon_dir, 'lexicons/amplifiers.txt'))]
deamplifiers = [line.rstrip('\n') for line in open(os.path.join(lexicon_dir, 'lexicons/deamplifiers.txt'))]
adversatives = [line.rstrip('\n') for line in open(os.path.join(lexicon_dir, 'lexicons/adversatives.txt'))]
lexicon = pd.read_csv(os.path.join(lexicon_dir, "lexicons/sentiment_lexicon_eswc.csv"))
lexicon = lexicon.set_index('word')
pauses = [":", ",", ";"]


def get_sentiment(word):
    try:
        return int(lexicon.loc[word, 'sentiment'])
    except:
        return 0


class pccValues:
    def __init__(self):
        self.neg = self.amp = self.deamp = self.advL = self.advR = 0


class Word:
    def __init__(self, word):
        self.word = word

        self.pol = get_sentiment(word) if get_sentiment(word) else 0
        self.pause = True if (word in pauses) else False
        self.neg = True if (word in negators) else False
        self.amp = True if (word in amplifiers) else False
        self.deamp = True if (word in deamplifiers) else False
        self.adv = True if (word in adversatives) else False


def get_words(sent):
    """returns a list of words in a given sentence"""
    clean = re.sub('[^a-z\s,:;]+', '', sent.lower())
    clean_split = re.split('(\W)', clean)
    words = []
    for w in clean_split:
        if w != ' ' and w != '': words += [Word(w)]
    return words


def eval_word(word, values, side):
    if word.neg and side == "L": values.neg += 1
    if word.amp: values.amp += 1
    if word.deamp: values.deamp += 1
    if word.adv and side == "L": values.advL += 1
    if word.adv and side == "R": values.advR += 1


def left_side(left, values):
    for w in left:
        if w.pause: break
        eval_word(w, values, "L")


def right_side(right, values):
    for w in right:
        if w.pause: break
        eval_word(w, values, "R")


def find_opinion_words_sentiment(tokens):
    """Returns a list of tuples (word, sentiment)"""
    words = [Word(token) for token in tokens]
    ow_pol = []
    for i, w in enumerate(words):
        if w.pol:
            values = pccValues()
            if 0 < i < 2:
                left_side([words[i - 1]], values)
            elif i > 1:
                left_side([words[i - 1], words[i - 2]], values)
            right_side(words[i + 1:i + 5], values)
            neg = values.neg % 2
            amp = (1 - neg) * 0.85 * values.amp
            deamp = 0.85 * values.deamp + neg * values.amp
            advcon = 1 + 0.85 * (values.advL - values.advR)
            ow_pol.append((w.word, w.pol * ((-1) ** neg) * (1 + amp + deamp) * advcon))
    return ow_pol


def find_aspect_expression_sentiment(tokens):
    """Returns a list of tuples (word, sentiment)"""
    words = [Word(token) for token in tokens]
    ow_pol = []
    for i, w in enumerate(words):
        w.pol = 1
        if w.pol:
            values = pccValues()
            if 0 < i < 2:
                left_side([words[i - 1]], values)
            elif i > 1:
                left_side([words[i - 1], words[i - 2]], values)
            right_side(words[i + 1:i + 5], values)
            neg = values.neg % 2
            amp = (1 - neg) * 0.85 * values.amp
            deamp = 0.85 * values.deamp + neg * values.amp
            advcon = 1 + 0.85 * (values.advL - values.advR)
            ow_pol.append((w.word, w.pol * ((-1) ** neg) * (1 + amp + deamp) * advcon))
    return ow_pol
