# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 13:41:46 2017

@author: rick

The bigram model according to the hannigan paper, which is using the
constraints.
"""

class BigramModelHannigan:
    
    template = ""
    compare = ""
    similarity_score = 0
    template_bigrams = []
    constrain_temp = 3
    constrain_comp = 3

    def __init__(self, template, compare, constrained=True):
        self.template = template
        self.compare = compare
        if not constrained:
            self.constrain_temp = len(template)
            self.constrain_comp = len(compare)
        self.make_template_bigrams()
        self.calculate_similarity_score()

    def make_template_bigrams(self):
        """ For each level of seperation between the bigrams, make a new list of
        those bigrams.

        i_letter_sep+1 has a plus 1 because the next letter is also already 1
        position removed when there is a zero-letter seperation."""
        temp = self.template
        for i_letter_sep in range(self.constrain_temp):
            self.template_bigrams.append(self.make_bigrams(i_letter_sep+1,
                                                           temp))

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
        for i in range(self.constrain_comp):
            match = match + \
                self.sum_matching(self.make_bigrams(i+1, comp_word))
        return match

    def sum_matching(self, bigrams):
        """
        For a list of bigrams (of the comparing word) the score of activated
        matches is added.
        """
        score = 0.0
        for bigram in bigrams:
            for i in range(self.constrain_temp):
                if bigram in self.template_bigrams[i]:
                    score = score + 1
        return score


def test():
    bm = BigramModelHannigan("12345", "123d45", False)
    print bm.similarity_score

test()
