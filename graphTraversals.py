#Joseph Harrison 2019
#graph traversals

def depth_first(graph,current,visited=[]):
    visited.append(current)
    for vertex in graph[current]:
        if vertex not in visited:
            visited = depth_first(graph,vertex,visited)
    return visited

def breadth_first(graph,current):
    queue = [current]
    visited = []
    while len(queue) > 0:
        current = queue.pop(0)
        visited.append(current)
        for vertex in graph[current]:
            if vertex not in visited and vertex not in queue:
                queue.append(vertex)
    return visited
