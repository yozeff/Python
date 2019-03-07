#Joseph Harrison 2019
#huffman coding
import math as m
import copy as c

class Huffman:

    #static instance constants
    LEFT = '1'
    RIGHT = '0'
    DECODE_BITSTRING_EXCEPTION = """bitstring must be
           consistant with left
           and right constants...\n
           reset constants with:
           Huffman.LEFT = <newleft>
           Huffman.RIGHT = <newright>"""
    INT_VERTEX_DATA = '>>>'
    INVALID_VERTEX_DATA = """data for huffman code
           cannot be the same as
           internal vertex data: """+INT_VERTEX_DATA+"""\n
           reset constant with:
           Huffman.INT_VERTEX_DATA = <newdata>"""
    ROOT_DATA = 'root'

    #construct huffman code based on frequencies
    @staticmethod
    def construct_huffman_code(frequencies):
        #basis tree
        if len(frequencies) == 2:
            root = Node(data=Huffman.ROOT_DATA,freq=sum(frequencies))
            root.left = Node(freq=frequencies[0])
            root.right = Node(freq=frequencies[1])
            return root
        #minimum frequencies
        min1 = min(frequencies)
        frequencies.remove(min1)
        min2 = min(frequencies)
        frequencies.remove(min2)
        frequencies.append(min1 + min2)
        #produce basis tree with recursion
        root = Huffman.construct_huffman_code(frequencies)
        #search for vertex with freq equal to sum of
        #minimum frequencies in this call
        vertex = root.get_vertex(min1 + min2)
        vertex.data = Huffman.INT_VERTEX_DATA
        vertex.freq = None
        #add children to vertex
        vertex.left = Node(freq=min1)
        vertex.right = Node(freq=min2)
        return root

    #produce frequency list from text
    @staticmethod
    def produce_freq_list(text):
        freqlist = []
        for char in text:
            #check if entry exists
            flag = True
            for i in range(len(freqlist)):
                if freqlist[i][0] == char:
                    #increment frequency
                    freqlist[i][1] += 1
                    flag = False
            #if entry doesn't exist, create one
            if flag:
                freqlist.append([char,1])
        return freqlist

    @staticmethod
    def deserialize(filename):
        root = Node(data='root')
        queue = [root]
        file = open(filename,'r')
        for line in file.readlines():
            current = queue.pop(0)
            #set vertex data and frequency
            line = line.split(':')
            current.data = line[0]
            current.freq = line[1][:-1]
            #if internal vertex
            if current.freq == 'None':
                #create next vertices and append to queue
                current.freq = None
                current.left = Node()
                current.right = Node()
                queue.append(current.left)
                queue.append(current.right)
            else:
                #cast frequency as int if terminating vertex
                current.freq = int(current.freq)
        file.close()
        root.update_freq()
        return root

class Node(Huffman):

    def __init__(self,data=None,freq=None):
        self.left = self.right = None
        self.data = data
        self.freq = freq

    def __repr__(self):
        self.print_tree()
        return 'Node ' + str(self.data) + ' ' + str(self.freq)

    def __add__(self,other):
        #get optimal vertex position
        vertex = self.closest_freq_vertex(other.freq)[0]
        #create basis tree rooted at vertex
        vertex.left = c.copy(other)
        vertex.left.data = Huffman.INT_VERTEX_DATA
        vertex.right = Node(data=vertex.data,freq=vertex.freq)
        #update data and frequency
        vertex.data = Huffman.INT_VERTEX_DATA
        vertex.update_freq()

    def update_freq(self):
        #for internal vertices
        if self.left != None:
            self.freq = self.left.update_freq() + self.right.update_freq()
        return self.freq

    def decode_bitstring(self,bitstring):
        current = self
        elements = []
        for bit in bitstring:
            #traverse tree
            if bit == Huffman.LEFT:
                current = current.left
            elif bit == Huffman.RIGHT:
                current = current.right
            else:
                raise Exception(Huffman.DECODE_BITSTRING_EXCEPTION)
            #if a leaf has been found
            if current.data != Huffman.INT_VERTEX_DATA:
                elements.append(current.data)
                current = self
        return elements

    def encode_element(self,element,bitstring=[]):
        #we have found the data
        if self.data == element:
            return bitstring
        #we have found a terminating vertex
        elif self.left == None:
            return False
        else:
            #traverse left
            newbitstring = self.left.encode_element(element,bitstring + [Huffman.LEFT])
            #check if solution
            if newbitstring: return newbitstring
            #traverse right
            newbitstring = self.right.encode_element(element,bitstring + [Huffman.RIGHT])
            if newbitstring: return newbitstring
            return False

    def print_tree(self,level=0):
        print('     ' * level,[val for val in [self.freq,self.data]
                               if val != None])
        level += 1
        if self.left != None:
            self.left.print_tree(level)
            self.right.print_tree(level)

    #utility method for construct_huffman_code
    def get_vertex(self,freq):
        queue = [self]
        while len(queue) > 0:
            #set current vertex pointer
            current = queue.pop(0)
            #if we have found our frequency
            if current.freq == freq:
                return current
            if current.left != None:
                #append children to queue
                queue.append(current.left)
                queue.append(current.right)
        return False

    #assign values to huffman code vertices
    def assign_data(self,freqlist):
        queue = [self]
        while len(queue) > 0:
            #set current vertex pointer
            current = queue.pop(0)
            #if current is a terminating vertex
            if current.left == None:
                #get data from frequency
                i,flag = 0,True
                while i < len(freqlist) and flag:
                    if freqlist[i][0] == Huffman.INT_VERTEX_DATA:
                        raise Exception(Huffman.INVALID_VERTEX_DATA)
                    elif freqlist[i][1] == current.freq:
                        if current.data == None:
                            current.data = freqlist[i][0]
                            freqlist.pop(i)
                            flag = False
                    i += 1
            else:
                queue.append(current.left)
                queue.append(current.right)

    #utility get vertex that has frequency closest to given frequency
    def closest_freq_vertex(self,freq):
        queue = [self]
        vertex = (self,m.inf)
        while len(queue) > 0:
            #set current pointer
            current = queue.pop(0)
            #if terminating
            if current.left == None:
                difference = abs(freq - current.freq)
                if difference < vertex[1]:
                    vertex = (current,difference)
            else:
                #continue traversing
                queue.append(current.left)
                queue.append(current.right)
        return vertex

    #serialise huffman code to file
    def serialise(self,filename):
        queue = [self]
        file = open(filename,'w')
        while len(queue) > 0:
            current = queue.pop(0)
            #write current vertex data and frequency to file
            file.write(str(current.data)+':'+str(current.freq)+'\n')
            #continue traversing
            if current.left != None:
                queue.append(current.left)
                queue.append(current.right)
        file.close()

