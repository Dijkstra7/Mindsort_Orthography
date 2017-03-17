""" 
Python bigrams editor
TODO: Better comments
"""
class BigramModel:

    weight_bigrams = [1.0, 0.8, 0.4]
    template = ""
    compare = ""
    similarity_score = 0
    template_bigrams = []

    def __init__(this, template, compare):
        this.template = template
        this.compare = compare
        this.make_template_bigrams()
        this.calculate_similarity_score()

    def make_template_bigrams(this):
        """ For each level of seperation between the bigrams, make a new list of
        those bigrams.

        i_letter_sep+1 has a plus 1 because the next letter is also already 1
        position removed when there is a zero-letter seperation."""
        temp = this.template
        for i_letter_sep in range(3):
            this.template_bigrams.append(this.make_bigrams(i_letter_sep+1, temp))

    def make_bigrams(this, sep, temp):
        """ make the bigrams seperated by sep - 1 letters (-1, see comment in
        make_template_bigrams).

        """
        bigrams = []
        for start in range(len(temp)-(sep)):
            first = temp[start]  # first letter of bigram
            last = temp[start+sep]  # last letter of bigram
            bigrams.append(first+last)  # The one-letter seperated bigrams
        return bigrams

    def calculate_similarity_score(this):
        """
        similarity_score is calculated by taking the maximum possible score and
        dividing it by the activationscore.
        """
        full_score = this.calculate_bigram_match(this.template, this.template)
        score = this.calculate_bigram_match(this.template, this.compare)
        this.similarity_score = score/full_score

    def calculate_bigram_match(this, temp_word, comp_word):
        """
        bigram_match is the activation score of a word on the template word:
        "each OB’s activation is multiplied by the corresponding weight, and
        lexical input is the sum of these products."

        The maximum match is where the temp_word is the same as the comp_word.
        for each x-letter seperated bigram of the comp_word, the dotproduct is made
        with the matching bigrams in the templateword.
        """
        match = 0.0
        for i in range(3):
            w = this.weight_bigrams[i]
            match = match + w * this.sum_matching(this.make_bigrams(i+1, comp_word))
        return match
        
    def sum_matching(this, bigrams):
        """
        For a list of bigrams (of the comparing word) the score of activated matches
        is added.
        """
        score = 0.0
        for bigram in bigrams:
            for i in range(3):
                if bigram in this.template_bigrams[i]:
                    score = score + this.weight_bigrams[i]
        return score
