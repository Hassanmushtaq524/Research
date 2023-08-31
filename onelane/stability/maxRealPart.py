from sympy import *
import numpy as np
from numpy.linalg import eig
import matplotlib.pyplot as plt

def main():
    L = 100
    nList = []
    maxPartList = []
    for n in range(3, 91):
        nList.append(n)  
        maxReal = -9999
        hBar = L/n
        l, v, d = symbols("l v d", constant=True)
        l = 1 
        v = 40
        d = 5

        y = symbols("y0:" + str(n), real = True)

        # our list of x' expressions will be stored in a list
        f = []
        for i in range(n):
            if (i == n-1):
                expr = v-v*exp(-l*(L-y[i]-d)/v)
            else: 
                if (i == 0):
                    expr = v-v*exp(-l*(y[1]-d)/v)
                else:
                    expr = v-v*exp(-l*(y[i+1]-y[i]-d)/v)
            f.append(expr)

        # y' expressions
        yPrime = [0 for i in range(n)]
        for i in range(1, n):
            yPrime[i] = f[i] - f[0]

        # values
        vals = {}
        for i in range(n):
            vals[y[i]] = i*hBar

        # form the jacobian
        Jacobian = []
        for i in range(1, n):
            temp = []
            for j in range(1, n):
                temp.append(diff(yPrime[i], y[j]).evalf(subs=vals))
            Jacobian.append(temp)

        Jacobian = np.array(Jacobian, dtype=float)  
        w, v = eig(Jacobian)
        # finding the maximum real part
        for i in range(len(w)):
            if (w[0].real > maxReal):
                maxReal = w[0].real
        maxPartList.append(maxReal)

    plt.plot(nList, maxPartList)
    plt.xlabel("# of cars")
    plt.ylabel("Maximum real part of eigenvalues")
    plt.show()
        
        



    
   
    

main()