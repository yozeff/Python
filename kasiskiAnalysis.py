#Joseph Harrison 2019
#execute a kasiski analysis on
#a ciphertext that has been enciphered
#using the vigenere cipher
import re
from typing import List, Dict, Set
from indexOfCoincidence import index_of_coincidence, ALPHABET
from frequencyAnalysis import optimal_shift

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

def get_factors(n: int) -> Set[int]:
    ret = set()
    for i in range(1, int(n ** 0.5)):
        #if divisible then factor
        if n % i == 0:
            ret.add(i)
    return ret

def get_cosets(string: str, n: int) -> List[str]:
    ret = ['' for i in range(n)]
    for i in range(len(string)):
        ret[i % n] += string[i]
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
        line = line.replace('\n', '')
        line = line.lower()
        ciphertext += line.replace(' ', '')

    handle.close()

    #total set of factors
    factorset = set()

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
                factorsubset = list(map(get_factors, dists[entry]))
                #intersection gives possible keyword length
                #considering only this graph
                factorsubset = set.intersection(*factorsubset)
                print(f'{entry} : {dists[entry]} : {factorset}')
                #union of factor sets - collect unique factors
                factorset = factorset | factorsubset

        sizeinput = input('stop getting graphs (s): ')

    #disregard factor 1
    factorset.remove(1)

    #factor yielding the best ic
    optimal = (0, 0)

    print('factor : mean IC')

    #evaluate indices of coincidence
    for factor in factorset:
        #make cosets
        cosets = get_cosets(ciphertext, factor)
        meanic = sum(map(index_of_coincidence, cosets))
        meanic /= factor
        print(f'{factor} : {meanic}')
        #update optimal factor
        if meanic > optimal[1]:
            optimal = (factor, meanic)

    factor = optimal[0]

    print(f'optimal factor: {factor}')

    #determine keyword
    keyword = ''
    cosets = get_cosets(ciphertext, factor)
    for i in range(factor):
        #frequency analysis on coset
        caesartable, _, shift = optimal_shift(cosets[i])
        keyword += ALPHABET[shift]
        decryptedcoset = ''
        #decrypt cosets
        for j in range(len(cosets[i])):
            decryptedcoset += caesartable[cosets[i][j]]
        cosets[i] = decryptedcoset

    #put cosets into plaitext string
    cosets = list(map(list, cosets))
    plaintext = ''
    for item in zip(*cosets):
        plaintext += ''.join(item)

    print(f'keyword: {keyword}')
    print(f'plaintext: {plaintext}')

