from aspectExtraction.taxonomy_matching import taxonomy_matching
from aspectExtraction.taxonomy_revision import taxonomy_revision
from aspectExtraction.extract_by_structure import get_aspect_by_structure
from aspectExtraction.serialize_taxonomy import save_taxonomy
from aspectExtraction.extract_by_frequency import frequent_candidates
from nltk.corpus import wordnet as wn



def get_aspects():
    """Finds aspect word candidates by frequency and using a known structure of a review"""
    frequent_nnps, frequent_adjs = frequent_candidates()
    taxonomy_matching(frequent_nnps, wn.NOUN)
    taxonomy_matching(frequent_nnps, wn.ADJ)
    get_aspect_by_structure()
    taxonomy_revision()


get_aspects()
save_taxonomy()
