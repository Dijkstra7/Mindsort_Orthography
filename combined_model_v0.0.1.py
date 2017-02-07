# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 09:28:54 2017

@author: rick
kijken of dit werkt.
"""
import numpy as np
from random import random
alphabet = [i for i in "abcdefghijklmnopqrstuvwxyz"]
def makebigrams(l):
    l2 = []
    for i in l:
        for j in l:
            l2.append(i+j)
    return l2
    
bigralphabet = makebigrams(alphabet)
    
def calcmscores(word):
    lw = len(word)+2
    scores = [.05, .2, .5, .2, .05]
    mtrxletters = []
    mscores=[]
    for idx,i in enumerate(word):
        row = [0]*lw
        for idxk,k in enumerate(scores):
            if (idx+idxk-1)>0 and idx+idxk-2<lw-1:
                row[idx+idxk-1] = k
                if idx==0:
                    row[idx+idxk-1] = k+0.25                    
        mtrxletters.append((i,row))
    for idxi,(idi,l) in enumerate(mtrxletters):
        for idxj,(idj,lj) in enumerate(mtrxletters[idxi+1:]):
            if idi==idj:
                l=[l[u]+lj[u] for u in range(len(l))]
                mtrxletters[idxj+idxi+1]=('',[])
        if idi: 
            mscores.append((idi,l))
    return mscores

def calcbigrams(word):
    mscores = calcmscores(word)
    wrdset = [(idx, letter) for idx,(letter,scores) in enumerate(mscores)]
    mbiscores=[]
    for (idi,i) in wrdset:
        for (idj,j) in wrdset:
            li = mscores[idi][1]
            lj = mscores[idj][1]
            lij = [li[u]+lj[u+1] for u in range(len(li)-1)]
            for (idx,k) in enumerate(lij):
                if k<0.25:
                    lij[idx]=0
            mbiscores.append((i+j,lij))
    return mbiscores

def compwords(w1,w2):
    scorew1 = calcbigrams(w1)
    scorew2 = calcbigrams(w2)
    biw1 = [bigram for (bigram,scores) in scorew1]
    biw2 = [bigram for (bigram,scores) in scorew2]
    scw1 = [scores for (bigram,scores) in scorew1]
    scw2 = [scores for (bigram,scores) in scorew2]
    bigramset = set([bigram for (bigram,scores) in scorew1]+[bigram for (bigram,scores) in scorew2])    
    score = 0
    lenrowscore = len(scorew1[0][1])
    for bigram in bigramset:
        birow1 = [0]*lenrowscore
        birow2 = [0]*lenrowscore        
        if bigram in biw1:
            idx = biw1.index(bigram)
            birow1 = scw1.pop(idx)
            biw1.pop(idx)
        if bigram in biw2:
            idx = biw2.index(bigram)
            birow2 = scw2.pop(idx)
            biw2.pop(idx)
        score = score+sum([abs(a-b) for (a,b) in zip(birow1,birow2)])
    return score
print compwords('12345','12245')           

constraints5 = [
"12345",
"1245",
"123345",
"12dd5",
"12d45",
"12435",
"d12345",
"12345d",
"21345",
"d2345",
"1234d",
"14325",
"2345"
]

constraint6 = [
"123256",
"123456"
]

constraints7 = [
"12345",
"34567",
"13457"
]

for i in constraints5:
    print "sim("+i+",12345)=" + str((50-compwords(i,"12345"))/50)


for i in constraint6:
    print "sim("+i+",1232456)=" + str((50-compwords(i,"1232456"))/50)


for i in constraints7:
    print "sim("+i+",1234567)=" + str((50-compwords(i,"1234567"))/50)
 