import json
from aspectExtraction import config
import os


class SetEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)
        return json.JSONEncoder.default(self, o)


def save_taxonomy():
    """Saves the aspect taxonomy to a file"""
    with open('aspect_taxonomy.json', 'w') as f:
        json.dump(config.ASPECT_TAXONOMY, f, cls=SetEncoder)


def load_taxonomy():
    """loads the taxonomy saved in a json file into a string"""
    dirpath = os.path.dirname(__file__)

    f = open(os.path.join(dirpath, 'aspect_taxonomy.json'), "r")
    return json.load(f)
