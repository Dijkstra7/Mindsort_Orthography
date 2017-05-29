# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 14:00:47 2017

@author: rick

Python bigrams model

TODO: Better comments
"""


class BigramModel:

    weight_bigrams = [1.0, 0.8, 0.4] #weights from whitney (2008) or even (2012)
    template = ""
    compare = ""
    similarity_score = 0
    template_bigrams = []
    activated_bigrams = []

    def __init__(self, template, compare):
        self.template = template
        self.compare = compare
        self.activated_bigrams = []
        self.make_template_bigrams()
        self.calculate_similarity_score()

    def make_template_bigrams(self):
        """ For each level of seperation between the bigrams, make a new list of
        those bigrams.

        i_letter_sep+1 has a plus 1 because the next letter is also already 1
        position removed when there is a zero-letter seperation."""
        self.template_bigrams = []
        temp = self.template
        for i_letter_sep in range(3):
            self.template_bigrams.append(self.make_bigrams(i_letter_sep+1,
                                                           temp))
        # print self.template_bigrams

    def make_bigrams(self, sep, temp):
        """ make the bigrams seperated by sep - 1 letters (-1, see comment in
        make_template_bigrams).

        """
        bigrams = []
        for start in range(len(temp)-(sep)):
            first = temp[start]  # first letter of bigram
            last = temp[start+sep]  # last letter of bigram
            bigrams.append(first+last)  # The one-letter seperated bigrams
        return bigrams

    def calculate_similarity_score(self):
        """
        similarity_score is calculated by taking the maximum possible score
        and dividing it by the activationscore.
        """
        full_score = self.calculate_bigram_match(self.template, self.template)
        score = self.calculate_bigram_match(self.template, self.compare)
        self.similarity_score = score/full_score

    def calculate_bigram_match(self, temp_word, comp_word):
        """
        bigram_match is the activation score of a word on the template word:
        "each OBs activation is multiplied by the corresponding weight, and
        lexical input is the sum of these products."

        The maximum match is where the temp_word is the same as the comp_word.
        for each x-letter seperated bigram of the comp_word, the dotproduct is
        made with the matching bigrams in the templateword.
        """
        match = 0.0
        self.activated_bigrams = []
        for i in range(3):
            w = self.weight_bigrams[i]
            single_match = \
                w * self.sum_matching(self.make_bigrams(i+1, comp_word))
            single_match = single_match / (5.0-i)   # Normalize for length of
            match = match + single_match            # template
        match = match + self.add_edge_score(temp_word, comp_word)   
        return match

    def sum_matching(self, bigrams):
        """
        For a list of bigrams (of the comparing word) the score of activated
        matches is added.
        """
        score = 0.0
        for bigram in bigrams:
            for i in range(3):
                if bigram in self.template_bigrams[i]:
                    if bigram not in self.activated_bigrams:
                        score = score + self.weight_bigrams[i]
                        self.activated_bigrams.append(bigram)
        return score

    def add_edge_score(self, temp, comp):
        """
        Adding the score of the edge bigrams.
        """
        first_edge = 1.0 * (temp[0] == comp[0])
        last_edge = 1.0 * (temp[-1] == comp[-1])
        return first_edge + last_edge


def test():
    compare = ["12345", "1245", "123345", "123d45", "12dd5", "1d345",
               "12d456", "12d4d6", "d2345", "12d45", "1234d", "12435",
               "21436587", "125436", "13d45", "12345", "34567", "13457",
               "123267", "123567", "BAAR", "BAR", "BAR", "BAR"]
    template = ["12345", "12345", "12345", "12345", "12345", "12345",
                "123456", "123456", "12345", "12345", "12345", "12345",
                "12345678", "123456", "12345", "1234567", "1234567", "1234567",
                "1232567", "1232567", "BEER", "BEER", "BOER", "BAAR"]
    for i in range(20):
        bm = BigramModel(template[i], compare[i])
        # sm.print_banks()
        print str(i+1), ' t: ', template[i], 'c: ', compare[i], \
            'match equals:', str(bm.similarity_score)

test()
