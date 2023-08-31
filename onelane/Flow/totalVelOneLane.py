import matplotlib.pyplot as plt
import math


# lambd - slope dv/dh
# x1 - position of current car
# x2 - position of next car
# vMax - maximum velocity of current car
# dMin - minimum headway of current car
# delta - reaction time
def func(lambd, x1, x2, vMax, dMin, L):
    if (x2-x1 == 0):
        return vMax - vMax*math.exp((-lambd/vMax)*(L-dMin))
    
    return vMax - vMax*math.exp((-lambd/vMax)*(((x2-x1) % L)-dMin));



def main():
    lambd = 1
    dMin = 5
    vMax = 40
    # max val
    maxVal = 0
    maxCar = 0
    # store total velocities
    totalVel = []
    carList = []
    L_List = []
    dStarList = []
    # loop through number of cars
    for L in range(100, 2001, 10):
        for n in range(100):
            if (n == 0):
                carList.append(n)
                totalVel.append(0)
                continue
            hBar = L/n
            if (n == 1):
                result = func(lambd, 0, 0, vMax, dMin, L)
            else:
                result = func(lambd, 0, hBar, vMax, dMin, L)
            if (hBar <= dMin):
                totalVel.append(0)
            else:
                totalVel.append(n*result)
            if (totalVel[len(totalVel)-1] > maxVal):
                maxVal = totalVel[len(totalVel)-1]
                maxCar = n
            carList.append(n)

        L_List.append(L)
        # the most efficient headway for this L
        dStarList.append(L/maxCar)

    #plt.plot(carList, totalVel)
    # plt.set_xlabel("# of cars")
    # plt.set_ylabel("total velocity")
    # plt.annotate(f"# of cars: {maxCar}, velocity: {maxVal}", xy=(maxCar, maxVal), xytext=(maxCar + 2, maxVal + 2), arrowprops=dict(facecolor='black', width=0.2, headlength=1.5, headwidth=2))
    # plt.text(40, maxVal - 10, f"L: {L}", bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

    plt.plot(L_List, dStarList)
    plt.xlabel("L")
    plt.ylabel("d*")
    plt.show()

if __name__ == "__main__":
    main()