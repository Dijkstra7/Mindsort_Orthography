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
        sigma = self.calculate_sigma(len(compare_word))
        self.sigma = sigma
        print sigma
        # self.similarity_score = \
        #    self.calculate_similarity(base_word, compare_word)
        self.initialise_receivers(base_word, compare_word, sigma)
        self.base_word = base_word
        self.compare_word = compare_word

    def initialise_receivers(self, template, input_, sigma):
        """
        initialise the receivers from the template, and activate them by
        finding the winning receivers based on competition within and between
        banks.
        """
        # Create the receivers.
        for position, identity in enumerate(template):
            self.bank_of_receivers.append(Receiver(identity, len(input_),
                                                   position, sigma))

        # Update the elimination within banks
        for position, identity in enumerate(input_):
            for bank_pos, bank in enumerate(self.bank_of_receivers):
                bank.update_clones(identity, position, bank_pos)

        # Update the elmimination between banks
        for bank in self.bank_of_receivers:
            if bank.winning_clone is not None:
                bank.cross_bank_winner(self.bank_of_receivers)

    def print_banks(self, start=None, stop=None, step=1):
        """
        For testing purposes.
        """
        if start is None:
            start = 0
            stop = len(self.bank_of_receivers)
        if stop is None:
            stop = start+1
        for bank in range(start, stop, step):
            self.bank_of_receivers[bank].printself()

    def calculate_sigma(self, length):
        """ equation 3 in spatial coding

        the assumption that longer words wil have bigger sigma's is
        implemented here.
        """
        return self.sigma_0+self.k_0*length

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

    def super_position(self, position, time):
        """ equation 10 in spatial coding.

        'The superposition function is found by summing across the receiver
        functions for each of the template’s receivers'

        """
        super_position_score = 0
        for bank in self.bank_of_receivers:
            winning_receiver_score = bank.receiver(position, time)
            super_position_score = super_position_score + \
                winning_receiver_score
        return super_position_score

    def match(self):
        """ equation 7 in spatial coding

        matching the base_word with the compare_word.
        """
        match = 0
        time = 0
        base_length = len(self.base_word)
        compare_length = len(self.compare_word)
        res_phase = self.find_resonating_phase(abs(base_length -
                                                   compare_length), time)
        len_word = len(self.base_word)
        match = 1/len_word*self.super_position(res_phase, time)
        return match

    def find_resonating_phase(self, max_dist, time):
        best_pos = (0, 0)
        for pos in range(-1*max_dist, max_dist):
            score = 0
            for bank in self.bank_of_receivers:
                score = score + bank.receiver(pos, time)
            if score > best_pos[1]:
                best_pos = (pos, score)
        return best_pos[0]

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
    sigma = 0

    def __init__(self, identity, n_clones, position, sigma):
        self.identity = identity
        clones = []
        for clone in range(n_clones):
            clones.append(None)
        self.clones = clones
        self.position = position
        self.sigma = sigma

    def update_clones(self, identity_input, pos_input, pos_self):
        if self.identity == identity_input:
            self.clones[pos_input] = self.receiver(pos_input, 0)
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

    def signal(self, letter_position, time):
        """ Equation 4 in spatial coding

        The signal function varies as a function of position, where the
        central tendency of the function represents the veridical letter
        position (posj), and the width of the function reflects the degree
        of letter position uncertainty.
        The signal function in Equation 4 also varies over time (t).

        Because the second part of this equation is equal to the spatial
        equation, I changed it here.
        """
        return self.activation(time)*self.spatial(letter_position)

    def activation(self, time):
        """ Calculate the activation level of a clone at a time.

        If there is a winning clone, the activation given for that clone is 1
        else there is no clone in this bank firing and the activation is 0
        """
        if self.winning_clone is None:
            return 0
        return 1

    def spatial(self, letter_pos):
        """ equation 1 in spatial coding

        letter_pos indexes the letters within the spatial code and goal_pos
        is the (veridical) serial position of the letter within the input
        stimulus.
        """
        power = (letter_pos-self.position)/self.sigma
        return math.exp(-1*power**2)

    def delay(self, letter_pos):
        """ the delay implemented by the SC model

        The value of delayri corresponds to the expected ordinal position of
        the corresponding letter within the template.
        """
        return self.position-letter_pos

    def receiver(self, letter_position, time):
        """ equation 9 in spatial coding.

        This equation calculates the activation of a receiver in a bank on a
        channel.
        The bank is the expected letter position.

        Not sure if identity or channel has to be implemented. in the SC
        paper
        it stands for the identity of the i'th word.
        """
        return self.signal(letter_position, time)-self.delay(letter_position)

    def printself(self):
        print self.identity
        for id_, clone in enumerate(self.clones):
            suffix = ''
            if id_ == self.winning_clone:
                suffix = ' <= winner'
            print str(id_+1)+" "+str(clone)+suffix


def test():
    sm = SpatialModel('stoop', 'stoop')
    sm.print_banks()
    print sm.match()

test()
