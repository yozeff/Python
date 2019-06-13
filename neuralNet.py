#Joseph Harrison 2019
#neural net using relu and backprop
import numpy as np
from typing import NewType, List, TypeVar
import random

Node = NewType('Node', object)
Real = TypeVar('Real', int, float)
Matrix = List[List[Real]]

ReLU = lambda x: 0 if x < 0 else x 
invReLU = lambda x: 0 if x == 0 else x
ReLUPrime = lambda x: 0 if x == 0 else 1

class Node:

    def __init__(self: Node) -> None:
        self.inputnode = True
        self.links = []
        self.wts = []
        self.bias = 0
        self.val = None

    #create links between nodes
    def link(self: Node, nodes: List[Node]) -> None:
        #raise error on empty list
        if len(nodes) == 0:
            raise ValueError('cannot be empty')
        else:
            #this node is no longer an input
            self.inputnode = False
            for node in nodes:
                self.links.append(node)
                self.wts.append(random.random())

    #present a pattern to net
    #this will set the values of the
    #input nodes
    def present(self: Node, pattern: List[Real], visited: List[Node]) -> None:
        if self.inputnode:
            try:
                if self not in visited:
                    self.val = pattern.pop(0)
                    visited.append(self)
            except IndexError:
                raise ValueError('insufficient pattern')
        else:
            #nullify value
            self.val = None
            #present nodes to children
            for node in self.links:
                node.present(pattern, visited)

    @property
    def weighted_sum(self: Node) -> Real:
        #if a nodes value is not none
        #this node has already been
        #evaluated
        if self.inputnode or self.val != None:
            return self.val
        else:
            #weighted sums of children
            x = []
            for node in self.links:
                x.append(node.weighted_sum)
            self.val = np.dot(x, self.wts)
            self.val += self.bias
            self.val = ReLU(self.val)
            return self.val

    #apply the calculated dCdAct derivative
    #to weights
    def apply_derivative(self: Node, dCdAct: Real, lrate: Real) -> None:
        if not self.inputnode:
            #sigma = x . wts + bias
            sigma = invReLU(self.val)
            dCdSigma = dCdAct * ReLUPrime(sigma)
            #recursive call on links
            dCdx = np.multiply(dCdSigma, self.wts)
            for i, node in enumerate(self.links):
                node.apply_derivative(dCdx[i], lrate)
            #dCdWts = dCdAct * dActdSigma * dSigmadWts
            x = [node.val for node in self.links]
            dCdWts = np.multiply(dCdSigma, x)
            #apply derivative to weights and bias
            self.wts -= dCdWts * lrate
            self.bias -= dCdSigma * lrate

    def mean_error_squared(self: Node, data: Matrix) -> Real:
        mes = 0
        for pattern in data:
            pattern = list(pattern)
            #expected output
            exp = pattern.pop()
            self.present(pattern, [])
            #sum error squared
            mes += (exp - self.weighted_sum) ** 2
        #mean
        mes /= len(data)
        return mes

    #remove weights that fall below threshold
    def prune(self: Node, threshold: Real) -> None:
        newWts = []
        newlinks = []
        for i, wt in enumerate(self.wts):
            if abs(wt) >= threshold:
                newWts.append(wt)
                newlinks.append(self.links[i])
            else:
                print(f'pruned a node with weight {wt}')
        self.wts = list(newWts)
        self.links = list(newlinks)
        #recursive call on remaining nodes
        for node in self.links:
            node.prune(threshold)

Layer = List[Node]

def backprop(outputs: Layer, data: Matrix, lrate: Real) -> None:
    for pattern in data:
        pattern = list(pattern)
        #expected output from net
        exp = np.array([pattern.pop() for 
                        node in outputs])
        exp = np.flip(exp)
        #present pattern to net
        outputs[0].present(pattern, [])
        #actual output from net
        act = np.array([node.weighted_sum 
                        for node in outputs])
        #evaluate dCdAct where
        #C = (act - exp)^2
        dCdAct = 2 * (act - exp)
        #apply derivative to net
        for i, node in enumerate(outputs):
            node.apply_derivative(dCdAct[i], lrate)

#layers is the number of nodes in each layer
def make_net(layers: List[int]) -> Layer:
    outputs = [Node() for i in range(layers.pop())]
    lastlayer = outputs
    while len(layers) != 0:
        layer = [Node() for i in range(layers.pop())]
        for node in lastlayer:
            node.link(layer)
        lastlayer = layer
    return outputs

if __name__ == '__main__':
    import timeit
    
    #(A ^ B) ^ (C ^ ~D)
    #some vectors are incorrect
    #the network is still able
    #to detect the correct patterns
    data = [[0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 1, 0, 0, 1],
            [0, 1, 0, 1, 0],
            [0, 1, 1, 0, 0],
            [0, 1, 1, 1, 0],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0],
            [1, 0, 1, 0, 0],
            [1, 0, 1, 1, 0],
            [1, 1, 0, 0, 0],
            [1, 1, 0, 1, 0],
            [1, 1, 1, 0, 1],
            [1, 1, 1, 1, 0]]

    roots = make_net([4, 2, 1])

    iterations = 7500
    start = timeit.default_timer()
    lrate = 0.01

    if iterations > 100:
        prunewhen = iterations // 50
    else:
        prunewhen = 5

    for i in range(iterations):
    
        if i % prunewhen == 0:
            mes = [root.mean_error_squared(data)
                   for root in roots]
            print(f'epoch: {i} mes: {mes}')
            roots[0].prune(0.01)

        backprop(roots, 
                np.random.combination(data), lrate)
    
    end = timeit.default_timer()
    print(f'finished training in {end - start}s')

    for pattern in data:
        roots[0].present(list(pattern), [])
        act = np.array([root.weighted_sum for root in roots])
        print(pattern[:-len(roots)] + np.ndarray.tolist(act))

    queue = list(roots)
    while len(queue) != 0:
        current = queue.pop()
        print(f'bias: {current.bias}')
        for i, node in enumerate(current.links):
            print(current.wts[i])
            if node not in queue:
                queue.append(node)


