# aspect-based-sentiment-analysis-of-conference-submission-reviews
### This repository contains the code for an aspect-based sentiment analysis of conference submission reviews, which was created as part of my master thesis.

The implementation of the algorithm, written in Python 3.8 is divided into three main parts:
- `aspectExtraction/` contains the code for the generation of an aspect expression taxonomy
- `sentimentLexicon/` contains the code for the generation of a sentiment lexicon
- `sentimentAnalysis/` contains the code for the aspect-based sentiment analysis algorithm

## Aspect extraction
The main script is the `aspectExtraction/aspect_extraction.py`. You can run it from the main directory with the following command:

`python -m aspectExtraction.aspect_extraction`

Unfortunately the data that was used for the aspect extraction cannot be made publicly available, but
if you have your own review data, you can put them inside the `aspectExtraction/data/data_for_frequency_extraction`
directory and run the code just the same.

## Sentiment lexicon
The main script for the generation of a sentiment lexicon is `sentimentLexicon/sentiment_lexicon.py` and can be run
using the command:

`python -m sentimentLexicon.sentiment_lexicon`

## Sentiment analysis
The main script to perform the sentiment analysis over conference submission reviews is the `sentimentAnalysis/review_sentiment analysis`
and can be run using the command:

`python -m sentimentAnalysis.review_sentiment_analysis`

As only the ESWC 2019 data can be made publicly available, it is set to analyze only the data in the `sentimentAnalysis/test_data/eswc19/`
directory.

The `sentimentAnalysis/sentimentr.py` script is a custom implementation of the [sentimentr algorithm](https://github.com/trinker/sentimentr).