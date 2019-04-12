import string as s
import numpy as np

ALPHABET = s.ascii_letters + s.punctuation + s.digits + ' '
to_int = lambda char: ALPHABET.find(char)
to_char = lambda index: ALPHABET[index]

def main():
    continueflag = ''
    while continueflag != 'quit':
        #get and validate operation from user
        operation = input('encipher (e) or decipher (d): ')
        while operation != 'e' and operation != 'd':
            operation = input('encipher (e) or decipher (d): ')
        message = input('message: ')
        #get the a and b keys
        flag = False
        while not flag:
            try:
                a = int(input('a: '))
                b = int(input('b: '))
                #make sure a and m (the length
                #of the alphabet) are coprime
                if np.gcd(a, len(ALPHABET)) == 1:
                    flag = True
                else:
                    print(f'length of alphabet, m, is {len(ALPHABET)}')
                    print('a and m must be coprime')
            #make sure a and b are integers
            except TypeError:
                pass
        if operation == 'e':
            ciphertext = encipher(message, a, b)
            print(f'ciphertext: {ciphertext}')
        else:
            plaintext = decipher(message, a, b)
            print(f'plaintext: {plaintext}')
        #see if the user wants to quit
        continueflag = input("'quit' to quit: ")
    print('exiting')

#extended euclidean algorithm for gcd
def ext_gcd(a, m):
    lastrem, rem = abs(a), abs(m)
    x, lastx, y, lasty = 0, 1, 1, 0
    while rem != 0:
        lastrem, (quot, rem) = rem, divmod(lastrem, rem)
        x, lastx = lastx - quot * x, x
        y, lasty = lasty - quot * y, y
    return lastrem, lastx * (-1 if a < 0 else 1), lasty * (-1 if m < 0 else 1)

#computes the modular inverse of a mod m
def mod_inv(a, m):
    lastrem, x, y = ext_gcd(a, m)
    return x % m

def encipher(message, a, b):
    ciphertext = ''
    #encipher each character
    for char in message:
        char = to_int(char)
        #affine transformation
        char = a * char + b
        char %= len(ALPHABET)
        #concatenate
        ciphertext += to_char(char)
    return ciphertext

def decipher(message, a, b):
    plaintext = ''
    for char in message:
        char = to_int(char)
        #modular inverse of a
        char = (char - b) * mod_inv(a, len(ALPHABET))
        char %= len(ALPHABET)
        plaintext += to_char(char)
    return plaintext

if __name__ == '__main__':
    main()
