#Joseph Harrison 2019
#class implementing markov chains
from linearAlgebra import *
import random as r

class Markov:

    def __init__(self,probmat,labels):
        self.states = []
        for i,label in enumerate(labels):
            self.states.append(State
            (label,Vector(*probmat[i])))
        self.state = r.choice(self.states)

    def update_state(self):
        rnum = r.random()
        prob = 0
        for i,elem in enumerate(self.state.probvec[0]):
            prob += elem
            if rnum < prob:
                self.state = self.states[i]
                return

class State:

    def __init__(self,label,probvec):
        self.label = label
        self.probvec = probvec

    def __repr__(self):
        return self.label

