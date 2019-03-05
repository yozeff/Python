#Joseph Harrison 2019
#huffman coding
import math as m

class Huffman:

    #static instance constants
    LEFT = '1'
    RIGHT = '0'
    DECODE_BITSTRING_EXCEPTION = 'bitstring must be consistant with constants'
    ROOT_DATA = 'root'
    INT_VERTEX_DATA = '>'

    #construct huffman code based on frequencies
    @staticmethod
    def construct_huffman_code(frequencies):
        #basis tree
        if len(frequencies) == 2:
            root = Node(data=Huffman.ROOT_DATA)
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
        #nullify vertex frequency
        vertex.freq = None
        vertex.data = Huffman.INT_VERTEX_DATA
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
            #if entry doesn't exist create one
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
        return root

class Node(Huffman):

    def __init__(self,data=None,freq=None):
        self.left = self.right = None
        self.data = data
        self.freq = freq

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
                    if freqlist[i][1] == current.freq:
                        current.data = freqlist[i][0]
                        freqlist.pop(i)
                        flag = False
                    i += 1
            else:
                queue.append(current.left)
                queue.append(current.right)

    #utility function to get the depth of a huffman code
    def get_depth(self,level=0):
        if self.left == None:
            return level
        else:
            levels = []
            levels.append(self.left.get_depth(level + 1))
            levels.append(self.right.get_depth(level + 1))
            return max(levels)

    def greedy_append_element(self,data,freq):
        queue = [self]
        while len(queue) > 0:
            #set current vertex pointer
            current = queue.pop(0)
            #if we have found a suitable space
            if current.left == None and current.freq <= freq:
                #construct new basis tree rooted on current
                #with current's data and data as the children's data
                current.left = Node(freq=current.freq,data=current.data)
                current.right = Node(freq=freq,data=data)
                current.freq = None
                current.data = Huffman.INT_VERTEX_DATA
                return True
            #continue traversing the tree
            elif current.left != None:
                queue.append(current.left)
                queue.append(current.right)
        current.left = Node(freq=current.freq,data=current.data)
        current.right = Node(freq=freq,data=data)
        current.freq = None
        current.data = Huffman.INT_VERTEX_DATA

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

    #append element to tree in the optimal location
    def optimal_append_element(self,data,freq):
        #get optimal vertex position
        vertex = self.closest_freq_vertex(freq)[0]
        #create basis tree rooted at vertex
        vertex.left = Node(data=data,freq=freq)
        vertex.right = Node(data=vertex.data,freq=vertex.freq)
        vertex.data = Huffman.INT_VERTEX_DATA
        vertex.freq = None

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
