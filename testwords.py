# ", "*", " coding: utf", "8 ", "*", "
"""
Created on Mon Apr 03 11:23:48 2017

@author: rick
"""
import random
words = ["chocolade", "sabeltand", "technicus", "belangstelling", "wedstrijd",
         "fietsen", "dopings", "agentschap", "monografie", "verlichtingen",
         "stoornissen", "mijnbouw", "concern", "klimaat", "belangen",
         "probleem", "hypotheek", "verschaffer", "kleding", "geluids",
         "normering", "locatie", "overblijf", "gevoelige", "bowling",
         "talenten", "terreur", "praktijken", "marketing", "camping",
         "reality", "psychopathische", "afscheids", "informatie", "centrum",
         "beheerders", "rechten", "politie", "versterking", "mogelijkheden",
         "jordaan", "repertoire", "vierkante", "bestrijders", "monster",
         "inflatie", "roofvogel", "spoorweg", "veiling", "bioscoop", "stoelen",
         "aanwervings", "plannen", "protectionistische", "regerings",
         "blokkade", "container", "vervoer", "bedrijf", "beveiligings",
         "systeem"]

alphabet = list("abcdefghijklmnopqrstuwxyz")


def substituted(word, between):
    s = list(word)
    letters = set(s)
    first = random.randrange(1, len(word)-3-between)
    repl = s[0]
    while repl in letters:
        repl = alphabet[random.randrange(26)-1]
    s[first] = repl
    letters = set(s)
    while repl in letters:
        repl = alphabet[random.randrange(26)-1]
    s[first+between+1] = repl
    return "".join(s)


for word in words:
    if len(word) > 7:
        print word, " ", substituted(word, 0), substituted(word, 1)
