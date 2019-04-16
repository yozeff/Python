#Joseph Harrison 2019
import random
import math
import sys
from aStar import a_star_search
from aStar import reconstruct_path

SPACE = ' '
WALL = 'o'
START = 's'
GOAL = 'g'

def make_array(x, y, prob):
    array = [[SPACE for i in range(x)]
                    for j in range(y)]
    #randomly populate with walls
    for i in range(y):
        for j in range(x):
            rnum = random.random()
            if rnum <= prob:
                array[i][j] = WALL
    return array

#using moore neighbourhood
def get_neighbours(array, vertex):
    neighbours = {}
    j, i = vertex
    x, y = len(array[0]), len(array)
    for k in range(-1, 2):
        for l in range(-1, 2):
            #don't consider vertex
            if k != 0 or l != 0:
                #check for valid neighbour
                if i + k < 0 or i + k >= y:
                    continue
                elif j + l < 0 or j + l >= x:
                    continue
                elif array[i + k][j + l] != WALL:
                    neighbour = j + l, i + k
                    neighbours[neighbour] = math.hypot(l, k)
    return neighbours

if __name__ == '__main__':
    #get args from command line
    x = int(sys.argv[1])
    y = int(sys.argv[2])
    prob = float(sys.argv[3])
    #create array, start and goal
    array = make_array(x, y, prob)
    start = (0, 0)
    goal = (x - 1, y - 1)
    #create adjacency list of array
    #and H set of heuristics
    graph = {}
    H = {}
    for i in range(x):
        for j in range(y):
            #heuristic cost is euclidean distance
            H[(i, j)] = math.hypot(i - goal[0], 
                                   j - goal[1])
            #graph of neighbours
            graph[(i, j)] = get_neighbours(array, (i, j))
    totalpath = a_star_search(graph, start, goal, H)
    if totalpath != None:
        #write path to array
        for j, i in totalpath:
            array[i][j] = 'p'
    else:
        print('not possible')
    array[start[1]][start[0]] = START
    array[goal[1]][goal[0]] = GOAL
    #display result
    for row in array:
        print(' '.join(row))

