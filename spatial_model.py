# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 14:29:49 2017

@author: rick
"""

# Imports


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

    def __init__(self, base_word, compare_word):
        self.sigma = calculate_sigma(len(compare_word))
        self.similarity_score = \
            self.calculate_similarity(base_word, compare_word)

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
        self.sigma = sigma_0+k_0*length

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
        activation_letter = activation(letter, time)
        return activation_letter*spatial(letter_pos, goal_pos)

    def delay(goal_pos, letter_pos):
        """ the delay implemented by the SC model

        The value of delayri corresponds to the expected ordinal position of
        the corresponding letter within the template.
        """
        return goal_pos-letter_pos

    def reciever(self, bank, channel, identity, letter, position, time):
        """ equation 9 in spatial coding.

        This equation calculates the activation of a reciever in a bank on a
        channel.
        The bank is the expected letter position.

        Not sure if identity or channel has to be implemented. in the SC paper
        it stands for the identity of the i'th word.
        """
        return signal(bank, position, time, letter)-delay(bank, position)

    def winning_reciever(recievers, position, time):
        """ calculate the score of the winning reciever

        The winning reciever is that reciever that is closest to 0.
        """
        winning_score = 99
        for (rec_letter, rec_pos) in recievers:
            rec_score = reciever(rec_pos, None, None, rec_letter, position,
                                 time)
            if abs(abs(winning_score) - abs(rec_score)) > 0:
                winning_score = rec_score
        return winning_score

    def super_position(banks_of_recievers, identity, position, time):
        """ equation 10 in spatial coding.

        'The superposition function is found by summing across the receiver
        functions for each of the template’s receivers'

        """
        super_position_score = 0
        for bank in banks_of_recievers:
            winning_reciever_score = winning_reciever(bank, position, time)
            super_position_score = super_position_score + \
                winning_reciever_score
        return super_position_score

    def calculate_similarity(self, baseword, compare_word):
        reutn 'to be mplemented'