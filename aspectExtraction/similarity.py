from nltk.corpus import wordnet as wn
from nltk import pos_tag, word_tokenize
import re
from aspectExtraction.JJtoN import JJ_to_N

from aspectExtraction.config import get_wordnet_pos


def asymmetric_similarity(term_1, term_2, pos):
    """Returns the similarity between two terms (consisting of 1+ tokens) using wordnet path_similarity"""
    if len(term_1.split()) == 1:
        term_1_synsets = wn.synsets(term_1, pos)
        if pos == wn.ADJ:  # if pos is adjective, we add in synsets of a noun derived from the adjective for better comparison
            term_1_synsets += wn.synsets(JJ_to_N(term_1))
    else:
        token_1_underscored = re.sub(" ", "_", term_1)
        term_1_synsets = wn.synsets(token_1_underscored)

    if len(term_2.split()) == 1:
        term_2_synsets = wn.synsets(term_2, pos)
    else:
        nnp2_us = re.sub(" ", "_", term_2)
        term_2_synsets = wn.synsets(nnp2_us)
    synsets1 = [[synset] for synset in term_1_synsets]
    synsets2 = [synset for synset in term_2_synsets]

    # token_1 or token_2 arent found in wordnet, compare them word by word, with adjectives converted to nouns for similarity measures
    if not synsets1 and len(term_1.split()) > 1:
        synsets1 = [wn.synsets(token, get_wordnet_pos(pos)) if pos != "JJ" else wn.synsets(JJ_to_N(token)) for
                    token, pos in pos_tag(word_tokenize(term_1))]
    if not synsets2 and len(term_2.split()) > 1:
        synsets2 = []
        for synset in [wn.synsets(token, get_wordnet_pos(pos)) if pos != "JJ" else wn.synsets(JJ_to_N(token)) for
                       token, pos in pos_tag(word_tokenize(term_2))]:
            synsets2 += synset

    score = 0
    for synset_group in synsets1:
        for synset1 in synset_group:
            for synset2 in synsets2:
                sim = synset1.path_similarity(synset2)
                if sim is not None and sim > score:
                    score = sim

    return score


def calculate_similarity(frequent_term, aspect, pos):
    """path_similarity is not a symmetrical metric, therefore we choose the maximum of distance(a,b) and
     distance(b,a) """
    return max(asymmetric_similarity(frequent_term, aspect, pos), asymmetric_similarity(aspect, frequent_term, pos))


