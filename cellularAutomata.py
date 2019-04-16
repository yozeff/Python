#Joseph Harrison 2019
#cellular automata using moore neighbourhood
import sys
import random
import time

LIVE = 'o'
DEAD = ' '

def parse_rulestr(rulestr):
    born, survive = rulestr.split('/')
    born = [int(char) for char in born]
    survive = [int(char) for char in survive]
    return born, survive

def apply_rulestr(array, born, survive):
    x, y = len(array[0]), len(array)
    #next state of automata
    nextarray = [[DEAD for i in range(x)]
                for j in range(y)]
    for i in range(y):
        for j in range(x):
            #number of live neighbours
            live = 0
            for k in range(-1, 2):
                for l in range(-1, 2):
                    #don't consider cell being evaluated
                    if k != 0 or l != 0:
                        if array[(i + k) % y][(j + l) % x] == LIVE:
                            live += 1
            #apply rules
            if array[i][j] == LIVE:
                if live in survive:
                    #cell survives to next state
                    nextarray[i][j] = LIVE
            else:
                if live in born:
                    #cell becomes alive
                    nextarray[i][j] = LIVE
    return nextarray

#create and populate an array according to prob
def make_array(i, j, prob):
    array = [[DEAD for k in range(j)] 
                   for l in range(i)]
    #populate
    for k in range(i):
        for l in range(j):
            rnum = random.random()
            if rnum <= prob:
                array[k][l] = LIVE
    return array

if __name__ == '__main__':
    #get rulestr, prob and sizes from sys
    rulestr = sys.argv[1]
    prob = float(sys.argv[2])
    y, x = int(sys.argv[3]), int(sys.argv[4])
    born, survive = parse_rulestr(rulestr)
    #create initial array
    array = make_array(y, x, prob) 
    while True:
        #print array
        arraystr = ''
        for row in array:
            arraystr += ''.join(row) + '\n'
        arraystr += '-' * x
        print(arraystr)
        #apply rules to create next state
        array = apply_rulestr(array, born, survive)
        time.sleep(0.1)

