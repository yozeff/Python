#Joseph Harrison 2019
#staircase problem

#N is number of steps
#X is set of step sizes
def possibilities(N,X):

    #if we haven't finished climbing
    if N != 0:

        #counts how many solutions have been found
        solutions = 0

        #for each possible step
        for step in X:

            #if it is legal
            if N - step >= 0:

                #add to number of solutions the number of solutions
                #once step is made
                solutions += possibilities(N - step,X)

        return solutions

    else:
        return 1
