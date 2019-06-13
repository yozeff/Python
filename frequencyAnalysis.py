#Joseph Harrison 2019
#alphabetic frequency analysis for
#caesar ciphers
from typing import Dict, Tuple
import numpy as np

#https://en.wikipedia.org/wiki/Letter_frequency
freqtable = {'a' : 0.08167,
             'b' : 0.01492,
             'c' : 0.02782,
             'd' : 0.04253,
             'e' : 0.12702,
             'f' : 0.02228,
             'g' : 0.02015,
             'h' : 0.06094,
             'i' : 0.06966,
             'j' : 0.00153,
             'k' : 0.00772,
             'l' : 0.04025,
             'm' : 0.02406,
             'n' : 0.06749,
             'o' : 0.07507,
             'p' : 0.01929,
             'q' : 0.00095,
             'r' : 0.05987,
             's' : 0.06327,
             't' : 0.09056,
             'u' : 0.02758,
             'v' : 0.00978,
             'w' : 0.02360,
             'x' : 0.00150,
             'y' : 0.01974,
             'z' : 0.00074}

alphabet = list(freqtable.keys())

def make_rel_freqtable(ciphertext: str) -> Dict[str, float]:
    #links characters to there relative frequencies
    ret = {key:0 for key in alphabet}
    for char in ciphertext:
        ret[char] += 1
    for entry in ret:
        ret[entry] /= len(ciphertext)
    return ret

CaesarTable = Dict[str, str]

#make a table for deciphering
def make_caesar_table(shift: int) -> CaesarTable:
    ret = {}
    for i in range(len(alphabet)):
        ret[alphabet[(i + shift) % len(alphabet)]] = alphabet[i]
    return ret

def optimal_shift(ciphertext: str) -> Tuple[CaesarTable, float, int]:
    relfreqtable = make_rel_freqtable(ciphertext)
    optimal = ({}, np.inf, 0)
    #test different shifts
    for shift in range(len(alphabet)):
        caesartable = make_caesar_table(shift)
        #evaluate chi-squared
        #between frequencies
        chi = 0
        for char in alphabet:
            a = freqtable[caesartable[char]]
            b = relfreqtable[char]
            chi += (a - b) ** 2
        chi /= len(alphabet)
        #optimal table is decided
        #chi-squared value
        if chi < optimal[1]:
            optimal = (caesartable, chi, shift)
    return optimal

if __name__ == '__main__':
    cont = ''
    while cont != 'q':
        ciphertext = input('ciphertext: ')
        ciphertext = ciphertext.replace(' ', '').lower()
        caesartable = optimal_shift(ciphertext)[0]
        plaintext = ''
        for char in ciphertext:
            plaintext += caesartable[char]
        print(f'plaintext: {plaintext}')
        cont = input('quit (q): ')

