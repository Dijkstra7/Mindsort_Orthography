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
    sigma = None
    template = ""
    compare = ""
    letter_layer_inhibition = False
    bigram_layer_inhibition = False
    quadrigram_layer_inhibiton = None
    letter_field = []
    bigram_field = []
    letter_field_letters = []
    bigram_field_bigrams = []

    def __init__(self, base_word, compare_word):
        self.template = base_word
        self.compare = compare_word
        self.sigma = 0.48+0.24*len(compare_word)
        self.init_base_field(self.sigma)
        self.sigma = 0.48+0.24*len(compare_word)
        self.init_bigram_field(max(len(base_word), len(compare_word)))
        self.similarity_score = \
            self.calculate_similarity(base_word, compare_word)

    def init_base_field(self, sigma=1.25):
        self.letter_field = []
        letters = []
        for position, letter in enumerate(self.template):
            if letter in letters:
                continue
            new_neuron = LetterNeuron(letter, sigma)
            self.letter_field.append(new_neuron)
            letters.append(letter)
        self.letter_field_letters = letters

    def init_bigram_field(self, sigma=1.25):
        """For now just closed bigrams"""
        self.bigram_field = []
        bigrams = []
        for position in range(len(self.template) - 1):
            first_letter = self.template[position]
            second_letter = self.template[position + 1]
            bigram = first_letter + second_letter
            if bigram in bigrams:  # Test if bigram already exists.
                continue

            # create neuron
            first_neuron = self.find_letter_neuron(first_letter)
            second_neuron = self.find_letter_neuron(second_letter)
            new_bigram = BigramNeuron(first_neuron, second_neuron, self.sigma,
                                      1)

            # Add neuron to field
            self.bigram_field.append(new_bigram)
            bigrams.append(bigram)
        self.bigram_field_bigrams = bigrams

    def find_letter_neuron(self, letter):
        index = self.letter_field_letters.index(letter)
        return self.letter_field[index]

    def match(self):
        return self.similarity_score

    def calculate_similarity(self, base_word='spam', compare_word='eggs'):
        """
        calculate the similarity between the base word and the compare word and
        returns the similarity-value.
        """
        # Calculate the similarity between template and compare.
        similarity = self.calc_bigram_similarity(self.compare)

        # Calculate the maximum similarity.
        self.reset_fields()
        max_similarity = self.calc_bigram_similarity(self.template)

        # Return the normalized similarity.
        if max_similarity == 0:
            return -0.0
        return (1.0 * similarity) / (1.0 * max_similarity)

    def reset_fields(self):
        for neuron in self.letter_field:
            neuron.reset()
        for neuron in self.bigram_field:
            neuron.reset()

    def calc_bigram_similarity(self, input_):
        similarity = 0.0

        # activate neurons
        for position, letter in enumerate(input_):
            if letter in self.letter_field_letters:
                letter_neuron = self.find_letter_neuron(letter)
                letter_neuron.activate(position)

        # calculate bigrams
        for position, fletter in enumerate(self.template[:-1]):
            sletter = self.template[position + 1]
            bigram = fletter+sletter
            similarity = similarity + \
                self.find_bigram_neuron(bigram).activation(position)
        return similarity / (len(self.template) - 1)  # sim / #bigrams

    def find_bigram_neuron(self, bigram):
        index = self.bigram_field_bigrams.index(bigram)
        return self.bigram_field[index]


class LetterNeuron:
    """
    The class for a letter Neuron. It has the positions where it is linked to
    an bigram node stored.
    """

    identity = ""
    position = None
    sigma = None
    deactivation = []

    def __init__(self, id_, sigma=1.25):
        self.identity = id_
        self.position = []
        self.sigma = sigma

    def activate(self, position):
        self.position.append(position)

    def competition(self, other_neurons, position):
        for other_neuron in other_neurons:
            if other_neuron.activation(position) > self.activation(position):
                self.deactivation.append(position)

    def activation(self, distance):
        if distance in self.deactivation:
            return 0.0
        powers = [(position - distance) / self.sigma for position in
                  self.position]
        results = [math.exp(-1.0 * power ** 2) for power in powers]
        if results == []:
            return 0.0
        return max(results)

    def reset(self):
        self.position = []


class BigramNeuron:

    identity = ""
    position = None
    sigma = None
    first_link = None
    second_link = None
    weight = 0
    deactivation = []

    def __init__(self, first, second, sigma=1.25, weight=1):
        self.identity = first.identity + second.identity
        self.first_link = first
        self.second_link = second
        self.position = []
        self.sigma = sigma
        self.weight = weight

    def activate(self, position):
        self.position.append(position)

    def competition(self, other_neurons, position):
        for other_neuron in other_neurons:
            if other_neuron.activation(position) > self.activation(position):
                self.deactivation.append(position)

    def activation(self, distance):
        """
        A bigram neuron is activated by the two neurons he is linked to in
        the letter field.

        His activation depends on the distance from the activation in the
        first neuron on the same position and the second neuron on the
        position one right to it

        If the neuron is inhibited on this location he will return 0.
        """
        if distance in self.deactivation:
            return 0.0
        return (self.first_link.activation(distance) +
                self.second_link.activation(distance+1)) / 2

    def reset(self):
        self.position = []


def test():
    template = ["testen", "12345", "1245", "123345", "123d45", "12dd5",
                "1d345",
                "12d456", "12d4d6", "d2345", "12d45", "1234d", "12435",
                "21436587", "125436", "13d45", "12345", "34567", "13457",
                "123267", "123567"]
    compare = ["getest", "12345", "12345", "12345", "12345", "12345",
               "12345",
               "123456", "123456", "12345", "12345", "12345", "12345",
               "12345678", "123456", "12345", "1234567", "1234567", "1234567",
               "1232567", "1232567", ]
    for i in range(1, 21):
        cm = CombinedModel(template[i], compare[i])
        # sm.print_banks()
        print str(i+1), ' t: ', template[i], 'c: ', compare[i], \
            'match equals:', str(cm.match())


def test2():
    LN1 = LetterNeuron("a")
    LN1.activate(4)
    LN1.activate(2)
    LN2 = LetterNeuron("b")
    LN2.activate(4)
    LN2.activate(3)
    BN = BigramNeuron(2, LN1, LN2)
    for i in range(6):
        print BN.activation(i)

test()
