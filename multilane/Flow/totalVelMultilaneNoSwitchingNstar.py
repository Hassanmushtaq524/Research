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


    # store number of cars
    nList = []
    # store optimal deltaN
    deltaNStarList = []
    # store optimal flow
    flowStarList = []
    # store flow when deltaN = 0
    flowAt0List = []
    for n in range(4, 161):
        hBar = [0, 0]
        # max val
        maxVal = 0
        maxDelta = 0
        # store delta N
        deltaN = 0
        # loop through number of cars in lane 1
        for c in range(n//2 + 1):
            if (c == 0):
                hBar = [L/(n-c), 0]
            else:
                hBar = [L/(n-c), L/c]
            deltaN = n-c-c
            # total velocity
            total = 0
            # we have to see if cars have enough headway
            if (hBar[0] > dMin and n-c > 0):
                total += (n-c)*func(lambd, 0, hBar[0], vMax, dMin, L)
                # print(func(lambd, 0, hBar[0], vMax, dMin, L))
            if (hBar[1] > dMin and c > 0):
                total += c*func(lambd, 0, hBar[1], vMax, dMin, L)
                # print(func(lambd, 0, hBar[1], vMax, dMin, L))
            # append to lists
            if (total > maxVal):
                maxVal = total
                maxDelta = deltaN
            # get the velocities in initial state
            if (deltaN == 0 or deltaN == 1):
                flowAt0List.append(total)
        print(str(n) + " - " + str(maxDelta))
        # optimal delta N
        deltaNStarList.append(maxDelta)
        # number of cars
        nList.append(n)
        # optimal flow
        flowStarList.append(maxVal)
    # print(diffList)
    figs, axs = plt.subplots(2, 1)
    axs[0].plot(nList, deltaNStarList)
    axs[0].set_xlabel("N")
    axs[0].set_ylabel("deltaN*")
    # plt.annotate(f"# of cars: {maxCar}, velocity: {maxVal}", xy=(maxCar, maxVal), xytext=(maxCar + 2, maxVal + 2), arrowprops=dict(facecolor='black', width=0.2, headlength=1.5, headwidth=2))
    # plt.text(40, maxVal - 10, f"L: {L}", bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
    axs[1].plot(nList, flowStarList, label="deltaN = deltaN*")
    axs[1].plot(nList, flowAt0List, label="deltaN = 0")
    axs[1].legend(loc="upper right")
    axs[1].set_xlabel("N")
    axs[1].set_ylabel("Q")
    
    # plt.xlabel("L")
    # plt.ylabel("d*")
    plt.show()

if __name__ == "__main__":
    main()