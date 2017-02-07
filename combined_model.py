# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 14:00:47 2017

@author: rick

The module in which the new combined model of spatial coding and open bigrams
will be implemented.
"""

# Imports.


class CombinedModel:
    """ The model that will implement my own theory of word-comparing.

    TODO:
    - find a good representation for the gaussian curves and how to add them.
    """
    sim_score = 0

    def __init__(self, base_word, compare_word):
        self.similarity_score = \
            self.calculate_similarity(base_word, compare_word)

    def add_curves(curve1, curve2):
        # Add the gaussian curves together into a new curve.
        # TODO: Make better addding method.
        added_curve = []
        for (score1, score2) in zip(curve1, curve2):
            added_curve.append(score1+score2)
        return added_curve

    def make_curve(letter):
        # TODO: make a representation of a curve.
        return 1

    def calculate_gaussian_curves(self, word):
        """
        calculate the curve of a single letter

        TODO:
        - figure out the best representation of curves, preferrably a function.
        """
        letters = []
        curves = []
        for letter in word:
            letters.append(letter)
            curves.append(self.make_curve(letter))
        return letters, curves

    def calculate_bigram_scores(self, letters, gausscurves):
        """
        calculating the bigrams of a word and (optionally) their scores

        TODO: implement the method further
        """
        bigrams = []
        scores = []
        for (first_letter, first_curve) in zip(letters, gausscurves):
            for (second_letter, second_curve) in zip(letters, gausscurves):
                bigram = first_letter+second_letter
                bigrams.append(bigram)

                score = self.add_curves('first_curve', 'second_curve')
                scores.append(score)

        return (bigrams, scores)

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
        base_letters, base_gausscurves = \
            self.calculate_gaussian_curves(base_word)
        base_bigrams_scores = self.calculate_bigram_scores(base_letters,
                                                           base_gausscurves)

        compare_letters, compare_gausscurves = \
            self.calculate_gaussian_curves(compare_word)
        compare_bigrams_scores = \
            self.calculate_bigram_scores(compare_letters, compare_gausscurves)

        similarity = self.calculate_bigram_similarity(base_bigrams_scores,
                                                      compare_bigrams_scores)
        return similarity
