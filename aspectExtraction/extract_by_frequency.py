import nltk
from nltk import pos_tag, word_tokenize, RegexpParser
from mlxtend.preprocessing import TransactionEncoder
import re
import pandas as pd
import os
from aspectExtraction import config


def nnp_extract(text):
    """gets the text from a review and returns all nouns or noun phrases in a list"""
    output = []
    lemmatizer = nltk.WordNetLemmatizer()
    tagged = pos_tag(word_tokenize(text))
    chunker = RegexpParser("""
        NBAR:
            {<NN.*|JJ>*<NN.*>} 

        NP:
            {<NBAR>}
            {<NBAR><IN><NBAR>}
        """)
    tree = chunker.parse(tagged)
    for st in tree.subtrees():
        if st.label() == "NP":
            if len(st.leaves()) > 3:
                continue
            nnp = ""
            for w, t in st.leaves():
                lemma = lemmatizer.lemmatize(re.sub('[^A-Za-z0-9-]+', '', w.lower()),
                                             config.get_wordnet_pos(t))
                if 2 < len(
                        lemma) < 20:
                    if nnp == "":
                        nnp = lemma
                    else:
                        nnp = " ".join([nnp, lemma])

            if nnp != "":
                output.append(nnp)
    return output


def jj_extract(text):
    """ extracts all adjectives from the text and returns them in a list"""
    tagged = pos_tag(word_tokenize(text))
    return [token for token, tag in tagged if tag == "JJ"]


def get_frequent_in_list(dataset, minsup):
    """ accepts a list of lists where each list contains the extracted aspects candidates from a single review
        returns a list of those aspect candidates, which have the minimal support minsup accross all reviews
    """
    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    return df.columns[df.sum() > (minsup * df.shape[0])].tolist()


def frequent_candidates():
    """Returns a tuple of a list most frequent nouns and noun phrases and  a list most frequent adjectives across
    reviews which serve as aspect word candidates """
    dataset_nnps = []
    dataset_jjs = []
    for dirpath, dirnames, filenames in os.walk(os.path.join(os.path.dirname(__file__), "data"
                                                                                        "/data_for_frequency_extraction")):
        for filename in filenames:
            if os.path.isfile(os.path.join(dirpath, filename)) and not filename.startswith("."):
                f = open(os.path.join(dirpath, filename), 'r', encoding="ISO-8859-1")
                content = f.read()
                dataset_nnps.append(nnp_extract(content))
                dataset_jjs.append(jj_extract(content))
    frequent_nnps = get_frequent_in_list(dataset_nnps, config.MINSUP)
    frequent_jjs = get_frequent_in_list(dataset_jjs, config.MINSUP)
    return frequent_nnps, frequent_jjs
