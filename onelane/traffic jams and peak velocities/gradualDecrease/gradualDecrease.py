
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



# Main
def main():
    t = 0
    lambd = 1
    delta = 0

    # traffic jams
    ended = False
    T0 = 20
    # T1 = T0 + deltaT + 10
    # T2 = T1 + deltaT + 10
    k = 2
    decreaseAngle = -(math.pi/180)*k
    dMin = 5
    # no. of cars
    n = 5
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
    nextv = 0
    # run for several time steps
    # time step
    j = 0
    trafficJam = False;
    while (t < 1000):
        t += 0.01
        
        for i in range(n):

            x1 = x[i][j]
            x2 = x[(i+1) % n][j]
            
            if trafficJam == True:
                trafficJam = False

            if (not (k == 0 or k == 90)):
                # introduce traffic jam
                if (t >= T0 and not ended and i == 0):
                    nextv = 0.01*math.tan(decreaseAngle) + v[i][len(v[i]) - 1]
                    # avoid going negative
                    if (nextv >= 0):
                        # create a gradual decrease
                        v[i].append(nextv)
                        trafficJam = True; 
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
        
        
        j += 1
        tList.append(t);
    
    figs, axs = plt.subplots(2, 1)

    # displaying velocity
    for i in range(n):
        carLabel = "Car " + str(i);
        axs[0].plot(tList, v[i], label=carLabel)
        axs[0].set_xlabel("time")
        axs[0].set_ylabel("velocity")
        axs[0].legend(loc="upper left")


    # displaying position
    for i in range(n):
        carLabel = "Car " + str(i);
        axs[1].plot(tList, x[i], label=carLabel)
        axs[1].set_xlabel("time")
        axs[1].set_ylabel("position")
        axs[1].legend(loc="upper left")
    

    plt.show()
    
    
main()

# none of the cars behind come to a full stop
# car 1 has the highest headway at all times, so it has the highest velocity