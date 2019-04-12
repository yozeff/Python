import string as s

ALPHABET = s.ascii_letters + s.punctuation + s.digits + ' '
#lookup functions for alphabet
to_int = lambda char: ALPHABET.find(char)
to_char = lambda index: ALPHABET[index]

def main():
    message = ''
    keyword = ''
    operation = ''
    continueflag = ''
    #check that the user has not tried to quit
    while continueflag != 'quit':
        operation = input('encipher (e) or decipher (d): ')
        #validate operation input
        while operation != 'e' and operation != 'd':
            operation = input('encipher (e) or decipher (d): ')
        #get message and keyword
        message = input('message: ')
        keyword = input('keyword: ')
        #carry out operation
        if operation == 'e':
            ciphertext = encipher(message, keyword)
            print(f'ciphertext: {ciphertext}')
        else:
            plaintext = decipher(message, keyword)
            print(f'plaintext: {plaintext}')
        #see if the user wants to continue using
        continueflag = input("'quit' to quit: ")
    print('exiting')

#loop the keyword to create keystream
#i.e loop_keyword('abc', 5) = 'abcab'
def loop_keyword(keyword, length):
    result = ''
    for i in range(length):
        result += keyword[i % len(keyword)]
    return result

def encipher(message, keyword):
    keystream = loop_keyword(keyword, len(message))
    ciphertext = ''
    #encipher each character against
    #the corresponding character in
    #the keystream
    for i, char in enumerate(message):
        char = to_int(char) + to_int(keystream[i])
        char %= len(ALPHABET)
        ciphertext += to_char(char)
    return ciphertext

def decipher(message, keyword):
    keystream = loop_keyword(keyword, len(message))
    plaintext = ''
    for i, char in enumerate(message):
        char = to_int(char) - to_int(keystream[i])
        char %= len(ALPHABET)
        plaintext += to_char(char)
    return plaintext

if __name__ == '__main__':
    main()
