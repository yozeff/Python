#Joseph Harrison 2019
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

#relation of form z(t + 1) = z(t) ^ n + c
#|z| doesn't escape u over T iterations
def rec_relation(n: float, c: complex, u: float, T: int):
    z = c
    for t in range(T):
        #update z
        z = z ** n + c
        #check u threshold
        if abs(z) > u:
            return False
    return True

#init function for matplot animation
def init():
    line.set_data([], [])
    return line,

#function for animation
def animate(a: float, b: float, u: float, 
            T: int, r: float, dr: float):
    n = complex(a, b)
    try:
        #create set of tuples in set
        recset = [(x, y) for x in np.arange(-r, r, dr)
                  for y in np.arange(-r, r, dr) if rec_relation(n, complex(x, y), u, T)]
    
        if len(recset) != 0:
            #set data for animate function
            x, y = zip(*recset)
            line.set_data(x, y)
    except (OverflowError, ZeroDivisionError):
        pass
    
    return line,

if __name__ == '__main__':
    print('''complex recurrence relations of form:
z(t + 1) = z(t) ^ n + c     0 < t < T
c is a member of set if |z| does not exceed u
members are automatically discovered within range (-r, r) at multiples of dr''')

    cont = ''
    while cont != 'q':

        #get parameters
        flag = True
        while flag:
            try:
                a = float(input('n real (real): '))
                b = float(input('n imag (real): '))
                n = complex(a, b)
                u = float(input('u (real): '))
                T = int(input('T (integer): '))
                r = float(input('r (real): '))
                dr = float(input('dr (real): '))
                flag = False
            except ValueError:
                print('invalid input')

        #produce set of complex numbers
        try:
            recset = [(a, b) for a in np.arange(-r, r, dr)
                      for b in np.arange(-r, r, dr) if rec_relation(n, complex(a, b), u, T)]
        except OverflowError:
            print('overflow error occured - try using smaller parameters')
            recset = []

        print(f'found {len(recset)} members')

        if len(recset) != 0:
            #plot user defined set
            a, b = zip(*recset)
            plt.plot(a, b, 'o', markersize=0.5)
            plt.xlabel('re')
            plt.ylabel('im')
            plt.show()

        animprompt = input('animation (y/n): ')

        #animate plotting of subsequent sets whilst
        #iterating the imaginary component of n
        if animprompt == 'y':
            fig = plt.figure()
            ax = plt.axes(xlim=(-r, r), ylim=(-r, r), xlabel='re', ylabel='im')
            line, = ax.plot([], [], 'o', markersize=0.5)

            flag = True
            while flag:
                try:
                    p = float(input('p max (real): '))
                    dp = float(input('dp (real): '))
                    flag = False
                except ValueError:
                    print('invalid input')

            print(f'animating set with n = q + {n.imag}i, -{p} < q < {p}')

            #add reverse of animation to frames
            frames = [i for i in np.arange(-p, p, dp)] + [i for i in np.arange(p, -p, -dp)]

            #animation varies the imaginary part of the exponent
            anim = animation.FuncAnimation(fig, animate, init_func=init,
                                           frames=frames,
                                           interval=2,
                                           blit=True,
                                           #pass thru additional user defined params
                                           fargs=(n.imag, u, T, r, dr))

            plt.show()

        cont = input('quit (q): ')

