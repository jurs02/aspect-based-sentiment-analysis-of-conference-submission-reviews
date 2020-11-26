import os
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
from aspectExtraction import config
from aspectExtraction.extract_by_frequency import get_frequent_in_list

aspect_headers = [("Relevance to ESWC", "relevance"),
                  ("Novelty of the Proposed Solution", "novelty"),
                  ("Correctness and Completeness of the Proposed Solution", "technical quality"),
                  ("Evaluation of the State-of-the-Art", "state of the art"),
                  ("Demonstration and Discussion of the Properties of the Proposed Approach", "technical quality"),
                  ("Reproducibility and Generality of the Experimental Study", "evaluation"),
                  ("Overall score", "")
                  ]
aspect_tokenized_sentences = {
    'relevance': [],
    'novelty': [],
    'technical quality': [],
    'state of the art': [],
    'evaluation': [],
    'presentation': [],
}


def extract_tokens_by_review_and_aspect(text):
    """Fills the aspect_tokenized_sentences dictionary with a
    list of lists where each list are tokens of a sentence in a text belonging to the aspect represented by the
    dictionary key  (using the known structure of a set of reviews from one conference)

    """
    lemmatizer = WordNetLemmatizer()
    for i in range(len(aspect_headers) - 1):
        current_header = text.find("----------- " + aspect_headers[i][0] + " -----------")
        next_header = text.find("----------- " + aspect_headers[i + 1][0] + " -----------")
        if current_header == -1 or next_header == -1:
            return
        current_header += len("----------- " + aspect_headers[i][0] + " ----------- ")
        stop_words = set(stopwords.words('english'))
        filtered_sentence = [lemmatizer.lemmatize(w.lower()) for w in word_tokenize(text[current_header:next_header]) if
                             not w.lower() in stop_words and w.isalpha()]

        aspect_tokenized_sentences[aspect_headers[i][1]].append(filtered_sentence)




def get_aspect_by_structure():
    """Uses the structure of reviews of the ESWC conference to extract aspect word candidates"""
    path = os.path.join(os.path.dirname(__file__), "data/data_for_structure_extraction")
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)) and not file.startswith("."):
            f = open(os.path.join(path, file), 'r', encoding="ISO-8859-1")
            content = f.read()
            extract_tokens_by_review_and_aspect(content)
    for aspect, text in aspect_tokenized_sentences.items():
        for candidate in get_frequent_in_list(text, 0.4):
            config.ASPECT_TAXONOMY_CANDIDATES[aspect].add(candidate)
