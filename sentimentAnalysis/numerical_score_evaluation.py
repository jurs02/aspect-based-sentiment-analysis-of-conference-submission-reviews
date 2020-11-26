import os
from .classes import Review
from .opinion_orientation import opinion_orientation
import re
"""This script serves to compare the numerical output of the sentiment analysis algorithm to the numerical scores
    in ISWC 2018 reviews."""


iswc18_mae = {
    'relevance': 0,
    'novelty': 0,
    'technical quality': 0,
    'state of the art': 0,
    'evaluation': 0,
    'presentation': 0,

}
iswc18_missings = {
    'relevance': 0,
    'novelty': 0,
    'technical quality': 0,
    'state of the art': 0,
    'evaluation': 0,
    'presentation': 0,

}
iswc18_mapping = {
    'relevance': {
        'APPROPRIATENESS',
    },
    'novelty': {
        'ORIGINALITY / INNOVATIVENESS',
        'IMPACT OF IDEAS AND RESULTS',
    },
    'technical quality': {
        'IMPLEMENTATION AND SOUNDNESS',
    },
    'state of the art': {
        'RELATED WORK',
    },
    'evaluation': {
        'EVALUATION',
    },
    'presentation': {
        'CLARITY AND QUALITY OF WRITING',
    },

}


def min_max_normalization(value, min=1, max=5, new_min=-2, new_max=2):
    """normalizes the outputted values from the original 1 to 5 range to the -2 to 2 range of ISWC 2018 reviews"""
    return round((((value - min) / (max - min)) * (new_max - new_min)) + new_min)




def mae(reviews):
    """calculates the mean absolute error between the outputted scores and scores from the reviews"""
    iswc18_mae_overall = 0

    for review, real_scores in reviews:
        output_scores = review.get_scores()
        for criterion in iswc18_mapping.keys():
            if output_scores[criterion] == "n/a":
                iswc18_missings[criterion] += 1
                continue
            iswc18_mae[criterion] += abs((real_scores[criterion] - min_max_normalization(output_scores[criterion])))

    for criterion, mae in iswc18_mae.items():
        iswc18_mae[criterion] = mae / (len(reviews) - iswc18_missings[criterion])
        iswc18_mae_overall+=iswc18_mae[criterion]
    return iswc18_mae_overall/len(iswc18_mae.keys())

def get_numerical_scores(content):
    """uses the specific structure of ISWC 2018 reviews to extract numerical scores of criteria"""
    scores = {}
    for criterion, iswc_names in iswc18_mapping.items():
        c_score = 0
        for name in iswc_names:
            p = re.compile(f"{name}:\s*\n(-?\d)")
            score = int(p.search(content).group(1))
            c_score += score
        scores[criterion] = c_score / len(iswc_names)
    return scores


path = "test_data/iswc18/"
path = os.path.join(os.path.dirname(__file__), path)
reviews = []
for file in os.listdir(path):
    if os.path.isfile(os.path.join(path, file)) and not file.startswith("."):
        f = open(os.path.join(path, file), 'r', encoding="ISO-8859-1")
        content = f.read()
        r = Review(file, content)
        opinion_orientation(r, False)
        reviews.append((r, get_numerical_scores(content)))

iswc18_mae_overall=mae(reviews)
for c in iswc18_mae.keys():
    print("{}:".format(c))
    print("\tMean absolute error: {}".format(round(iswc18_mae[c], 2)))
    print("\tNumber of missing scores: {} out of {}".format(iswc18_missings[c], len(reviews)))
print("Overall MAE: {}".format(round(iswc18_mae_overall,2)))