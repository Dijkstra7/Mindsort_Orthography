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
    if current is None:
        return True
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
    banks_of_receivers = []
    base_word = 'spam'
    compare_word = 'eggs'

    def __init__(self, base_word, compare_word):
        sigma = self.calculate_sigma(len(compare_word))
        self.sigma = sigma
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
            self.banks_of_receivers.append(Bank(identity, len(input_),
                                                position, sigma))

        # Update the elimination within banks
        for position, identity in enumerate(input_):
            for bank_pos, bank in enumerate(self.banks_of_receivers):
                bank.update_receivers(identity, position, bank_pos)

        # Update the elmimination between banks
        for bank in self.banks_of_receivers:
            if bank.win_rec_pos is not None:
                bank.cross_bank_winner(self.banks_of_receivers)

    def print_banks(self, start=None, stop=None, step=1):
        """
        For testing purposes.
        """
        if start is None:
            start = 0
            stop = len(self.banks_of_receivers)
        if stop is None:
            stop = start+1
        for bank in range(start, stop, step):
            self.banks_of_receivers[bank].printself()

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
        for bank in self.banks_of_receivers:
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
        print res_phase
        return match

    def find_resonating_phase(self, max_dist, time):
        best_pos = (0, 0)
        for pos in range(-1*max_dist, max_dist):
            score = 0
            for bank in self.banks_of_receivers:
                score = score + bank.receiver(pos, time)
            if score > best_pos[1]:
                best_pos = (pos, score)
        return best_pos[0]

    def calculate_similarity(self, time):
        return 1  # receiver_output(time)+ext_letter_match(time)

    def ext_letter_match(time):
        for i in pie:
            'eat sky'


class Bank:
    """
    the structure of a receiver
    """
    identity = 'a'
    receivers = []
    position = -1
    win_rec_pos = -1
    winning_receiver_activation = 0
    sigma = 0

    def __init__(self, identity, n_receivers, position, sigma):
        self.identity = identity
        receivers = []
        for id_receiver in range(n_receivers):
            receivers.append(Receiver(id_receiver, False))
        self.receivers = receivers
        self.position = position
        self.sigma = sigma

    def update_receivers(self, identity_input, pos_input, pos_self):
        if self.identity == identity_input:
            self.receivers[pos_input].set_delay(pos_self)
        self.select_winner()

    def select_winner(self):
        win_id = 0
        self.receivers[0].won()
        for id_r, r in enumerate(self.receivers):
            if closer_to_0(self.receivers[win_id].delay, r.delay):
                self.receivers[win_id].lost()
                self.winning_receiver = id_r
                self.winning_clone_activation = \
                    self.receiver(self.position - self.winning_receiver, 0)
                win_id = id_r
                self.receivers[win_id].won()

    def cross_bank_winner(self, bank):
        for other_rec in bank:
            if self.identity == other_rec.identity:
                if closer_to_0(other_rec.receivers[self.win_rec_pos].delay,
                               self.receivers[self.win_rec_pos].delay):
                    self.receivers[self.win_rec_pos].lost()
                    self.win_rec_pos = None
                    self.winning_receiver_activation = 0
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
        return self.activation(letter_position,
                               time)*self.spatial(letter_position)

    def activation(self, position, time):
        """ Calculate the activation level of a clone at a time.

        If there is a winning clone, the activation given for that clone is 1
        else there is no clone in this bank firing and the activation is 0
        """
        if self.win_rec_pos == position:
            return 1
        return 0

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
        for id_, rec in enumerate(self.receivers):
            suffix = ''
            if rec.winning == True:
                suffix = ' <= winner'
            print str(id_+1)+" "+str(rec.delay)+suffix


class Receiver:
    winning = False
    position = None
    delay = None

    def __init__(self, position, winning):
        self.winning = winning
        self.position = position

    def won(self):
        self.winning = True

    def lost(self):
        self.winning = False

    def set_delay(self, difference):
        self.delay = self.position - difference


def test():
    sm = SpatialModel('brain', 'wetbrain')
    sm.print_banks()
    print str(sm.match())

test()
