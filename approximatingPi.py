#Joseph Harrison 2019
#approximating pi using monte carlo in unit square
import numpy as np
import timeit
from typing import List
import matplotlib.pyplot as plt

#centre of circle
centre = np.array([0.5, 0.5])

#return true if position vector r is in circle with r = 0.5
#e.g |r| ≤ 0.5
def in_circle(r: List[float]) -> bool:
    #get displacement vector
    s = r - centre
    #make sure in circle
    if np.linalg.norm(s) <= 0.5:
        return True
    else:
        return False
        
def approximate_pi(iterations: int) -> float:
    #number of times inside circle
    successes = 0
    for i in range(iterations):
        #generate point
        r = np.random.random(2)
        if in_circle(r):
            successes += 1
    #compute pi
    pi = 4 * successes / iterations
    return pi

if __name__ == '__main__':
    flag = True
    while flag:
        try:
            iterations = int(input('iterations (int): '))
            flag = False
        except ValueError:
            print('iterations must be integer')
    
    start = timeit.default_timer()
    pi = approximate_pi(iterations)
    end = timeit.default_timer()
    print(f'finished in {end - start}s')
    print(f'approximate value: π = {pi}')
    
    flag = True
    while flag:
        try:
            trials = int(input('trials (int): '))
            maxiterations = int(input('maximum iterations (int): '))
            flag = False
        except ValueError:
            print('trials and maximum iterations must be integer')
    
    #collect data comparing numpy pi constant and approximations
    #against iteration number
    data = []
    for iterations in range(1, maxiterations):
        #evaluate average pi value for 
        #a given number of iterations
        avgpi = 0
        for i in range(trials):
            avgpi += approximate_pi(iterations)
        avgpi /= trials
        
        error = abs(avgpi - np.pi)
        data.append((iterations, error))
        
    x, y = zip(*data)
        
    #regression on data assuming model of form:
    #y = C * x ^ (-k) + c - remove constant for moment
    #ln y = ln(C) - k * ln x
    x2 = np.log(x)
    y2 = np.log(y)
    
    #fit line to data
    m, c = np.polyfit(x2, y2, 1)
    
    C = np.e ** c
    k = -m
    y2 = C * x ** (-k)
        
    print('predicted model:')
    print(f'error = {C:.4f} * iterations ^ {k:.4f}')
        
    plt.plot(x, y2, label=f'error = {C:.4f} * iterations ^ {k:.4f}')
    plt.plot(x, y, 'o', label='data')
    plt.legend()
    plt.title(f'error vs. iterations {trials} trials per iteration')
    plt.xlabel('iterations')
    plt.ylabel('error')
    plt.show()
    
