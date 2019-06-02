#Joseph Harrison 2019
#neural net using relu and backprop
import numpy as np
from typing import NewType, List, TypeVar

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
        self.bias = 0.001
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
                self.wts.append(1)

    #present a pattern to net
    #this will set the values of the
    #input nodes
    def present(self: Node, pattern: List[Real]) -> None:
        if self.inputnode:
            try:
                self.val = pattern.pop(0)
            except IndexError:
                raise ValueError('insufficient pattern')
        else:
            #present nodes to children
            for node in self.links:
                node.present(pattern)

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
            self.present(pattern)
            #nullify nodes before evaluating
            #weighted sum
            self.nullify_hidden()
            #actual output from net
            act = self.weighted_sum
            #evaluate dCdAct where
            #C = (act - exp)^2
            dCdAct = 2 * (act - exp) 
            #apply derivative to net
            root.apply_derivative(dCdAct, lrate)

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

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    data = [[1, 1, 1],
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 0]]

    root = Node()
    root.link([Node(), Node()])

    mes = 0
    for pattern in data:
        pattern = list(pattern)
        exp = pattern.pop()
        root.present(pattern)
        root.nullify_hidden()
        act = root.weighted_sum
        err = (act - exp) ** 2
        mes += err
    mes /= len(data)
    print('before:')
    print(f'mes: {mes}')

    mesdata = []
    iterations = 100
    printwhen = iterations // 100

    for i in range(100):
        root.backprop(data, 0.1)
    
        if i % printwhen == 0:
            mes = 0
            for pattern in data:
                pattern = list(pattern)
                exp = pattern.pop()
                root.present(pattern)
                root.nullify_hidden()
                act = root.weighted_sum
                err = (act - exp) ** 2
                mes += err
            mes /= len(data)
            mesdata.append((i, mes))
            print(f'epoch: {i} mes: {mes}')

    x, y = zip(*mesdata)
    plt.plot(x, y)
    plt.title('mes against time')
    plt.xlabel('time /epochs')
    plt.ylabel('mean error squared')
    plt.show()

