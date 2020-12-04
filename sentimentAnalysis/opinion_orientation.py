import re
from .sentimentr import find_opinion_words_sentiment, adversatives



def find_words_between_ow_and_aspect(ow, aspect, sentence):
    """returns all words between the opinion word and the aspect expression"""
    words_between = re.search(rf'{re.escape(ow.name)}(.*?){aspect.name}', sentence.sentence)
    if words_between is None:
        words_between = re.search(rf'{aspect.name}(.*?){re.escape(ow.name)}', sentence.sentence)
    return re.findall(r'\w+', words_between.group(1))


def distance_between_words(ow, aspect, sentence):
    """Calculates the distance between words in a sentence as a number of words between them + 1"""
    if ow.name == aspect.name:
        return 1
    words_between = find_words_between_ow_and_aspect(ow, aspect, sentence)
    return len(words_between) + 1


def adversative_between_ow_and_aspect(ow, aspect, sentence):
    """returns True if there is an adversative between the opinion word and the aspect expression"""
    words_between = find_words_between_ow_and_aspect(ow, aspect, sentence)
    if words_between is not None:
        for word in words_between:
            if word in adversatives:
                return True
    return False


def orientation_to_interval(orientation, strict_interval=False):
    """ Transforms the given orientation value to one of 5 values: -1,-0.5,0,0.5,1 .
        if the strict_interval argument is set to True, the function only returns -1,0,1
    """
    if orientation > 0.5:
        return 1
    elif orientation > 0:
        if strict_interval:
            return 1
        return 0.5
    elif orientation < -0.5:
        return -1
    elif orientation < 0:
        if strict_interval:
            return -1
        return -0.5
    else:
        return 0


def opinion_orientation(review, strict_interval=False):
    """For each sentence in review which contains aspect words, it calculates the oriententation of the sentiment
    towards said aspect """
    for sentence_index in range(len(review.sentences)):
        sentence = review.sentences[sentence_index]
        # checks if number of aspects in a sentence is too high, in which case it would be difficult to asses which
        # OW belongs to which aspect
        if len(sentence.aspects) > 5 or len(sentence.aspects) == 0:
            continue

        for aspect in sentence.aspects:
            orientation = 0
            for ow_index in range(len(sentence.opinion_words)):
                ow = sentence.opinion_words[ow_index]
                # if there is an adversative between the analyzed aspect expression and sentiment expression
                # the opinion word will have no influence on the aspect
                if adversative_between_ow_and_aspect(ow, aspect, sentence):
                    continue
                # calculates the distance between ow and aspect and assigns the orientation as the fraction
                # of the ow sentiment score calculated by sentimentr  and the distance
                distance = distance_between_words(ow, aspect, sentence)
                orientation += (ow.sentiment_score / distance)
            # the sum of influences of different opinion words on the aspect expression
            # is transformed into one of the discrete values
            orientation = orientation_to_interval(orientation, strict_interval)

            # the polarity of the criterion in the sentence is adjusted
            if aspect.criterion in sentence.criterion_orientation.keys():
                sentence.criterion_orientation[aspect.criterion] += orientation
            else:
                sentence.criterion_orientation[aspect.criterion] = orientation
            # if the orientation is not 0 it is added as a score of the criterion to the review
            # otherwise the aspect expression is added to the list of unoriented aspects of the sentence
            if orientation != 0:
                review.add_score(aspect.criterion, orientation)
            else:
                sentence.unoriented_aspects.append(aspect)
        # for each unoriented aspect expression of the sentence, the orientation is first attempted to
        # be determined based on if the aspect is an opinion word itself
        # then based on intra sentence rules
        for aspect in sentence.unoriented_aspects:
            orientation = 0
            ows = find_opinion_words_sentiment(sentence.tokens)
            for ow, pol in ows:
                if ow == aspect.name and aspect.adjective:
                    orientation = pol
                    break

            if orientation == 0:
                orientation = apply_intra_sentence_rules(sentence, aspect)

            orientation = orientation_to_interval(orientation, strict_interval)
            if aspect.criterion in sentence.criterion_orientation.keys():
                sentence.criterion_orientation[aspect.criterion] += orientation
            else:
                sentence.criterion_orientation[aspect.criterion] = orientation
            if orientation != 0:
                review.add_score(aspect.criterion, orientation)


def apply_intra_sentence_rules(sentence, aspect):
    """
    finds the closest opinion word and assigns the aspect expression the orientation based on if there is
    an advesative between them (in which case the orientation is inversed) or not
    """
    if not sentence.opinion_words:
        return 0

    least_words = len(find_words_between_ow_and_aspect(sentence.opinion_words[0], aspect, sentence))
    words_between_aspect_and_closest_ow = []

    for ow in sentence.opinion_words:
        words_between = find_words_between_ow_and_aspect(ow, aspect, sentence)

        if len(words_between) <= least_words:
            words_between_aspect_and_closest_ow = words_between
            closest_ow = ow
            least_words = len(words_between)
    if words_between_aspect_and_closest_ow:
        for word in words_between_aspect_and_closest_ow:
            if word in adversatives:
                return -closest_ow.sentiment_score / len(words_between_aspect_and_closest_ow)
            else:
                return closest_ow.sentiment_score / len(words_between_aspect_and_closest_ow)
    return 0
