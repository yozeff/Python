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
            #present nodes to children
            for node in self.links:
                node.present(pattern, visited)

    #nullify hidden layer node values
    #this must be done before evaluating
    #weighted sum
    def nullify_hidden(self: Node) -> None:
        if self.inputnode == False:
            self.val = None
            for node in self.links:
                node.nullify_hidden()

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

    def backprop(self: Node, data: Matrix, lrate: Real) -> None:
        for pattern in data:
            pattern = list(pattern)
            #expected output from net
            exp = pattern.pop()
            #present pattern to net
            self.present(pattern, [])
            #nullify nodes before evaluating
            #weighted sum
            self.nullify_hidden()
            #actual output from net
            act = self.weighted_sum
            #evaluate dCdAct where
            #C = (act - exp)^2
            dCdAct = 2 * (act - exp) 
            #apply derivative to net
            self.apply_derivative(dCdAct, lrate)

    #apply the calculated dCdAct derivative
    #to weights
    def apply_derivative(self: Node, dCdAct: Real, lrate: Real) -> None:
        if self.inputnode == False:
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
            self.nullify_hidden()
            #sum error squared
            mes += (exp - self.weighted_sum) ** 2
        #mean
        mes /= len(data)
        return mes

#layers is the number of nodes in each layer
def make_net(layers: List[int]) -> List[Node]:
    outputs = [Node() for i in range(layers.pop())]
    lastlayer = outputs
    while len(layers) != 0:
        layer = [Node() for i in range(layers.pop())]
        for node in lastlayer:
            node.link(layer)
        lastlayer = layer
    return outputs

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    data = [[1, 1, 1],
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 0]]

    root = Node()
    root.link([Node(), Node()])

    data = [[1, 1, 0],
            [1, 0, 1],
            [0, 1, 1],
            [0, 0, 0]]
    
    root = Node()
    hidden = [Node(), Node(), Node()] 
    inputs = [Node(), Node()]
    for node in hidden:
        node.link(inputs)
    root.link(hidden)

    data = [[0.2, 0.8, 0.5, 1],
            [0.7, 0.3, 0.9, 0],
            [0.8, 0.3, 0.4, 0],
            [0.3, 0.6, 0.2, 1],
            [0.1, 0.5, 0.4, 1]]
    
    root = make_net([3, 1])[0]

    mesdata = []
    iterations = 10000
    if iterations >= 200:
        printwhen = iterations // 100
    else:
        printwhen = 1

    for i in range(iterations):
    
        if i % printwhen == 0:
            mes = root.mean_error_squared(data)
            mesdata.append((i, mes))
            print(f'epoch: {i} mes: {mes}')

        root.backprop(data, 0.01) 

    for pattern in data:
        pattern = list(pattern)
        exp = pattern.pop()
        print(f'pattern: {pattern}')
        root.present(pattern, [])
        root.nullify_hidden()
        act = root.weighted_sum
        print(f'exp: {exp} act: {act} err: {abs(exp - act)}')

    x, y = zip(*mesdata)
    plt.plot(x, y)
    plt.title('mes against time')
    plt.xlabel('time /epochs')
    plt.ylabel('mean error squared')
    plt.show()

