
import matplotlib.pyplot as plt
# plt.style.use('seaborn-whitegrid')
# import numpy as np
import math

L = 200

# lambd - slope dv/dh at v = 0
# x1 - position of current car
# x2 - position of next car
# vMax - maximum velocity of current car
# dMin - minimum headway of current car
# delta - reaction time
def func(lambd, x1, x2, vMax, dMin, delta):
    result = vMax - vMax*math.exp((-lambd/vMax)*(((x2-x1) % L)-dMin))
    return result


# Main
def main():

    lambd = 1
    delta = 0

    # traffic jams
    deltaT = 0
    deltaTList = []
    avgPeakVel = []
    T0 = 10
    dMin = 5
    # no. of cars
    n = 5
    # average headway
    hBar = L/n  

    # vMax of cars
    vMax = []
    for i in range(n):
        vMax.append(40.0)

    


    for k in range(30):

        deltaT = k
        deltaTList.append(deltaT)

        T1 = T0 + deltaT + 10
        T2 = T1 + deltaT + 10
        T3 = T2 + deltaT + 10
        T4 = T3 + deltaT + 10
        T5 = T4 + deltaT + 10

        tList = [0]
        # reset positions of cars
        x = []
        for i in range(n):
            x.append([float(i)*hBar])

        # reset velocities of cars
        v = []
        for i in range(n): 
            v.append([math.nan])
        # print(deltaTList)
        t = 0
        sum = 0
        
        trafficJam = False
        j = 0

        # run for several time steps
        while (t < 300):
            t += 0.01
            for i in range(n):

                x1 = x[i][j]
                x2 = x[(i+1) % n][j]
                
                if trafficJam == True:
                    trafficJam = False

                # introduce traffic jam
                if (not (deltaT == 0)):

                    if (((t >= T0 and t <= T0 + deltaT) or 
                        (t >= T1 and t <= T1 + deltaT) or
                        (t >= T2 and t <= T2 + deltaT) or 
                        (t >= T3 and t <= T3 + deltaT) or
                        (t >= T4 and t <= T4 + deltaT) or
                        (t >= T5 and t <= T5 + deltaT)) and i == 0):
                        v[i].append(0)
                        trafficJam = True
                    
                
                # check if we are less than dMin
                if (trafficJam == False):
                    if ((x2 - x1) % L <= dMin):
                        v[i].append(0)
                    else:
                        v[i].append(func(lambd, x1, x2, vMax[i], dMin, delta))

                        # if the previous velocity was 0 of car 0, then now we are in peak
                        if (v[0][j] == 0 and i == 1):
                            sum += v[i][len(v[i]) - 1]
                        
                    
                # get the next position of the i'th car based on i'th cars velocity
                x[i].append((x1 + 0.01*v[i][len(v[i])-1]) % L)

            j += 1
            tList.append(t)
        
        if (deltaT == 0):
            avgPeakVel.append(v[1][1])
        else:
            avgPeakVel.append(sum/5)

   



    # displaying avgPeakVelocities
    print(deltaTList)
    print(avgPeakVel)
    plt.plot(deltaTList, avgPeakVel)
    

    plt.show()
    
    
main()

# no. 1 -> introduce the jam, stop car 0 at time t and make it go again at t + deltaT
# no. 2 -> alter the number of cars and inspect terminal vel. inspec tthe dynamics after the jam is introduced

# less terminal velocity when greater no. of cars (because less headways allowed)
# longer to go back to terminal velocity after traffic jam (Because other cars are crowding and car 1 takes longer to restart)


# keep delta T same in all 3 simulations and gradually reduce