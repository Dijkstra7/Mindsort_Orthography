# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 14:00:47 2017

@author: rick

The module in which the new combined model of spatial coding and open bigrams
will be implemented.
"""

# Imports.
import math


class CombinedModel:
    """ The model that will implement my own theory of word-comparing.

    TODO:
    - find a good representation for the gaussian curves and how to add them.
    """
    similarity_score = 0
    template = ""
    compare = ""

    def __init__(self, base_word, compare_word):
        self.template = base_word
        self.compare = compare_word
        self.sigma = 0.48+0.24*len(base_word)
        self.similarity_score = \
            self.calculate_similarity(base_word, compare_word)

    def match(self):
        return self.similarity_score

    def make_bigram_curves(self, base_curves, positions):
        """
        calculating the bigrams of a word and their scores
        """
        bigram_curves = []
        for first in base_curves:
            for second in base_curves:
                bigram_curves.append(BigramCurve(first, second, positions))
        return bigram_curves

    def calculate_similarity(self, base_word='spam', compare_word='eggs'):
        """
        calculate the similarity between the base word and the compare word and
        returns the similarity-value.

        TODO:
        - decide between similarity between 0 and 1 or something else.
        - Implement all pseudocode:
            - from word to letters.
            - from letters to gaussian curves.
            - from lettercurves to bigram curves or bigram scores.
        """
        # calculate the templateword scores.
        template_base_curves = []
        for position, identity in enumerate(self.template):
            template_base_curves.append(BaseCurve(identity, position,
                                                  self.sigma))
        template_bigrams_scores = \
            self.make_bigram_curves(template_base_curves, len(self.template))

        # calculate the compareword scores.
        compare_base_curves = []
        for position, identity in enumerate(self.compare):
            compare_base_curves.append(BaseCurve(identity, position,
                                                 self.sigma))
        compare_bigrams_scores = self.make_bigram_curves(compare_base_curves,
                                                         len(self.compare))

        # Calculate the similarity between template and compare.
        similarity = self.calc_bigram_similarity(template_bigrams_scores,
                                                 compare_bigrams_scores)

        # Calculate the maximum similarity.
        max_similarity = self.calc_bigram_similarity(template_bigrams_scores,
                                                     template_bigrams_scores)

        # Return the normalized similarity.
        return (1.0 * similarity) / (1.0 * max_similarity)

    def calc_bigram_similarity(self, scores_1, scores_2):
        similarity = 0.0
        for score_1 in scores_1:
            for score_2 in scores_2:
                if score_1.identity == score_2.identity:
                    for pos in range(max(len(score_1.scores),
                                         len(score_2.scores))):
                        similarity = similarity + \
                            score_1.scores[pos] * score_2.scores[pos]
        return similarity


class BaseCurve:

    identity = ""
    position = -1
    sigma = 0

    def __init__(self, identity, position, sigma):
        self.sigma = sigma
        self.identity = identity
        self.position = position

    def score(self, distance):
        power = (self.position-distance)/self.sigma
        return math.exp(-1.0*power**2)


class BigramCurve:

    first = None
    second = None
    identity = ""
    scores = []

    def __init__(self, first, second, num_scores):
        self.first = first
        self.second = second
        self.calculate_scores(num_scores)
        self.identity = first.identity + second.identity

    def calculate_scores(self, num):
        for i in range(num-1):
            self.scores.append(self.first.score(i)+self.second.score(i+1))


def test():
    template = ["12345", "1245", "123345", "123d45", "12dd5", "1d345",
                "12d456", "12d4d6", "d2345", "12d45", "1234d", "12435",
                "21436587", "125436", "13d45", "12345", "34567", "13457",
                "123267", "123567"]
    compare = ["12345", "12345", "12345", "12345", "12345", "12345",
               "123456", "123456", "12345", "12345", "12345", "12345",
               "12345678", "123456", "12345", "1234567", "1234567", "1234567",
               "1232567", "1232567", ]
    for i in range(20):
        cm = CombinedModel(template[i], compare[i])
        # sm.print_banks()
        print str(i+1), ' t: ', template[i], 'c: ', compare[i], \
            'match equals:', str(cm.match())


test()
