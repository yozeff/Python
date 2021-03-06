#Joseph Harrison 2019
#brainfuck interpreter
import os

#increment data pointer
def inc_ptr():
    global dataptr
    dataptr = (dataptr + 1) % cellno

#decrement data pointer
def dec_ptr():
    global dataptr
    dataptr = (dataptr - 1) % cellno

#increment value at data pointer
def inc_val():
    global cells
    cells[dataptr] = (cells[dataptr] + 1) % 255

#decrement value at data pointer
def dec_val():
    global cells
    cells[dataptr] = (cells[dataptr] - 1) % 255

#output value at data pointer
def out_val():
    print(chr(cells[dataptr]))

#set value at data pointer to input
def inp_val():
    global cells
    try:
        cells[dataptr] = ord(input('$$  '))
        return
    except TypeError:
        print('takes an ascii character')

#position of next ] command
#that is a pair
def get_next_brac():
    global line
    global insptr
    i = insptr
    #j counts instances of brackets
    #the instances are resolved by
    #decreasing j
    j = 0
    while i < len(line):
        #if we have found a ]
        if line[i] == ']':
            j -= 1
            if j == 0:
                return i
        elif line[i] == '[':
            j += 1
        i += 1
    print('no succeeding ]')

#position of last [ command
#that is a pair
def get_last_brac():
    global line
    global insptr
    i = insptr
    j = 0
    while i > -1:
        #if we have found a [
        if line[i] == '[':
            j -= 1
            if j == 0:
                return i
        elif line[i] == ']':
            j += 1
        i -= 1
    print('no preceeding [')

#print the data pointer
def print_dataptr():
    print(dataptr)

#print the current contents
#the cells
def print_cells():
    print(' '.join([str(val)
         for val in cells]))

#print a manual for brainfuck interpreter
def print_man():
    print('\n                       brainfuck interpreter manual\n')
    descdict = {'>':f'increment the data pointer by 1 (mod {cellno})',
                '<':f'decrement the data pointer by 1 (mod {cellno})',
                '+':f"""increment the value in the cell pointed to by
             the data pointer by 1 (mod 255)""",
                '-':f"""decrement the value in the cell pointed to by 
             the data pointer by 1 (mod 255)""",
                '.':"""output the ascii representation of the value
             in the cell pointed to by the data pointer""",
                ',':"""takes an ascii character as input and stores
             it in the cell pointed to by the data pointer""",
                '[':"""if the value in the cell pointed to by the
             data pointer is zero, jump to the command
             after the next ']' character""",
                ']':"""if the value in the cell pointed to by the
             data pointer is non-zero, jump to the
             command after the previous '[' character"""}
    print('brainfuck commands:\n')
    for command in descdict:
        print(f'    {command}        {descdict[command]}\n')
    descdict = {'q':'quit interpreter',
                'm':'manual... but it seems you already know that',
                'c':'print current contents of the memory cells',
                'd':'print the current value of the data pointer',
                'r':'reset interpreter state',
                'o':'open a brainfuck file and run it immediately',
                'n':"""open the brainfuck editor and create a new file
             the file is closed and saved with an 'n'"""}
    print('interpreter commands:\n')
    for command in descdict:
        print(f'    {command}        {descdict[command]}\n')

#reset cells and data pointer
def reset():
    global cells
    global dataptr
    cells = [0 for i in range(cellno)]
    dataptr = 0

#open a brainfuck file
def open_bf_file():
    global line
    filename = input('$$$ ')
    try:
        file = open('bfPrograms/' + filename + '.txt','r')
        #read code from file
        filecode = ''
        for fileline in file.readlines():
            filecode += fileline.replace('\n','')
        #replace o in line with
        #code in file
        file.close()
        line = line.replace('o','o' + filecode)
    except FileNotFoundError:
        print('file not found')

#open brainfuck editor
def open_editor():
    filename = input('$$$ ')
    file = open('bfPrograms/' + filename + '.txt','w')
    fileline = ''
    filecode = ''
    while fileline != 'n':
        fileline = input('~   ')
        #remove newlines and whitespace
        fileline = fileline.replace('\n','')
        fileline = fileline.replace(' ','')
        filecode += fileline
    file.write(filecode[:-1])
    file.close()

#memory cells
cellno = 16
cells = [0 for i in range(cellno)]
#points to a memory cell
dataptr = 0

#command dict keys can be paired
#with corresponding procedures
commdict = {'>':inc_ptr,
            '<':dec_ptr,
            '+':inc_val,
            '-':dec_val,
            '.':out_val,
            ',':inp_val,
            'm':print_man,
            'c':print_cells,
            'd':print_dataptr,
            'r':reset,
            'o':open_bf_file,
            'n':open_editor}

print("brainfuck interpreter Joseph Harrison 2019"
      "\n'm' for manual 'q' to quit")

#create 'bfPrograms' folder if it doesn't
#already exist
try:
    if not os.path.exists('bfPrograms'):
        print("creating 'bfPrograms' directory")
        os.makedirs('bfPrograms')
except OSError:
    print("error creating 'bfPrograms' directory")

#line that is being processed
line = ''
#'q' to exit
while line != 'q':

    #get input line
    line = input('$   ')
            
    #flag allows a line to stop
    #being processed if an error
    #occurs
    errflag = False

    #points to the
    #next instruction
    insptr = 0

    #haven't reached the end of line
    #and an error has not occured
    while insptr != len(line) and not errflag:
        
        #for [ routine
        if line[insptr] == '[':
            #if value at data pointer
            #is zero
            if cells[dataptr] == 0:
                #set the instruction pointer
                #to the instruction after the
                #next ]
                insptr = get_next_brac() + 1
            #proceed to the next instruction
            else:
                insptr += 1

        #for ] routine
        elif line[insptr] == ']':
            #if value at data pointer
            #is non zero
            if cells[dataptr] != 0:
                #set instruction pointer
                #to the instruction after the
                #next [
                insptr = get_last_brac() + 1
            #proceed to the next instruction
            else:
                insptr += 1

        #if we are processing a
        #regular command
        else:

            try:
                #call procedure for
                #command
                commdict[line[insptr]]()
                insptr += 1
            #if the command doesn't exist
            except KeyError:
                print("command doesn't exist")
                errflag = True

print('thank you for choosing brainfuck')
