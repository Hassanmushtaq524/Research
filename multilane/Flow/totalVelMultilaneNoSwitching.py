import matplotlib.pyplot as plt
import math


# lambd - slope dv/dh
# x1 - position of current car
# x2 - position of next car
# vMax - maximum velocity of current car
# dMin - minimum headway of current car
# delta - reaction time
def func(lambd, x1, x2, vMax, dMin, L):
    if ((x2-x1) % L == 0):
        return vMax - vMax*math.exp((-lambd/vMax)*(L-dMin))
    
    return vMax - vMax*math.exp((-lambd/vMax)*(((x2-x1) % L)-dMin));



def main():
    lambd = 1
    dMin = 5
    vMax = 40
    L = 400
    n = 5
    hBar = [0, 0]
    # max val
    maxVal = 0
    maxDelta = 0
    # store delta N
    deltaN = 0;
    # store total velocities
    totalVel = []
    totalVel_0 = []
    totalVel_1 = []
    diffList = []
    # loop through number of cars in lane 1
    for c in range(n//2 + 1):
        if (c == 0):
            hBar = [L/(n-c), 0]
        else:
            hBar = [L/(n-c), L/c]
        deltaN = n-c-c
        # store the total in each lane
        total0 = 0
        total1 = 0
        # we have to see if cars have enough headway
        if (hBar[0] > dMin and n-c > 0):
            total0 = (n-c)*func(lambd, 0, hBar[0], vMax, dMin, L)
            # print(func(lambd, 0, hBar[0], vMax, dMin, L))
        if (hBar[1] > dMin and c > 0):
            total1 = c*func(lambd, 0, hBar[1], vMax, dMin, L)
            # print(func(lambd, 0, hBar[1], vMax, dMin, L))
        # append to lists
        diffList.append(deltaN)
        totalVel_0.append(total0);
        totalVel_1.append(total1);
        totalVel.append(total1+total0)

    # print(diffList)
    print(totalVel)
    print("Max: " + str(maxDelta) + " " + str(maxVal))
    plt.plot(diffList, totalVel, label="Both lanes")
    plt.plot(diffList, totalVel_0, label="Lane 0")
    plt.plot(diffList, totalVel_1, label="Lane 1")
    plt.legend(loc="upper right")
    plt.xlabel("delta N")
    plt.ylabel("total velocity")
    # plt.annotate(f"# of cars: {maxCar}, velocity: {maxVal}", xy=(maxCar, maxVal), xytext=(maxCar + 2, maxVal + 2), arrowprops=dict(facecolor='black', width=0.2, headlength=1.5, headwidth=2))
    # plt.text(40, maxVal - 10, f"L: {L}", bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

    # plt.xlabel("L")
    # plt.ylabel("d*")
    plt.show()

if __name__ == "__main__":
    main()