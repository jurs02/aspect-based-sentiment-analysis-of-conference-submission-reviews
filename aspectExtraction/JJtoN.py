from nltk.corpus import wordnet as wn



def JJ_to_N(word):
    """Tries to convert an adjective into a noun,returns an empty string if no similar noun is found"""
    nouns = wn.synsets(word, wn.NOUN)
    if not nouns:
        synsets = wn.synsets(word, pos=wn.ADJ)
        lemmas = [l for s in synsets for l in s.lemmas() if s.name().split('.')[1] in ['a', 's']]
        derivationally_related_forms = [(l.derivationally_related_forms()) for l in lemmas]
        related_noun_lemmas = [l for drf in derivationally_related_forms
                               for l in drf
                               if l.synset().name().split('.')[1] == "n"]
        nouns = list(dict.fromkeys([l.name() for l in related_noun_lemmas]))
        if not nouns:
            return ""
        return nouns[0]
    return nouns[0].lemmas()[0].name()
