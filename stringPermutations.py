#Joseph Harrison 2018

#string permutations

def perm(string):

    #basis case
    if len(string) == 2:

        perms = [[string[0],string[1]],[string[1],string[0]]]

    else:

        perms = []

        for char in string:

            temp = list(string)
            temp.remove(char)

            #get permutations of lower length string
            #iterate permutations against char
            for permutation in perm(temp):
                perms.append(list(char)+permutation)

    return perms
