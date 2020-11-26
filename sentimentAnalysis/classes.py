from nltk import sent_tokenize, word_tokenize, WordNetLemmatizer, pos_tag, MWETokenizer
import contractions
from .taxonomy import taxonomy
from senticnet.senticnet import SenticNet
from .config import get_wordnet_pos
from .sentimentr import find_opinion_words_sentiment, negators, get_sentiment
import re

sn = SenticNet()

# initialize the tokenizer with a list of MWEs taken from the aspect taxonomy and multi-word sentiment expressions
MWEtokenizer = MWETokenizer(
    [tuple(word_tokenize(aspect)) for aspect in taxonomy.aspects_names if len(aspect.split()) > 1], separator=" ")
MWEtokenizer.add_mwe(("overall", "evaluation"))
for neg in negators:
    tokens = tuple(word_tokenize(neg))
    MWEtokenizer.add_mwe(tokens)


class Review:
    """represents one review with its contents and outputted scores"""

    def __init__(self, file, review):
        self.file_name = file
        self.sentences = []
        for sentence in sent_tokenize(re.sub(r"(?<!\.)\n", ". ", review)):
            self.sentences.append(Sentence(sentence))

        self.criteria = {criterion: CriterionScore(criterion) for criterion in taxonomy.criteria}

    def get_scores(self):
        scores = {}
        for c in self.criteria.values():
            if c.count != 0:
                scores[c.criterion] = round((((c.score / c.count) + 1) / 2) * 4 + 1)
            else:
                scores[c.criterion] = "n/a"
        return scores

    def add_score(self, criterion, value):

        self.criteria[criterion].score += value
        self.criteria[criterion].count += 1

    def print_results(self):
        print(self.file_name)
        for criterion, score in self.get_scores().items():
            print("\t{0:30}  {1}".format(criterion, score))
        print("\n\n")
        for sentence in self.sentences:
            if len(sentence.criterion_orientation) > 0:
                sentence.print_results()


class Sentence:
    """represents a single sentence with its aspect and sentiment expressions"""

    def __init__(self, sentence):
        self.tokens = []
        for w, pos in pos_tag(MWEtokenizer.tokenize(word_tokenize(contractions.fix(sentence).lower()))):
            if not pos.startswith("J"):
                token = WordNetLemmatizer().lemmatize(w, get_wordnet_pos(pos))
            else:
                token = w

            if not (get_sentiment(token) or taxonomy.get_aspects([token])):
                self.tokens.extend(token.split("-"))
            else:
                self.tokens.append(token)
            # self.tokens.append(token)

        self.sentence = " ".join(self.tokens)
        self.sentence_original = sentence
        self.aspects = taxonomy.get_aspects(self.tokens)
        self.opinion_words = []
        self.criterion_orientation = {}
        self.unoriented_aspects = []
        for ow, pol in find_opinion_words_sentiment(self.tokens):
            if not taxonomy.aspect_words_overlap(ow):
                self.opinion_words.append(OpinionWord(ow, pol))

    def print_results(self):
        print("\t", self.sentence_original)
        for criterion, orientation in self.criterion_orientation.items():
            sentiment = "neutral" if orientation == 0 else ("positive" if orientation > 0 else "negative")
            print("\t\t{0:30}  {1}".format(criterion, sentiment))


class OpinionWord:
    """represents a sentiment expression with the score calculated by sentimentr"""

    def __init__(self, word, score):
        self.name = word
        self.sentiment_score = score


class CriterionScore:
    """represent a score for a criterion for a given review"""

    def __init__(self, criterion):
        self.criterion = criterion
        self.score = 0
        self.count = 0
