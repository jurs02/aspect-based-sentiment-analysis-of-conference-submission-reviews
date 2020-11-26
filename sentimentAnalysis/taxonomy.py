from aspectExtraction.serialize_taxonomy import load_taxonomy
from nltk.corpus import wordnet


class Taxonomy:
    """ loads the taxonomy generated by the aspectExtraction module"""
    def __init__(self):
        taxonomy_from_json = load_taxonomy()
        self.aspects = {}
        self.aspects_names = []
        self.criteria = []
        for criterion in taxonomy_from_json:
            self.criteria.append(criterion)
            for aspect in taxonomy_from_json[criterion]:
                self.aspects[aspect] = Aspect(criterion, aspect)
                self.aspects_names.append(aspect)

    def get_aspects(self, tokens):
        """returns the aspect expressions found in the supplied token list"""
        aspects = []
        for token in tokens:
            try:
                aspects.append(self.aspects[token])
            except:
                pass
        return aspects

    def aspect_words_overlap(self, word):
        """returns True if the supplied word is an aspect expression"""
        if word in self.aspects_names:
            return True
        return False


class Aspect:
    """represents a single aspect expression"""
    def __init__(self, criterion, aspect):
        self.criterion = criterion
        synsets = wordnet.synsets(aspect)
        self.adjective = any([True if synset.pos() in ["a", "s"] else False for synset in synsets])
        self.name = aspect


taxonomy = Taxonomy()
