#Joseph Harrison 2019
import numpy as np
import timeit

def poly_mul(p, q):
    #result polynomial
    r = [0] * (len(p) + len(q) - 1)
    for i in range(len(p)):
        for j in range(len(q)):
            r[i + j] += p[i] * q[j]
    return r

def make_poly_list(d):
    #produce a list of deranged polynomials
    #from denominator
    #d = (x + a)(x + b)(x + c) ...
    #r = [(x + b)(x + c) ... , (x + a)(x + c) ...
    r = [[1]] * len(d)
    for i in range(len(d)):
        for j in range(len(d)):
            if i != j:
                #multiply deranged polynomials
                r[i] = poly_mul(r[i], d[j])
    return r

def maximum_order(r):
    #order of highest order
    #polynomial in r
    mo = 0
    for p in r:
        if len(p) - 1 > mo:
            mo = len(p) - 1
    return mo

def make_matrix(r, ns):
    A = [[0 for _ in range(mo + 1)]
            for _ in range(mo + 1)]
    for i in range(len(r)): 
        for j in range(len(r[i])):
            A[len(r[i]) - 1 - j][i] = r[i][j]
    return A

def solve_system(r, n, mo):
    while len(n) < mo + 1:
        n.append(0)
    r = np.mat(r)
    n = np.mat(n)
    n = np.transpose(n)
    n = np.flip(n)
    s = np.linalg.solve(r, n)
    s = np.ndarray.tolist(s)
    return s

if __name__ == '__main__':

    flag = True
    while flag:
        try:
            dsize = int(input('number of denominator factors (int): '))
            if dsize >= 1:
                flag = False
            else:
                print('must be greater than 0')
        except ValueError:
            print('must be integer')

    d = []
    for i in range(dsize):
        flag = True
        while flag:
            print(f'factor {i + 1} in form (ax + b): ')
            try:
                a = int(input('a (int): '))
                b = int(input('b (int): '))
                d.append([b, a])
                flag = False
            except ValueError:
                print('must be integers')

    flag = True
    while flag:
        try:
            nsize = int(input('numerator order (int): '))
            flag = False
        except ValueError:
            print('must be integer')

    n = []
    for i in range(nsize + 1):
        flag = True
        while flag:
            try: 
                a = int(input(f'order {i} term (int): '))
                n.append(a)
                flag = False
            except ValueError:
                print('must be integer')

    start = timeit.default_timer()
    r = make_poly_list(d)
    mo = max(maximum_order(r), nsize)
    r = make_matrix(r, mo)
    try:
        s = solve_system(r, n, mo)
        end = timeit.default_timer()
        print(f'finished in {round(end - start, 3)}s (3 d.p)')
        print('numerators of partial fractions (3 d.p):')
        for i in range(len(s)):
            print(f'{i + 1} : {round(s[i][0], 3)}')
    except:
        print('singular matrix - impossible solve')

