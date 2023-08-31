
import matplotlib.pyplot as plt
# plt.style.use('seaborn-whitegrid')
# import numpy as np
import math

L = 200

# lambd - slope dv/dh
# x1 - position of current car
# x2 - position of next car
# vMax - maximum velocity of current car
# dMin - minimum headway of current car
# delta - reaction time
def func(lambd, x1, x2, vMax, dMin, delta):
    result = vMax - vMax*math.exp((-lambd/vMax)*(((x2-x1) % L)-dMin));
    return result

def transientEnded(v, n):
    for i in range(n):
        for j in range(n):
            if (abs(v[i][len(v[i]) - 1]-v[j][len(v[j]) - 1]) > 1e-3):
                return False            
    return True

# Main
def main():
    lambd = 1
    delta = 0
    
    # storing transientTimes
    transientList = []
    # storing angles
    angleList = []
    # dMin of cars
    dMin = 5
    # no. of cars
    n = 5
    # average headway
    hBar = L/n
    # start the decrease
    T0 = 1
    # vMax of cars
    vMax = []
    for i in range(n):
        vMax.append(40.0)

    for k in range(1,90):
        t = 0
        # traffic jams
        ended = False
        # positions of cars
        x = []
        for i in range(n):
            x.append([float(i)*hBar])
        # velocities of cars
        v = []
        for i in range(n): 
            v.append([math.nan])

        # next velocity
        nextv = 0   
        # next angle
        decreaseAngle = -(math.pi/180)*k
        angleList.append(k)
        # startTime
        startTime = 1
        # endTime
        endTime = 0
        # run for several time steps
        # time step
        j = 0
        trafficJam = False
        stabilityReached = False
        while (t < 1000):
            t += 0.01
            for i in range(n):
                x1 = x[i][j]
                x2 = x[(i+1) % n][j]

                if trafficJam == True:
                    trafficJam = False
                
                # ERROR
                # if (not (k == 0 or k == 90)):
                    # introduce traffic jam
                if (t >= T0 and not ended and i == 0):
                    nextv = 0.01*math.tan(decreaseAngle) + v[i][len(v[i]) - 1]
                    # avoid going negative
                    if (nextv >= 0):
                        # create a gradual decrease
                        v[i].append(nextv)
                        trafficJam = True
                    else:
                        # end the traffic jam
                        ended = True
                        trafficJam = False
                

                # check if we are less than dMin
                if (trafficJam == False):
                    if ((x2 - x1) % L <= dMin):
                        v[i].append(0)
                    else:
                        v[i].append(func(lambd, x1, x2, vMax[i], dMin, delta))   
                # get the next position of the i'th car based on i'th cars velocity
                x[i].append((x1 + 0.01*v[i][len(v[i])-1]) % L)
            
            # check if transient time has ended
            if (ended == True and stabilityReached == False):
                if (transientEnded(v, n)):
                    # end the timer
                    endTime = t
                    stabilityReached = True
                
            j += 1
        transientList.append(endTime-startTime)

    plt.plot(angleList, transientList)
    plt.show()
main()

# none of the cars behind come to a full stop
# car 1 has the highest headway at all times, so it has the highest velocity