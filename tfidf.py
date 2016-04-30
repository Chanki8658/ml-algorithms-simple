#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
import os
from bs4 import *
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

PATH = 'shakes_dir'
token_dict = {}
stemmer = PorterStemmer()


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems


def to_words(raw_review):
    review_text = BeautifulSoup(raw_review, 'html.parser').get_text()
    letters_only = re.sub('[^a-zA-Z]', ' ', review_text)
    words = letters_only.lower().split()
    stops = set(stopwords.words('english'))
    meaningful_words = [w for w in words if not w in stops]
    return ' '.join(meaningful_words)


def main():
    for subdir, dirs, files in os.walk(PATH):
        for file in files:
            file_path = subdir + os.path.sep + file
            shakes = open(file_path, 'r')
            text = shakes.read()
            token_dict[file] = to_words(text)

    tfidf = TfidfVectorizer(tokenizer=tokenize)
    tfs = tfidf.fit_transform(token_dict.values())

if __name__ == '__main__':
    main()
