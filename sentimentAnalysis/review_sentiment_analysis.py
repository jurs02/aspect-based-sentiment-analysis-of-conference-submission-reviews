import os
from .classes import Review
from .opinion_orientation import opinion_orientation
import sys
"""
    This script serves as the main script of the aspect-based sentiment analysis algorithm.
    The conference from which the reviews will be sourced for the analysis can be specified by providing the appropriate argument
    when running the script.
    The default conferenc for the analysis are the ESWC 2019 reviews, as they are the only ones that can be made
    publically available.
"""
try:
    data_type = sys.argv[1]
except IndexError:
    data_type = "test_data/eswc19"

if data_type == "eswc19":
    path = "test_data/eswc19/"
elif data_type == "ekaw18":
    path = "test_data/ekaw18/"
elif data_type == "iswc18":
    path = "test_data/iswc18/"
else:
    path = "test_data/eswc19"
path = os.path.join(os.path.dirname(__file__), path)
reviews = []
for file in os.listdir(path):
    if os.path.isfile(os.path.join(path, file)) and not file.startswith("."):
        f = open(os.path.join(path, file), 'r', encoding="ISO-8859-1")
        content = f.read()
        r = Review(file, content)
        reviews.append(r)
        opinion_orientation(r)
        r.print_results()
