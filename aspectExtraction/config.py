from nltk.corpus import wordnet as wn

ASPECT_TAXONOMY = {
    'relevance': {
        'appropriateness',
        'relevance'
    },
    'novelty': {
        'originality',
        'innovativeness',
        'innovation',
        'novelty of contribution',
        'novelty',
        'impact',
        'significance'
    },
    'technical quality': {
        'scientific quality',
        'implementation',
        'soundness',
        'technical quality'
    },
    'state of the art': {
        'scholarship',
        'references',
        'related work',
        'state of the art'
    },
    'evaluation': {
        'reproducibility',
        'evaluation',
        'evaluating',
        'evaluate'
    },
    'presentation': {
        'clarity',
        'quality of writing',
        'presentation',
        'typo',
        'description',
        'describe',
        'written'
    },
}

ASPECT_TAXONOMY_CANDIDATES = {
    'relevance': set(),
    'novelty': set(),
    'technical quality': set(),
    'state of the art': set(),
    'evaluation': set(),
    'presentation': set(),
}

MINSUP = 0.02


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
