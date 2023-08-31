
import matplotlib.pyplot as plt
# plt.style.use('seaborn-whitegrid')
# import numpy as np
import math

L = 100
countList = []

# lambd - slope dv/dh
# x1 - position of current car
# x2 - position of next car
# vMax - maximum velocity of current car
# dMin - minimum headway of current car
# delta - reaction time
def func(lambd, x1, x2, vMax, dMin, delta):
    result = vMax - vMax*math.exp((-lambd/vMax)*(((x2-x1) % L)-dMin));
    return result


# x - list of car poistions
# windowSize - size of how large the window of measuring no. of cars is
# n - no. of cars 
def measureDensity(x, windowSize, n):  
    countList.append([])
    i = 0
    while i <= L:
        count = 0
        for j in range(n):
            low = (i - windowSize/2) % L
            high = (i + windowSize/2) % L
            # near x = 0 or x = L
            if (low >= high):
                if ((x[j][len(x[j]) - 1] <= high and x[j][len(x[j]) - 1] >= 0) or 
                    (x[j][len(x[j]) - 1] >= low and x[j][len(x[j]) - 1] <= L)):
                    count += 1
            else:
                if (x[j][len(x[j]) - 1] <= high and x[j][len(x[j]) - 1] >= low):
                    count += 1
        i += 0.1
        countList[len(countList)-1].append(count)            




# Main
def main():

    t = 0
    lambd = 1
    delta = 0
    
    windowSize = 20

    # traffic jams
    deltaT = 5
    T0 = 20
    dMin = 3
    # no. of cars
    n = 10
    # average headway
    hBar = L/n
    
    # positions of cars
    x = []
    for i in range(n):
        x.append([float(i)*hBar])
    

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
                    measureDensity(x, windowSize, n)
                v[i].append(0)
                trafficJam = True;      
            # check if we are less than dMin
            if (trafficJam == False):
                if ((x2 - x1) % L <= dMin):
                    v[i].append(0)
                else:
                    if (v[i][j] == 0):
                        measureDensity(x, windowSize, n)
                    v[i].append(func(lambd, x1, x2, vMax[i], dMin, delta))         
            # get the next position of the i'th car based on i'th cars velocity
            x[i].append((x1 + 0.01*v[i][len(v[i])-1]) % L)
        j += 1
        tList.append(t);
    
    
    
    figs, axs = plt.subplots(2, 1)

    
    xlist = []
    i = 0
    while i <= L:
        xlist.append(i)
        i += 0.1

    # displaying at T0
    for i in range(n):
        axs[0].plot(xlist, countList[0])
        axs[0].set_xlabel("x")
        axs[0].set_ylabel("p(x)")


    # displaying at T0 + deltaT
    for i in range(n):
        axs[1].plot(xlist, countList[1])
        axs[1].set_xlabel("x")
        axs[1].set_ylabel("p(x)")
    

    plt.show()
    
    
main()

# no. 1 -> introduce the jam, stop car 0 at time t and make it go again at t + deltaT
# no. 2 -> alter the number of cars and inspect terminal vel. inspec tthe dynamics after the jam is introduced

# less terminal velocity when greater no. of cars (because less headways allowed)
# longer to go back to terminal velocity after traffic jam (Because other cars are crowding and car 1 takes longer to restart)


# keep delta T same in all 3 simulations and gradually reduce