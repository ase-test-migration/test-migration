import pandas as pd
import numpy as np
import scipy
import math
import os
import matplotlib.pyplot as plt
#import seaborn as sns
#import requests
import nltk
import gensim
from gensim.models import Word2Vec
from gensim.scripts.glove2word2vec import glove2word2vec
import csv
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import math
import functools as ft


class Sentence:
    def __init__(self, sentence):
        self.raw = sentence
        normalized_sentence = sentence.replace("’", "'")
        self.tokens = [t.lower() for t in nltk.word_tokenize(normalized_sentence)]
        STOP = set(nltk.corpus.stopwords.words("english"))
        self.tokens_without_stop = [t for t in self.tokens if t not in STOP or t == "more"]
        COMMON = {"selected", "tab", "not selected", "bar", "button", "menubar", "icon", "view", "ub", "container", "row", "scroll", "horizontal", "imageview", "icn", "btn"}
        self.tokens_without_stop_common = [t for t in self.tokens_without_stop if t not in COMMON]
        if "more" in self.tokens:
            self.tokens_without_stop.append("more")


class SimilarityCalculator:
    def __init__(self):
        nltk.download('stopwords')
        nltk.download('punkt')
        PATH_TO_WORD2VEC = os.path.expanduser("data/GoogleNews-vectors-negative300.bin")
        print("beforeee")
        self.word2vec = gensim.models.KeyedVectors.load_word2vec_format(PATH_TO_WORD2VEC, binary=True)
        print("afterrr")
        PATH_TO_FREQUENCIES_FILE = "data/frequencies.tsv"
        PATH_TO_DOC_FREQUENCIES_FILE = "data/doc_frequencies.tsv"

        self.frequencies = self.read_tsv(PATH_TO_FREQUENCIES_FILE)
        self.doc_frequencies = self.read_tsv(PATH_TO_DOC_FREQUENCIES_FILE)
        self.doc_frequencies["NUM_DOCS"] = 1288431

        self.benchmarks = [
              ("AVG-W2V-TFIDF-STOP", ft.partial(self.run_avg_benchmark, model=self.word2vec, use_stoplist=True, doc_freqs=self.doc_frequencies))
              ]


    def read_tsv(self, f):
        frequencies = {}
        with open(f) as tsv:
            tsv_reader = csv.reader(tsv, delimiter="\t")
            for row in tsv_reader:
                frequencies[row[0]] = int(row[1])
        return frequencies


    def run_avg_benchmark(self, sent1, sent2, model=None, use_stoplist=False, doc_freqs=None):
        if doc_freqs is not None:
            N = doc_freqs["NUM_DOCS"]

        sims = []

        tokens1 = sent1.tokens_without_stop_common if use_stoplist else sent1.tokens
        tokens2 = sent2.tokens_without_stop_common if use_stoplist else sent2.tokens

        tokens1 = [token for token in tokens1 if token in model]
        tokens2 = [token for token in tokens2 if token in model]

        print(tokens1)
        print(tokens2)

        if len(tokens1) == 0 or len(tokens2) == 0:
            sims.append(0)

        else:
            tokfreqs1 = Counter(tokens1)
            tokfreqs2 = Counter(tokens2)

            weights1 = [tokfreqs1[token] * math.log(N / (doc_freqs.get(token, 0) + 1))
                        for token in tokfreqs1] if doc_freqs else None
            weights2 = [tokfreqs2[token] * math.log(N / (doc_freqs.get(token, 0) + 1))
                        for token in tokfreqs2] if doc_freqs else None

            embedding1 = np.average([model[token] for token in tokfreqs1], axis=0, weights=weights1).reshape(1, -1)
            embedding2 = np.average([model[token] for token in tokfreqs2], axis=0, weights=weights2).reshape(1, -1)

            sim = cosine_similarity(embedding1, embedding2)[0][0]
            sims.append(sim)

        return sims


    def calc_similarity(self, sentence1, sentence2):
        for label, method in self.benchmarks:
            sims = method(Sentence(sentence1), Sentence(sentence2))
            print(sims)
            return sims[0]


    def run_experiment(df, benchmarks):
        sentences1 = [Sentence(s) for s in df['sent_1']]
        sentences2 = [Sentence(s) for s in df['sent_2']]

        pearson_cors, spearman_cors = [], []
        for label, method in benchmarks:
            sims = method(sentences1, sentences2)
            print(label)
            i = 0
            for sim in sims:
                i += 1
                print(i)
                print(sim)

        return pearson_cors, spearman_cors




# pearson_results, spearman_results = {}, {}
# pearson_results["SICK-DEV"], spearman_results["SICK-DEV"] = run_experiment(sick_dev, benchmarks)
