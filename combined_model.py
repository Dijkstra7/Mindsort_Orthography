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
    quadgram_field = []
    letter_field_letters = []
    bigram_field_bigrams = []
    quadgram_field_quadgrams = []

    def __init__(self, base_word, compare_word):
        self.template = base_word
        self.compare = compare_word
        self.sigma = 0.48+0.24*len(compare_word)
        self.init_base_field(self.sigma)
        self.sigma = (0.48+0.24*len(compare_word))/4
        self.init_bigram_field(self.sigma)
        self.init_quadgram_field()
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

    def init_quadgram_field(self, sigma=1.25):
        self.quadgram_field = []
        quadgrams = []
        max_len = len(self.template)
        for pos in range(max_len - 3):
            bigrams = [self.find_bigram_for_quadgram(p+pos) for p in range(3)]
            new_quad = QuadrigramNeuron(bigrams, max_len)
            if new_quad.identity in quadgrams:
                continue
            self.quadgram_field.append(new_quad)
            quadgrams.append(new_quad.identity)
        self.quadgram_field_quadgrams = quadgrams
        # print quadgrams

    def find_bigram_for_quadgram(self, position):
        f_letter = self.template[position]
        s_letter = self.template[position + 1]
        bigram = f_letter + s_letter
        return self.find_bigram_neuron(bigram)

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
        similarity = self.calc_quadgram_activation(self.compare)

        # Calculate the maximum similarity.
        self.reset_fields()
        max_similarity = self.calc_quadgram_activation(self.template)

        # Return the normalized similarity.
        if max_similarity == 0:
            return -0.0
        return (1.0 * similarity) / (1.0 * max_similarity)

    def reset_fields(self):
        for neuron in self.letter_field:
            neuron.reset()
        for neuron in self.bigram_field:
            neuron.reset()

    def calc_bigram_activation(self, input_):
        """
        Calculate the activation of the neurons that are linked to the
        template.
        """
        activation = 0.0

        # activate neurons
        for position, letter in enumerate(input_):
            if letter in self.letter_field_letters:
                letter_neuron = self.find_letter_neuron(letter)
                letter_neuron.activate(position)

        for n in range(1, len(self.template)-1):
            activation = activation + self.calc_n_removed_bigram_activation(n)
        return activation

    def calc_n_removed_bigram_activation(self, n):
        # calculate bigrams
        activation = 0.0
        for position, f_letter in enumerate(self.template[:-1*n]):
            s_letter = self.template[position + n]
            bigram = f_letter+s_letter
            bigram_neuron = self.find_bigram_neuron(bigram)
            if bigram_neuron is not None:
                activation = activation + bigram_neuron.activation(position)
        return activation / (len(self.template) - n)  # activation / #bigrams

    def find_bigram_neuron(self, bigram):
        if bigram in self.bigram_field_bigrams:
            index = self.bigram_field_bigrams.index(bigram)
            return self.bigram_field[index]
        return None

    def calc_quadgram_activation(self, input_):
        activation = 0.0

        # activate neurons
        for position, letter in enumerate(input_):
            if letter in self.letter_field_letters:
                letter_neuron = self.find_letter_neuron(letter)
                letter_neuron.activate(position)

        activation = sum([node.activation() for node in self.quadgram_field])
        return activation


class LetterNeuron:
    """
    The class for a letter Neuron. It has the positions where it is linked to
    an bigram node stored.
    """

    identity = ""
    position = None
    sigma = None
    endletter = False
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


class QuadrigramNeuron:

    nodes = []
    identity = ""
    sigma = None
    templatelen = None

    def __init__(self, nodes, templatelen, sigma=1.25):
        self.identity = self.get_id(nodes)
        self.nodes = nodes
        self.sigma = sigma
        self.templatelen = templatelen

    def get_id(self, nodes):
        _id = "".join([n.identity[0] for n in nodes])
        _id = _id + nodes[-1].identity[1]
        return _id

    def activation(self):
        activation = 0.0
        for position in range(self.templatelen-3):
            for shift in range(len(self.nodes)):
                activation += self.nodes[shift].activation(position+shift)
        return activation


def test():
    template = ["testen", "12345", "1245", "123345", "123d45", "12dd5",
                "1d345",
                "12d456", "12d4d6", "d2345", "12d45", "1234d", "12435",
                "21436587", "125436", "13d45", "12345", "34567", "13457",
                "123267", "123567", "12dd56", "1d3d56", "ideeen", "ideeen"]
    compare = ["getest", "12345", "12345", "12345", "12345", "12345",
               "12345",
               "123456", "123456", "12345", "12345", "12345", "12345",
               "12345678", "123456", "12345", "1234567", "1234567", "1234567",
               "1232567", "1232567", "123456", "123456", "ideeeen",
               "ideeekn"]
    template_new_study = ["123456", "12345", "123456d", "123465", "124356",
                          "12456", "12345d", "d23456", "213456", "123d456",
                          "d123456", "123", "123dd456", "1256", "12d456",
                          "13d456", "143256", "123de456", "214365", "12de56",
                          "321654", "153426", "415263", "456123", "design",
                          "165432", "1bcde6", "abcdef"]
    template.extend(template_new_study)
    for i in range(28):
        compare.append("123456")
    for i in range(23, 25):
        cm = CombinedModel(compare[i], template[i])
        # sm.print_banks()
        print str(i+1), ' t: ', template[i], 'c: ', compare[i], \
            'match equals:', str(cm.match())


def test2():
    LN1 = LetterNeuron("a")
    LN1.activate(1)
    LN1.activate(1)
    LN2 = LetterNeuron("b")
    LN2.activate(0)
    LN2.activate(0)
    LN3 = LetterNeuron("c")
    LN3.activate(3)
    LN3.activate(3)
    LN4 = LetterNeuron("d")
    LN4.activate(2)
    LN4.activate(2)
    BN1 = BigramNeuron(LN1, LN2)
    BN2 = BigramNeuron(LN2, LN3)
    BN3 = BigramNeuron(LN3, LN4)
    QN = QuadrigramNeuron([BN1, BN2, BN3], 4)
    print QN.identity, QN.activation()

test()
