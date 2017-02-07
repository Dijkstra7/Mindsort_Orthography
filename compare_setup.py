# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 11:31:39 2017

@author: rick
"""
# Trying to make this according to commenting standards

# The imports.
from random import random

from combined_model import CombinedModel


def words_to_be_compared():
    """ Een lijst van de woorden of woordvormen die moeten worden vergeleken.

    TODO:
    - kiezen om een lijst hier te hardcoden of om het uit een file te halen.
    """
    some_words = ''
    return some_words


def get_similarity_words(base_word, compare_word, method_='Open Bigrams'):
    """ Giving a similarity of two words.

    Vergelijk de twee woorden in de Class die de vergelijking uitvoert.

    TODO:
    - choose what models to use and implement as class
    - implement all the classes basic operations
    """
    similarity_score = 0
    if method_ == 'Open Bigrams':
        similarity_score = BigramModel(base_word, compare_word).sim_score
    if method_ == 'Spatial Coding':
        similarity_score = SpatialModel(base_word, compare_word).sim_score
    if method_ == 'Combined Method':
        similarity_score = CombinedModel(base_word, compare_word).sim_score
    if method_ == 'Holo Open Bigrams':
        similarity_score = HoloModel(base_word, compare_word).sim_score
    return similarity_score


def compare_words(method=None):
    # Take two random words from the list of words and get a similarityscore.
    words = words_to_be_compared()
    base_word = words[random.randint(0, len(words))]
    compare_word = words[random.randint(0, len(words))]
    return get_similarity_words(base_word, compare_word, method)


print compare_words()
