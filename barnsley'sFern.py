#Joseph Harrison 2019
#barnsely's fern
import random
import matplotlib.pyplot as plt

X = Y = 0
I = 4000
f1X = []
f1Y = []
f2X = []
f2Y = []
f3X = []
f3Y = []
f4X = []
f4Y = []

for i in range(I):
    r = random.randint(1,100)
    if r == 1:
        X = 0
        Y *= 0.16
        f1X.append(X)
        f1Y.append(Y)
    elif r <= 8:
        x = 0.2 * X - 0.26 * Y
        Y = 0.23 * X + 0.22 * Y + 1.6
        X = x
        f2X.append(X)
        f2Y.append(Y)
    elif r <= 15:
        x = -0.15 * X + 0.28 * Y
        Y = 0.26 * X + 0.24 * Y + 0.44
        X = x
        f3X.append(X)
        f3Y.append(Y) 
    else:
        x = 0.85 * X + 0.04 * Y
        Y = -0.04 * X + 0.85 * Y + 1.6
        X = x
        f4X.append(X)
        f4Y.append(Y)

plt.plot(f1X,f1Y,'ro',markersize=1,color='g')
plt.plot(f2X,f2Y,'ro',markersize=1,color='g')
plt.plot(f3X,f3Y,'ro',markersize=1,color='g')
plt.plot(f4X,f4Y,'ro',markersize=1,color='g')
plt.title("Barnsely's Fern")
plt.show()
