#Joseph Harrison 2019
#1D cellular automata hashing
#using extended von neumann neighbourhood
import random as r
import sys

LIVE = '1'
DEAD = '0'

def parse_rulestr(rulestr):
    born, surv = rulestr.split('/')
    born = [int(elem) for elem in born]
    surv = [int(elem) for elem in surv]
    return born, surv

def apply_rulestr(bitstr, born, surv):
    result = list(bitstr)
    for i in range(len(bitstr)):
        #get number of live neighbours
        live = 0
        for j in range(-2, 3):
            if bitstr[(i + j) % len(bitstr)] == LIVE:
                live += 1
        #apply rules given by born and surv lists
        if bitstr[i] == LIVE and live in surv:
            result[i] = LIVE
        elif bitstr[i] == DEAD and live in born:
            result[i] = LIVE
        else:
            result[i] = DEAD
    return ''.join(result)

if __name__ == '__main__':
    #get command line arguments
    message = sys.argv[1]
    bitstr = [format(ord(char), 'b') for char in message]
    bitstr = ''.join(bitstr)
    original = bitstr
    rulestr = sys.argv[2]
    iterations = int(sys.argv[3])
    born, surv = parse_rulestr(rulestr)
    #run cellular automata over iterations
    for i in range(iterations):
        bitstr = apply_rulestr(bitstr, born, surv)
    #output result
    print(f'original: {original}')
    print(f'hashed:   {bitstr}')

