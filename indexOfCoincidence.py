#Joseph Harrison 2019
import timeit

#index of coincidence of english
ICEnglish = 0.0686

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

#linear time complexity
def index_of_coincidence(text: str) -> float:
    #record occurences of each character
    occurences = {char : 0 for char in ALPHABET}
    for char in text:
        occurences[char] += 1
    #calculate index of coincidence
    ret = occurences.values()
    ret = map(lambda F: F * (F - 1), ret)
    ret = sum(ret)
    ret /= len(text) * (len(text) - 1)
    return ret

if __name__ == '__main__':
    cont = ''
    while cont != 'q':
        
        #attempt to get handle
        flag = True
        while flag:
            filename = input('filename: ')
            try:
                handle = open(filename, 'r')
                flag = False
            except FileNotFoundError:
                print(f'file {filename} not found')
        
        start = timeit.default_timer()

        #read contents
        text = ''
        for line in handle.readlines():
            line = line.replace('\n', '')
            line = line.lower()
            line = filter(lambda x: x in ALPHABET, line)
            text += ''.join(line)
            
        handle.close()

        ic = index_of_coincidence(text)
        end = timeit.default_timer()
        print(f'index of coincidence: {ic}')
        print(f'IC english: {ICEnglish}')
        print(f'difference: {abs(ICEnglish - ic)}')
        print(f'finished in {end - start}s')
        cont = input('quit (q): ')
