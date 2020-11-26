from aspectExtraction.similarity import calculate_similarity
from aspectExtraction import config



def taxonomy_matching(frequent_tokens,pos):
    """Calculates the similarity between frequent terms in text (nouns, noun phrases or adjectives) to terms in the
    manually created taxonomy
    Fills the confing.ASPECT_TAXONOMY_CANDIDATES dictionary with terms similar enough """
    for f_t in frequent_tokens:
        best_match_aspect = ""
        best_match_sim = 0
        for top_aspect in config.ASPECT_TAXONOMY:
            for aspect in config.ASPECT_TAXONOMY[top_aspect]:
                sim = calculate_similarity(f_t, aspect,pos)
                if sim > best_match_sim:
                    best_match_aspect = top_aspect
                    best_match_sim = sim
        if best_match_sim > 0.3:
            config.ASPECT_TAXONOMY_CANDIDATES[best_match_aspect].add(f_t)
