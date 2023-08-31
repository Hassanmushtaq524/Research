
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
    deltaT = 3
    T0 = 0
    T1 = T0 + deltaT + 10
    T2 = T1 + deltaT + 10
    T3 = T2 + deltaT + 10
    T4 = T3 + deltaT + 10
    T5 = T4 + deltaT + 10
    T6 = T5 + deltaT + 10
    T7 = T6 + deltaT + 10
    T8 = T7 + deltaT + 10
    
    dMin = 5
    # no. of cars
    n = 10
    # average headway
    hBar = L/n
    
    # positions of cars
    x = []
    for i in range(n):
        x.append([i*10])
    

    # velocities of cars
    v = []
    for i in range(n): 
        v.append([math.nan])

    # vMax of cars
    vMax = []
    for i in range(n):
        vMax.append(40)

    # time list
    tList = [0]

    # run for several time steps
    # time step
    j = 0
    trafficJam = False;
    while (t < 100):
        t += (0.005/2)
        
        for i in range(n):

            x1 = x[i][j]
            x2 = x[(i+1) % n][j]
            
            if trafficJam == True:
                trafficJam = False

            # # introduce traffic jam
            # if ((t >= T0 and t <= T0 + deltaT) and i == 0):
            #     v[i].append(0)
            #     trafficJam = True;
            
            # if ((t >= T1 and t <= T1 + deltaT) and i == 0):
            #     v[i].append(0)
            #     trafficJam = True;
            
            # if ((t >= T2 and t <= T2 + deltaT) and i == 0):
            #     v[i].append(0)
            #     trafficJam = True;

            # if ((t >= T3 and t <= T3 + deltaT) and i == 0):
            #     v[i].append(0)
            #     trafficJam = True;
            
            # if ((t >= T4 and t <= T4 + deltaT) and i == 0):
            #     v[i].append(0)
            #     trafficJam = True;
            
            # if ((t >= T5 and t <= T5 + deltaT) and i == 0):
            #     v[i].append(0)
            #     trafficJam = True;
            
            # if ((t >= T6 and t <= T6 + deltaT) and i == 0):
            #     v[i].append(0)
            #     trafficJam = True;

            # if ((t >= T7 and t <= T7 + deltaT) and i == 0):
            #     v[i].append(0)
            #     trafficJam = True;
            
            # if ((t >= T8 and t <= T8 + deltaT) and i == 0):
            #     v[i].append(0)
            #     trafficJam = True;
            
            # check if we are less than dMin
            if (trafficJam == False):
                if ((x2 - x1) % L <= dMin):
                    v[i].append(0)
                else:
                    v[i].append(func(lambd, x1, x2, vMax[i], dMin, delta))
                
            # get the next position of the i'th car based on i'th cars velocity
            x[i].append((x1 + (0.005/2)*v[i][len(v[i])-1]) % L)
        
        
        j += 1
        tList.append(t);
    
    # figs, axs = plt.subplots(2, 1)

    # displaying velocity
    for i in range(n):
        carLabel = "Car " + str(i);
        plt.plot(tList, v[i], label=carLabel)
        plt.xlabel("Time")
        plt.ylabel("Velocity")
        plt.legend(loc="upper right")


    # # displaying position
    # for i in range(n):
    #     carLabel = "Car " + str(i);
    #     axs[1].plot(tList, x[i], label=carLabel)
    #     axs[1].set_xlabel("time")
    #     axs[1].set_ylabel("position")
    #     axs[1].legend(loc="upper left")
    

    plt.show()
    
    print(v[0][1])
    print(v[1][1])
main()

# no. 1 -> introduce the jam, stop car 0 at time t and make it go again at t + deltaT
# no. 2 -> alter the number of cars and inspect terminal vel. inspec tthe dynamics after the jam is introduced

# less terminal velocity when greater no. of cars (because less headways allowed)
# longer to go back to terminal velocity after traffic jam (Because other cars are crowding and car 1 takes longer to restart)


# keep delta T same in all 3 simulations and gradually reduce