#Joseph Harrison 2018

def print_array(arr):
    for i in range(len(arr)):
        sub = [str(item) for item in arr[i]]
        print(' '.join(sub))

#matrix spiral traversal

def spiral(matrix):

    print_array(matrix)

    #initialise ordered list of elements
    elements = []

    if len(matrix) > 1:
        #initialise x and y index vars
        x = y = 0
        #initialise index ders
        dx = dy = 0

        #loop for x
        for i in range(4):

            #get the x index der
            if i % 2 != 0:
                dx = 0
            else:
                dx = ((i + 1) % 2) * (1 - i)

            #get the y index der
            dy = ((dx - 1) % 2) * (2 - i)

            #sub loop
            for j in range(len(matrix) - 1):

                elements.append(matrix[y][x])

                #apply derivatives
                x += dx
                y += dy

        if len(matrix) > 2:

            #initialise sub matrix
            sub = []

            for i in range(1,len(matrix) - 1):

                #append centre elements
                sub.append(matrix[i][1:len(matrix) - 1])

            #call algorithm again with sub matrix
            elements += spiral(sub)

    else:

        elements.append(matrix[0][0])

    return elements
