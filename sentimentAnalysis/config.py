from nltk.corpus import wordnet as wn

ASPECT_TAXONOMY_CANDIDATES = {
    'relevance': 0,
    'novelty': 0,
    'technical quality': 0,
    'state of the art': 0,
    'evaluation': 0,
    'significance': 0,
    'presentation': 0,
}


def get_wordnet_pos(pos_tag):
    if pos_tag.startswith('J'):
        return wn.ADJ
    elif pos_tag.startswith('V'):
        return wn.VERB
    elif pos_tag.startswith('N'):
        return wn.NOUN
    elif pos_tag.startswith('R'):
        return wn.ADV
    else:
        return wn.NOUN
