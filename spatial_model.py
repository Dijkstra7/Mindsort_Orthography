# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 14:29:49 2017

@author: rick
"""

# Imports
import math


def closest_to_0(current, contender):
    if abs(current)-abs(contender) > 0:
        return contender
    return current


def closer_to_0(current, contender):
    if contender is None:
        return False
    if abs(current)-abs(contender) > 0:
        return True
    return False


class SpatialModel:
    """ The model that implements Spatial Coding.

    In the spatial coding paper the author says that only the first 16
    equations are enough to represent the spatial coding model for comparing
    two words with each other. So this will be the extent of this model for
    now.
    TODO: implement SC
    """

    similarity_score = 0
    sigma_0 = 0.48  # As stated in table 3 in spatial coding.
    k_0 = 0.24      # As stated in table 3 in spatial coding.
    sigma = 0
    bank_of_receivers = []   # Not sure if needed
    base_word = 'spam'
    compare_word = 'eggs'

    def __init__(self, base_word, compare_word):
        self.sigma = self.calculate_sigma(len(compare_word))
        # self.similarity_score = \
        #    self.calculate_similarity(base_word, compare_word)
        self.initialise_receivers(base_word, compare_word)
        self.base_word = base_word
        self.compare_word = compare_word

    def initialise_receivers(self, template, input_):
        """
        initialise the receivers from the template, and activate them by
        finding the winning receivers
        """
        for position, identity in enumerate(template):
            self.bank_of_receivers.append(Receiver(identity, len(input_),
                                                   position))
        for position, identity in enumerate(input_):
            for bank_pos, bank in enumerate(self.bank_of_receivers):
                bank.update_clones(identity, position, bank_pos)
        for bank in self.bank_of_receivers:
            if bank.winning_clone is not None:
                bank.cross_bank_winner(self.bank_of_receivers)
        for bank in self.bank_of_receivers:
            bank.printself()

    def spatial(self, letter_pos, goal_pos):
        """ equation 1 in spatial coding

        letter_pos indexes the letters within the spatial code and goal_pos
        is the (veridical) serial position of the letter within the input
        stimulus.
        """
        power = (letter_pos-goal_pos)/self.sigma
        return math.exp(-1*power**2)

    def calculate_sigma(self, length):
        """ equation 3 in spatial coding

        the assumption that longer words wil have bigger sigma's is
        implemented here.
        """
        self.sigma = self.sigma_0+self.k_0*length

    def activation(self, letter, time):
        """ calculate the activation level of a letter at a time.

        For now the paper doesn't seem to do anything with this other than
        setting it to 1
        """
        return 1

    def signal(self, letter_pos, goal_pos, time, letter):
        """ equation 4 in spatial coding

        TODO: figure out if activation should be impplemented differently
        """
        activation_letter = self.activation(letter, time)
        return activation_letter*self.spatial(letter_pos, goal_pos)

    def delay(goal_pos, letter_pos):
        """ the delay implemented by the SC model

        The value of delayri corresponds to the expected ordinal position of
        the corresponding letter within the template.
        """
        return goal_pos-letter_pos

    def receiver(self, bank, channel, identity, letter, position, time):
        """ equation 9 in spatial coding.

        This equation calculates the activation of a receiver in a bank on a
        channel.
        The bank is the expected letter position.

        Not sure if identity or channel has to be implemented. in the SC paper
        it stands for the identity of the i'th word.
        """
        return self.signal(bank, position, time, letter)-self.delay(bank,
                                                                    position)

    def winning_receiver(self, receivers, position, time):
        """ calculate the score of the winning receiver

        The winning receiver is that receiver that is closest to 0.
        """
        winning_score = 99
        for (rec_letter, rec_pos) in receivers:
            rec_score = self.receiver(rec_pos, None, None, rec_letter,
                                      position, time)
            winning_score = closest_to_0(winning_score, rec_score)
        return winning_score

    def super_position(self, banks_of_receivers, identity, position, time):
        """ equation 10 in spatial coding.

        'The superposition function is found by summing across the receiver
        functions for each of the template’s receivers'

        """
        super_position_score = 0
        for bank in banks_of_receivers:
            winning_receiver_score = self.winning_receiver(bank, position,
                                                           time)
            super_position_score = super_position_score + \
                winning_receiver_score
        return super_position_score

    def match(self, banks_of_receivers, base_length, compare_length, time):
        """ equation 7 in spatial coding

        matching the base_word with the compare_word.
        """
        match = 0
        res_phase = self.find_resonating_phase(abs(base_length - 
                                                   compare_length))

    def find_resonating_phase(max_dist):
        best_pos = (0,0)       
        for pos in range(-1*max_dist, max_dist):
            'Do things'

    def calculate_similarity(self, time):
        return 1  # receiver_output(time)+ext_letter_match(time)

    def ext_letter_match(time):
        for i in pie:
            'eat sky'


class Receiver:
    """
    the structure of a receiver
    """
    identity = 'a'
    clones = []
    position = -1
    winning_clone = None

    def __init__(self, identity, n_clones, position):
        self.identity = identity
        clones = []
        for clone in range(n_clones):
            clones.append(None)
        self.clones = clones
        self.position = position

    def update_clones(self, identity_input, pos_input, pos_self):
        if self.identity == identity_input:
            self.clones[pos_input] = pos_input-pos_self
        self.select_winner()

    def select_winner(self):
        winning_clone = 99
        for id_clone, clone in enumerate(self.clones):
            if closer_to_0(winning_clone, clone):
                self.winning_clone = id_clone
                winning_clone = clone

    def cross_bank_winner(self, bank):
        for other_clones in bank:
            if self.identity == other_clones.identity:
                if closer_to_0(self.clones[self.winning_clone],
                               other_clones.clones[self.winning_clone]):
                    self.winning_clone = None
                    break

    def printself(self):
        print self.identity
        for id_, clone in enumerate(self.clones):
            suffix = ''
            if id_ == self.winning_clone:
                suffix = ' <= winner'
            print str(id_+1)+" "+str(clone)+suffix
