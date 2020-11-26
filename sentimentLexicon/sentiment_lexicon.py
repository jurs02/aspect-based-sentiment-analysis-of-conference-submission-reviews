import pandas as pd
import nltk
from nltk import WordNetLemmatizer, pos_tag_sents
from sentimentAnalysis.config import get_wordnet_pos
import contractions
import csv
import os
stopwords = ["the", "be", "of", "a", "to", "and", "in", "it", "i", "this", "that", "do", "for", "on", "have"]


def document_features(document, word_features):
    """returns the terms in document which belong to the list of frequent word_features"""
    document_words = set(
        [WordNetLemmatizer().lemmatize(token, get_wordnet_pos(pos)) if not pos.startswith('J') else token.lower() for
         token, pos in document])
    features = {}
    for word in word_features:
        features[word] = (word in document_words)
    return features


def show_most_informative_features_in_list(classifier, n=10):
    """
    Return a nested list of the "most informative" features
    used by the classifier along with it's predominant labels
    """
    cpdist = classifier._feature_probdist  # probability distribution for feature values given labels
    feature_list = {}
    for (fname, fval) in classifier.most_informative_features(n):
        def labelprob(label):
            return cpdist[label, fname].prob(fval)

        labels = sorted([l for l in classifier._labels if fval in cpdist[l, fname].samples()],
                        key=labelprob)
        ratio = (cpdist[labels[-1], fname].prob(fval) / cpdist[labels[0], fname].prob(fval))
        if ratio >= 2.4:
            if fval:
                feature_list[fname] = 1 if labels[-1] == "positive" else -1
            else:
                feature_list[fname] = 1 if labels[0] == "positive" else -1
    return feature_list


def create_lexicon(num_of_words):
    """Extracts sentiment words using the Naive Bayes algorithm anda dataset of a 1000 sentences with labeled sentiment
    Saves the resulting sentiment lexicon into sentimentAnalysis/lexicons/sentiment_lexicon_eswc.csv
    """
    data = pd.read_csv(os.path.join(os.path.dirname(__file__),"eswc19_labeled_sentiment.csv"))
    data.sample(frac=1)
    data["text"] = pos_tag_sents(data["text"].apply(contractions.fix).apply(nltk.word_tokenize).tolist())
    all_words = []
    for tokens in data["text"]:
        for w, pos in tokens:
            if not pos.startswith('J'):
                word = WordNetLemmatizer().lemmatize(w.lower(), get_wordnet_pos(pos))
            else:
                word = w.lower()
            if word not in stopwords:
                all_words.append(word)
    frequent_words = nltk.FreqDist(all_words)
    word_features = [w for w, f in frequent_words.most_common(num_of_words)]
    featuresets = [(document_features(tokens, word_features), s) for tokens, s in zip(data["text"], data["sentiment"])]

    train_set, test_set = featuresets[50:], featuresets[:50]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    n = 100
    most_informative = show_most_informative_features_in_list(classifier, n)
    classifier.show_most_informative_features(100)
    negative = positive = {}
    with open(os.path.join(os.path.dirname(__file__),'manual_sentiment_dictionaries/neg_list')) as f_n:
        for line in f_n:
            negative[line.rstrip()] = -1
    with open(os.path.join(os.path.dirname(__file__),'manual_sentiment_dictionaries/pos_list')) as f_p:
        for line in f_p:
            positive[line.rstrip()] = 1
    data = {**most_informative, **positive, **negative}
    output_file= os.path.normpath(
        os.path.join(os.path.dirname(__file__), '../sentimentAnalysis/lexicons/sentiment_lexicon_eswc.csv'))
    with open(output_file, 'w') as lexicon_file:
        csv_out = csv.writer(lexicon_file)
        csv_out.writerow(['word', 'sentiment'])
        for w in sorted(data):
            csv_out.writerow([w, data[w]])
    print('Classifier accuracy is: {}'.format(nltk.classify.accuracy(classifier, test_set)))
    print('You will find the outputted sentiment lexicon here: {}'.format(output_file))

create_lexicon(450)