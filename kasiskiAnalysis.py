#Joseph Harrison 2019
#execute a kasiski analysis on
#a ciphertext that has been enciphered
#using the vigenere cipher
import re
from typing import List, Dict, Set
import frequencyAnalysis
import vigenereCipher

DistanceTable = Dict[str, List[int]]

#find repeating n-graphs and their distances
def repeating_graphs(n: int, string: str) -> DistanceTable:
    #store distances between consecutive
    #occurences
    ret = {}
    for i in range(n, len(string)):
        substr = string[i - n:i]
        if substr not in ret:
            ret[substr] = []
            #find all occurrences of substring
            matches = re.finditer(substr, string)
            matches = list(matches)
            for j in range(1, len(matches)):
                #distance between consecutive occurrences
                dist = matches[j].span()[0] \
                       - matches[j - 1].span()[0]
                ret[substr].append(dist)
    return ret

def factors(n: int) -> Set[int]:
    ret = set()
    for i in range(1, int(n ** 0.5)):
        #if divisible then factor
        if n % i == 0:
            ret.add(i)
    return ret

if __name__ == '__main__':
    #get the filename from user
    flag = True
    while flag:
        filename = input('filename: ')
        try:
            #try to make file handle
            handle = open(filename, 'r')
            flag = False
        except FileNotFoundError:
            print(f'file {filename} could not be found')

    #write file contents to ciphertext string
    ciphertext = ''
    for line in handle.readlines():
        ciphertext += line.replace('\n', '')

    handle.close()

    #record occurences of each factor
    factortable = {}

    sizeinput = ''
    #continue gathering n-graphs until 
    #the user has finished
    while sizeinput != 's':

        #get graph size from user
        flag = True
        while flag:
            try:
                n = int(input('graph size, n: '))
                flag = False
            except ValueError:
                print('must be integer')

        #table stores distances between consecutive n graphs
        dists = repeating_graphs(n, ciphertext)

        print(f'{n}-graph : distances : factors')

        for entry in dists:
            #only consider non empty entries
            if len(dists[entry]) != 0:
                #get list of factors of each distance
                factorset = list(map(factors, dists[entry]))
                #intersection gives possible keyword length
                #considering only this graph
                factorset = set.intersection(*factorset)
                print(f'{entry} : {dists[entry]} : {factorset}')
                #record factor
                for factor in factorset:
                    if factor not in factortable:
                        factortable[factor] = 1
                    else:
                        factortable[factor] += 1

        sizeinput = input('stop getting graphs (s): ')

    #output factors with occurences
    optimal = (0, 0)
    print('factor : occurrence')
    for factor in factortable:
        print(f'{factor :6} : {factortable[factor]}')
        #evaluate optimal factor by multiplying it by occurences
        if factor * factortable[factor] > optimal[1]:
            optimal = (factor, factortable[factor] * factor)
    
    p = optimal[0]

    print(f'most probable key length: {p}')

    ciphertext = ciphertext.lower()
    keyword = ''

    #frequency analysis on slices of ciphertext
    #gives keyword
    for i in range(p):
        k = (len(ciphertext) // (i + 1)) * (i + 1)
        subciphertext = [ciphertext[j] for j in range(i, k, p)]
        subciphertext = ''.join(subciphertext)
        _, _, shift = frequencyAnalysis.optimal_shift(subciphertext)
        keyword += frequencyAnalysis.alphabet[shift]

    print(f'most probable keyword: {keyword}')

    #decipher ciphertext
    plaintext = vigenereCipher.decipher(ciphertext, keyword)
    print(f'plaintext: {plaintext}')

