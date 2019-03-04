#Joseph Harrison 2019
#dijkstra's algorithm
import math as m

#traditional implementation
#i.e: calculates weight of shortest path, but doesn't
#return vertices in path
def dijkstra(graph,start,end):
    path = {}
    path[start] = 0
    #label all adjacent vertices to start with weight given in graph
    for vertex in graph[start]:
        path[vertex[0]] = vertex[1]
    #label all remaining vertices with infintite weights
    for vertex in [vertex for vertex in graph if vertex not in path]:
        path[vertex] = m.inf
    #T is the set of elements for which the shortest path to a has not
    #been found
    T = [vertex for vertex in path if vertex != start]
    while end in T:
        #choosing current as vertex with minimum path
        current = ('a',m.inf)
        for vertex in T:
            if path[vertex] <= current[1]:
                current = (vertex,path[vertex])
        current = current[0]
        #setting shortest path from current
        T.remove(current)
        for vertex in graph[current]:
            path[vertex[0]] = min(path[vertex[0]],path[current] + vertex[1])
    return path
