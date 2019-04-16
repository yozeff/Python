#Joseph Harrison 2019
#a star search in directed acyclic graph
import math

#a star search returns path from start to goal
def a_star_search(graph, start, goal, H):
    closedset = []
    openset = [start]
    #most efficient way to approach a node
    camefrom = {}
    
    #cost of getting from start to each node
    gscore = {vertex : math.inf for vertex in graph}
    gscore[start] = 0

    #cost of getting from start to end through each node
    fscore = {vertex : math.inf for vertex in graph}
    fscore[start] = H[start]

    while len(openset) != 0:
        
        #choose the vertex in openset with lowest fscore
        current = '', math.inf
        for vertex in openset:
            if fscore[vertex] < current[1]:
                current = vertex, fscore[vertex]
        current = current[0]
    
        if current == goal:
            return reconstruct_path(camefrom, current)

        openset.remove(current)
        closedset.append(current)

        for neighbour in graph[current]:
            #we can ignore this vertex
            if neighbour in closedset:
                continue

            tentGScore = gscore[current] + graph[current][neighbour]

            #discover neighbour
            if neighbour not in openset:
                openset.append(neighbour)
            elif tentGScore >= gscore[neighbour]:
                continue

            #best path
            camefrom[neighbour] = current
            gscore[neighbour] = tentGScore
            fscore[neighbour] = gscore[neighbour] + H[neighbour]

def reconstruct_path(camefrom, current):
    totalpath = [current]
    while current in camefrom.keys():
        current = camefrom[current]
        totalpath.append(current)
    return totalpath

if __name__ == '__main__':
    #storing graph using adjacency list
    graph = {'s' : {'a': 1, 'b': 4},
             'a' : {'b': 2, 'c': 5, 'g': 12},
             'b' : {'c': 2},
             'c' : {'g': 3},
             'g' : {}}
    #set of admissable heuristics
    H = {'s': 7,
         'a': 6,
         'b': 2,
         'c': 1,
         'g': 0}
    #shortest path between a and g
    totalpath = a_star_search(graph, 'a', 'g', H)
    totalpath = reversed(totalpath)
    print('optimal path')
    print(' -> '.join(totalpath))

