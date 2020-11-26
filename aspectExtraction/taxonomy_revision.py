from aspectExtraction import config


def choose_other_aspect(candidate_term):
    print('Does it belong under any of these aspects ?:')
    switcher = {}
    i = "a"
    for top_aspect in config.ASPECT_TAXONOMY:
        switcher[i] = top_aspect
        print('{:<25s}[{}]'.format(top_aspect, i))
        i = chr(ord(i) + 1)
    print('\n{:<25s}[n]'.format("none of the above"))
    i = input()
    if i == 'n':
        return
    i = switcher.get(i, "o")
    if i == 'o':
        return choose_other_aspect(candidate_term)
    config.ASPECT_TAXONOMY[i].add(candidate_term)
    return


def candidate_revision(candidate_term, candidate_aspect):
    """Adds the candidate term in the aspect taxonomy under candidate aspect if user agrees, otherwise user will be
    asked if they want to choose a aspect by calling choose_other_aspect """
    print('Does the term "', candidate_term, '" belong under aspect "', candidate_aspect, '" ? [y/n]')
    i = input()
    if i == "y":
        config.ASPECT_TAXONOMY[candidate_aspect].add(candidate_term)
    elif i == "n":
        choose_other_aspect(candidate_term)
    else:
        candidate_revision(candidate_term, candidate_aspect)
    return


def check_if_already_in_taxonomy(candidate):
    for aspects in config.ASPECT_TAXONOMY.values():
        if candidate in aspects:
            return True
    return False


def taxonomy_revision():
    """Allows the user to manually confirm/adjust the addition of extracted aspect word candidates to the taxonomy"""
    for aspect, candidates in config.ASPECT_TAXONOMY_CANDIDATES.items():
        for candidate in candidates:
            if check_if_already_in_taxonomy(candidate):
                continue
            candidate_revision(candidate, aspect)
