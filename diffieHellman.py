#Joseph Harrison 2018
import random, string

#init public constants
g = random.randint(10,100)
n = random.randint(10,100)

#print public constants
print('public constants:\ng:',g,'n:',n)

class Client:

    def __init__(self,name,a):
        self.name = name
        self.a = a
        print(name,'\na:',self.a)

    def subscribe(self,client):
        self.client = client
        print(client.name,'subscribed to',self.name)

    def compute_sub_key(self):
        self.sub = (g ** self.a) % n
        print(self.name,'computed sub key:',self.sub)

    def transmit_sub_key(self):
        self.client.b = self.sub
        print(self.name,'transmitted sub key',self.sub,'to client',self.client.name)

    def compute_full_key(self):
        self.key = (self.b ** self.a) % n
        print(self.name,'computed key',self.key)

    def encrypt(self,m):
        m = list(m)
        for i in range(len(m)):
            m[i] = chr((ord(m[i]) + self.key) % 255)
        return ''.join(m)

    def decrypt(self,E):
        E = list(E)
        for i in range(len(E)):
            E[i] = chr((ord(E[i]) - self.key) % 255)
        return ''.join(E)

    def message(self,m):
        E = self.encrypt(m)
        print(self.name,'sent message:')
        print('plaintext: ',m)
        print('encrypted: ',E)
        self.client.recieve(E)

    def recieve(self,E):
        m = self.decrypt(E)
        print(self.name,'recieved message:')
        print('encrypted: ',E)
        print('decrypted: ',m)

alice = Client('alice',random.randint(1,n))
bob = Client('bob',random.randint(1,n))
alice.subscribe(bob)
bob.subscribe(alice)
alice.compute_sub_key()
bob.compute_sub_key()
alice.transmit_sub_key()
bob.transmit_sub_key()
alice.compute_full_key()
bob.compute_full_key()
m = 'hello there, how are you'
alice.message(m)
