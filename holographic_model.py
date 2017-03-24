# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 12:35:13 2017

@author: rick
"""
import numpy as np


class HoloModel:

    similarity_score = 0.0
    template = ""
    compare = ""
    used_letters = []
    letter_vectors = []
    position_vectors = []
    max_pos = 0
    num_trials = 100
    start_sparse = None
    do_sparse = False

    def __init__(this, template, compare):
        this.template = template
        this.compare = compare
        s = set(compare+template)
        this.get_used_letters(s)
        this.similarity_score = this.calculate_similarity("Slot coding")

    def create_position_vectors(this):
        this.position_vectors = []
        num_positions = max(len(this.compare), len(this.template))
        for position in range(num_positions):
            this.position_vectors.append(HoloRep(True, "", this.start_sparse))
            if this.do_sparse:
                this.start_sparse = this.start_sparse + 1

    def create_letter_vectors(this):
        this.letter_vectors = []
        for letter in this.used_letters:
            this.letter_vectors.append(HoloRep(False, letter,
                                               this.start_sparse))
            if this.do_sparse:
                this.start_sparse = this.start_sparse + 1

    def get_used_letters(this, s):
        for i in range(len(s)):
            this.used_letters.append(s.pop())

    def chunk_rule(this, vector_1, vector_2):
        new_vector = [this.x_or(x) for x in zip(vector_1, vector_2)]
        return new_vector

    def x_or(this, elements):
        if elements[0] == elements[1]:
            return 0
        return 1

    def bind_rule(this, vectors):
        number_vectors = len(vectors)
        new_vector = []
        for element_id in range(len(vectors[0])):
            maj_score = 0
            for i in range(number_vectors):
                maj_score = maj_score + vectors[i][element_id] * 2 - 1
            if maj_score > 0:
                new_vector.append(1)
            elif maj_score < 0:
                new_vector.append(0)
            else:
                new_vector.append(np.random.choice(2, 1)[0])
        # print np.sum(new_vector)
        return new_vector

    def hamming_similarity(this, vector_1, vector_2):
        sim_score = 0.0
        for i, j in zip(vector_1, vector_2):
            if i == j:
                sim_score = sim_score + 1.0
        ham_score = 1.0 - sim_score / len(vector_1)
        return ham_score

    def calculate_similarity(this, method="Slot coding"):
        sim_score = 0.0
        if method == "Slot coding":
            for i in range(this.num_trials):
                sim_score = sim_score + this.calculate_similarity_slotcoding()
        return sim_score / this.num_trials

    def calculate_similarity_slotcoding(this):
        if this.do_sparse:
            this.start_sparse = 0
        this.create_letter_vectors()
        this.create_position_vectors()
        compare_vector = this.set_vectors(this.compare)
        # this.create_letter_vectors()
        template_vector = this.set_vectors(this.template)
        return this.similarity(compare_vector, template_vector)

    def set_vectors(this, word):
        return this.bind_rule(this.chunk_positions_and_letters(word))

    def chunk_positions_and_letters(this, word):
        vectors = []
        for i in range(len(word)):
            vectors.append(this.chunk_rule(this.position_vectors[i].vector,
                                           this.find_vector(word[i])))
        # print [np.sum(x) for x in vectors]
        return vectors

    def find_vector(this, letter):
        for vector in this.letter_vectors:
            if vector.identity == letter:
                return vector.vector

    def similarity(this, vector_1, vector_2):
        """Correcting for the fact that my vectors are not orthogonal.

        Altough it is an ugly fix, it still produces the same numbers as
        mentioned in the paper
        """
        c = this.hamming_similarity(vector_1, vector_2)
        # print c
        return 1.0 - (2.0 * abs(c))


class HoloRep:

    identity = ""
    is_position = False
    vector = []
    vector_dimension = 1000

    def __init__(this, is_pos, identity="", start_sparse=None):
        this.vector = this.generate_vector(this.vector_dimension,
                                           start_sparse)
        if is_pos is False:
            this.identity = identity
        this.is_position = is_pos

    def generate_vector(this, size, start_sparse=None):
        if start_sparse is None:
            halfsize = size / 2
            halfsizeodd = size / 2 + size % 2
            vector = np.array([0] * halfsize + [1] * halfsizeodd)
            np.random.shuffle(vector)
            return vector
        vector = []
        for i in range(10):
            if i == start_sparse:
                addvector = 100*[1]
            else:
                addvector = 100*[0]
            vector = vector + addvector
        return vector


def test():
    hm = HoloModel("12345", "1245")
    print hm.similarity_score
    tl = []
    for i in range(3):
        tl.append(HoloRep(True).vector)
    print hm.hamming_similarity(tl[0], hm.chunk_rule(tl[0], np.ones(1000)))


test()
