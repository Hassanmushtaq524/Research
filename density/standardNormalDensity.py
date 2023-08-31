from sklearn.neighbors import KernelDensity
from scipy.stats import gaussian_kde, norm
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import math

L = 20
yList = []

# lambd - slope dv/dh
# x1 - position of current car
# x2 - position of next car
# vMax - maximum velocity of current car
# dMin - minimum headway of current car
# delta - reaction time
def func(lambd, x1, x2, vMax, dMin, delta):
    if (x2-x1 == 0):
        result =  vMax - vMax*math.exp((-lambd/vMax)*(L-dMin)); 
    else:
        result = vMax - vMax*math.exp((-lambd/vMax)*(((x2-x1) % L)-dMin));
    return result



# x - list of car poistions
# windowSize - size of how large the window of measuring no. of cars is
# n - no. of cars 
def measureDensity(x, n):  
    yList.append([])
    h = 10
    # position
    p = 0
    while (p <= L):
        y = 0
        # for every car at position p, find the y value
        for i in range(n):
            y = y + math.exp((-1*((p-x[i][len(x[i])-1])/h)**2)) + math.exp((-1*((p-(x[i][len(x[i])-1] + L))/h)**2)) + math.exp((-1*((p-(x[i][len(x[i])-1] - L))/h)**2))
        y = y/(n*h)
        yList[len(yList)-1].append(y)
        p += 0.1




# Main
def main():

    t = 0
    lambd = 1
    delta = 0
    
    windowSize = 40

    # traffic jams
    deltaT = 20
    T0 = 0
    dMin = 5
    # no. of cars
    n = 5
    # average headway
    hBar = L/n
    
    # positions of cars
    x = []
    for i in range(n):
        x.append([float(i)*hBar])
    x[0][0] = 0

    # velocities of cars
    v = []
    for i in range(n): 
        v.append([math.nan])

    # vMax of cars
    vMax = []
    for i in range(n):
        vMax.append(40.0)

    # time list
    tList = [0]

    # run for several time steps
    # time step
    j = 0
    trafficJam = False;
    while (t < 300):
        t += 0.01
        for i in range(n):
            x1 = x[i][j]
            x2 = x[(i+1) % n][j]
            if trafficJam == True:
                trafficJam = False
            # introduce traffic jam
            if ((t >= T0 and t <= T0 + deltaT) and i == 0):
                if (not (v[i][j] == 0)):
                    measureDensity(x, n)
                v[i].append(0)
                trafficJam = True;      
            # check if we are less than dMin
            if (trafficJam == False):
                if (x2 == x1):
                    v[i].append(func(lambd, x1, x2, vMax[i], dMin, delta))
                else:
                    if ((x2 - x1) % L <= dMin):
                        v[i].append(0)
                    else:
                        if (v[i][j] == 0):
                            measureDensity(x, n)
                        v[i].append(func(lambd, x1, x2, vMax[i], dMin, delta))         
            # get the next position of the i'th car based on i'th cars velocity
            x[i].append((x1 + 0.01*v[i][len(v[i])-1]) % L)
        j += 1
        tList.append(t);
    
    
    
    # figs, axs = plt.subplots(2, 1)
    

    pList = []
    p = 0
    while p <= L:
        pList.append(p)
        p += 0.1

    plt.plot(pList, yList[1])
    plt.show()
    
    
main()

# no. 1 -> introduce the jam, stop car 0 at time t and make it go again at t + deltaT
# no. 2 -> alter the number of cars and inspect terminal vel. inspec tthe dynamics after the jam is introduced

# less terminal velocity when greater no. of cars (because less headways allowed)
# longer to go back to terminal velocity after traffic jam (Because other cars are crowding and car 1 takes longer to restart)


# keep delta T same in all 3 simulations and gradually reduce