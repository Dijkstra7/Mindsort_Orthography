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
    # Set up the parameters
    similarity_score = 0
    sigma_0 = 0.48  # As stated in table 3 in spatial coding.
    k_0 = 0.24      # As stated in table 3 in spatial coding.
    sigma = 0
    banks_of_receivers = []
    weight = 0
    base_word = 'spam'
    compare_word = 'eggs'
    ELM = True

    def __init__(self, base_word, compare_word, ELM=True):
        self.base_word = base_word
        self.compare_word = compare_word
        self.banks_of_receivers = []
        self.ELM = ELM

        # Calculate the sigma and weight of the gaussians.
        sigma = self.calculate_sigma(len(compare_word))
        self.sigma = sigma
        self.weight = 1.0/(len(base_word))
        if ELM:
            self.weight = 1.0/(len(base_word)+2)
        # Set up the receivers
        self.initialise_receivers(base_word, compare_word, sigma)

    def initialise_receivers(self, template, input_, sigma):
        """
        - Initialise the receivers based on the template
        - Activate the receivers
        - Deactivate the not-winning receivers
        """
        # Create the receivers.
        # print "-----------create receivers-----------"
        for position, identity in enumerate(template):
            self.banks_of_receivers.append(Bank(identity, len(input_),
                                                position, sigma))

        # Activate the receivers
        # print "-----------activate receivers---------"
        for position, identity in enumerate(input_):
            for bank_pos, bank in enumerate(self.banks_of_receivers):
                bank.activate_receivers(identity, position, bank_pos)

        # De-activate losing recievers in bank
        for bank in self.banks_of_receivers:
            bank.update_receivers()

        # Eliminate losing receivers between banks
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
        return 1.25  # self.sigma_0 + self.k_0*length

    def super_position(self, position, time):
        """ equation 10 in spatial coding.

        'The superposition function is found by summing across the receiver
        functions for each of the template’s receivers'

        """
        super_position_score = 0
        for bank in self.banks_of_receivers:
            winning_receiver_score = self.weight*bank.receiver(position,
                                                               time)
            super_position_score = super_position_score + \
                winning_receiver_score
        return super_position_score

    def match(self):
        """ equation 7 in spatial coding

        matching the base_word with the compare_word.
        """
        match_score = 0
        time = 0
        base_length = len(self.base_word)
        compare_length = len(self.compare_word)
        res_phase = self.find_resonating_phase(abs(base_length -
                                                   compare_length) + 1, time)
        match_score = self.super_position(res_phase, time)+self.ELM_score()
        return match_score

    def find_resonating_phase(self, max_dist, time):
        """
        The resonating phase corresponds to the value of the signal-weight
         difference where the superposition function is at its peak
        """
        min_dist = -1*max_dist
        best_pos = (min_dist, self.super_position(min_dist, 0))
        for pos in range(min_dist, max_dist):
            score = self.super_position(pos, 0)
            if score > best_pos[1]:
                best_pos = (pos, score)
        return best_pos[0]

    def ELM_score(self):
        if self.ELM is False:
            return 0
        score = 0
        if self.base_word[0] == self.compare_word[0]:
            score = score + self.weight
        if self.base_word[-1] == self.compare_word[-1]:
            score = score + self.weight
        return score


class Bank:
    """
    the structure of a receiver
    """
    identity = 'a'
    receivers = []
    position = -1
    win_rec_pos = 0
    sigma = 0

    def __init__(self, identity, n_receivers, position, sigma):
        self.identity = identity
        receivers = []
        for pos_receiver in range(n_receivers):
            receivers.append(Receiver(pos_receiver, False, sigma))
        self.receivers = receivers
        self.position = position
        self.sigma = sigma

    def activate_receivers(self, id_input, pos_input, pos_self):
        if self.identity == id_input:
            self.receivers[pos_input].set_delay(pos_self)

    def update_receivers(self):
        win_id = 0
        self.receivers[0].won()
        for id_r, r in enumerate(self.receivers):
            if closer_to_0(self.receivers[win_id].delay, r.delay):
                self.receivers[win_id].lost()
                self.win_rec_pos = id_r
                self.winning_clone_activation = \
                    self.receiver(self.position, 0)
                win_id = id_r
                self.receivers[win_id].won()

    def cross_bank_winner(self, bank):
        """ De-activates the reeiverbank if there is another receiver with
        less delay.
        """
        for other_rec in bank:
            if self.identity == other_rec.identity:
                if self.win_rec_pos >= len(other_rec.receivers):
                    break
                if closer_to_0(self.receivers[self.win_rec_pos].delay,
                               other_rec.receivers[self.win_rec_pos].delay):
                    self.receivers[self.win_rec_pos].lost()
                    self.win_rec_pos = None
                    self.winning_receiver_activation = 0
                    break

    def receiver(self, letter_position, time):
        """ Return the receiver value for the winning receiver.
        """
        if self.win_rec_pos is None:
            return 0
        return self.receivers[self.win_rec_pos].receiver(letter_position,
                                                         time)

    def printself(self):
        print 'id: ', self.identity
        for id_, rec in enumerate(self.receivers):
            suffix = ''
            if rec.winning is True:
                suffix = ' <= winner'
            print str(id_+1)+" "+str(rec.delay)+suffix


class Receiver:
    winning = False
    position = None
    delay = None
    sigma = 0

    def __init__(self, position, winning, sigma):
        self.winning = winning
        self.position = position
        self.sigma = sigma

    def won(self):
        self.winning = True

    def lost(self):
        self.winning = False

    def set_delay(self, difference):
        self.delay = self.position - difference

    def receiver(self, letter_position, time):
        """ equation 9 in spatial coding.

        self equation calculates the activation of a receiver in a bank on a
        channel.
        The bank is the expected letter position.

        Not sure if identity or channel has to be implemented. in the SC
        paper
        it stands for the identity of the i'th word.
        """
        return self.signal(letter_position,
                           time)  # - self.calculate_delay(letter_position)

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
        if self.winning is True:
            return 1
        return 0

    def spatial(self, letter_pos):
        """ equation 1 in spatial coding

        letter_pos indexes the letters within the spatial code and goal_pos
        is the (veridical) serial position of the letter within the input
        stimulus.
        """
        if self.delay is None:             # Ugly hack
            return 0
        power = (letter_pos-self.delay)/self.sigma
        return math.exp(-1*power**2)

    def calculate_delay(self, letter_pos):
        """ the delay implemented by the SC model

        The value of delayri corresponds to the expected ordinal position of
        the corresponding letter within the template.
        """
        return self.position-letter_pos


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
        sm = SpatialModel(template[i], compare[i], True)
        # sm.print_banks()
        print str(i+1), ' t: ', template[i], 'c: ', compare[i], \
            'match equals:', str(sm.match())

test()
