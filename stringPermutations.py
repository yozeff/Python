#Joseph Harrison 2018

#string permutations

def perm(string):

    if len(string) == 2:

        perms = [[string[0],string[1]],[string[1],string[0]]]

    else:

        perms = []

        for char in string:

            temp = list(string)
            temp.remove(char)

            for permutation in perm(temp):
                perms.append(list(char)+permutation)

    return perms

perms = perm('test')
i = 3
while i < len(perms):
    print ' '.join([''.join(item) for item in [perms[i - 3], perms[i - 2], perms[i - 1], perms[i]]])
    i += 1
