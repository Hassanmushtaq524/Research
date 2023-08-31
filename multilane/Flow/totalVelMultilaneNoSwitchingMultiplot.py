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
    n = 160
    hBar = [0, 0]
    # max val
    maxVal = 0
    maxDelta = 0
    # loop through cars
    for n in range(10, 161, 10):
        # store total velocities
        totalVel = []
        diffList = []
        # loop through cars in lane 1
        for c in range(n//2 + 1):
            print(str(n-c) + " -- " + str(c))
            if (c == 0):
                hBar = [L/(n-c), 0]
            else:
                hBar = [L/(n-c), L/c]
                
            total = 0
            if (hBar[0] > dMin and n-c > 0):
                total += (n-c)*func(lambd, 0, hBar[0], vMax, dMin, L)
                # print(func(lambd, 0, hBar[0], vMax, dMin, L))

            if (hBar[1] > dMin and c > 0):
                total += c*func(lambd, 0, hBar[1], vMax, dMin, L)
                # print(func(lambd, 0, hBar[1], vMax, dMin, L))

            # if (total > maxVal):
            #     maxVal = total
            #     maxDelta = n-c-c
            diffList.append((n-c-c) / n)
            totalVel.append(total)

        # print(diffList)
        print("Max: " + str(maxDelta) + " " + str(maxVal))
        plt.plot(diffList, totalVel, label="" + str(n) + " cars")
        plt.legend(loc="upper right")
        # plt.annotate(f"# of cars: {maxCar}, velocity: {maxVal}", xy=(maxCar, maxVal), xytext=(maxCar + 2, maxVal + 2), arrowprops=dict(facecolor='black', width=0.2, headlength=1.5, headwidth=2))
        # plt.text(40, maxVal - 10, f"L: {L}", bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})

        # plt.xlabel("L")
        # plt.ylabel("d*")
    plt.xlabel("delta N")
    plt.ylabel("total velocity")
    plt.show()

if __name__ == "__main__":
    main()