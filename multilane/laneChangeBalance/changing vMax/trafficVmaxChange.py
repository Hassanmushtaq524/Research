import matplotlib.pyplot as plt
import math
import random
class Car:

    def __init__(self, ID, initialPos, lane, vMax, tolerance) -> None:
        # id of the car
        self.ID = ID
        # store velocities at every time step
        self.velArr = [math.nan]
        # store positions at every time step
        self.posArr = [initialPos]
        # stores the lanes the car is at 
        self.laneArr = [lane]
        # minimum headway
        self.dMin = 5
        # maximum velocity of car
        self.vMax = vMax
        # lane of car
        self.lane = lane
        # the driver tolerance
        self.tolerance = tolerance
        # previous time step position
        self.curPosition = self.posArr[0]
        # count the impatience
        self.impatience = 0
        
    def getPosition(self, timeStep):
        return self.posArr[timeStep]
    
    def getVelocity(self, timeStep):
        return self.velArr[timeStep]

    def appendVelocity(self, v):
        self.velArr.append(v)

    def appendPosition(self, x):
        self.posArr.append(x)
        self.curPosition = self.posArr[len(self.posArr) - 1]

    def patienceExceeded(self):
        if (self.impatience > self.tolerance):
            self.impatience = 0
            return True
        else:
            return False

# lambd - slope dv/dh
# x1 - position of current car
# x2 - position of next car
# vMax - maximum velocity of current car
# dMin - minimum headway of current car
# delta - reaction time
def func(lambd, x1, x2, vMax, dMin, delta, L):
    if (x2-x1 == 0):
        result =  vMax - vMax*math.exp((-lambd/vMax)*(L-dMin)); 
    else:
        result = vMax - vMax*math.exp((-lambd/vMax)*(((x2-x1) % L)-dMin));
    return result

# mat: matrix of cars
# curCar: the object of the current car
# curHeadway: the headway right now for current car
# l: total number of lanes
# L: total length of road
# n: total number of cars
# timeStep: current time step 
def switch(mat, curCar, curHeadway, l, L, n, timeStep):
    if curHeadway == 0:
        return (False, None, -1)
    # headway in the other lane
    otherHeadway = 0
    curLane = []
    lanesToCheck = [curCar.lane + 1, curCar.lane - 1]
    # check the possible lanes we can move to
    for ln in lanesToCheck:
        if (ln >= 0 and ln <= l - 1):
            # make a deep copy
            for i in range(len(mat[ln])):
                curLane.append(mat[ln][i])
            # place the car and check for new possible headway
            curLane[len(curLane)-1] = curCar
            curLane.sort(key=lambda x : L if x is None else x.getPosition(timeStep-1))
            # find the next car
            for i, c in enumerate(curLane):
                if (c is not None):
                    if (c.ID == curCar.ID):
                        nextCar = curLane[(i + 1) % n]
                        if (nextCar == None):
                            nextCar = curLane[0]
            # get the other headway 
            if (nextCar.ID == curCar.ID):
                otherHeadway = L
            else:
                otherHeadway = (nextCar.getPosition(timeStep - 1) - curCar.getPosition(timeStep - 1)) % L
    
            if (otherHeadway > curHeadway):
                # add to the impatience counter
                curCar.impatience += 1
                # if we have exceeded the tolerance for the current car
                if (curCar.patienceExceeded()):
                    return (True, nextCar, ln)
                else:
                    break
            else:
                # this will reduce the counter twice if both lanes are worse
                if (curCar.impatience > 0):
                    curCar.impatience -= 1
    return (False, None, -1)
   
def main():
    # number of cars
    n = 20
    # lanes
    l = 2
    # length of the road
    L = 400
    plotNum = 0
    figs, axs = plt.subplots(3, 1)
    for num in range(0, n//2 + 1, 5):
        # total deltaN for averaging
        averageDeltaNList = [0 for i in range(15001)]
        averageDeltaNList[0] = n-num
        # 10 simulations for this
        for k in range(30):
            # represents the lanes
            mat = [[None]*n for _ in range(l)]
            # stores hBar for each lane
            cars = [n-num, num]
            hBar = [0]*l
            for i in range(len(cars)):
                if (cars[i]):
                    hBar[i] = L/cars[i]
            # place the cars
            ID = 0
            for i in range(l):
                for j in range(cars[i]):
                    mat[i][j] = Car(ID, j*hBar[i], i, random.gauss(50, 10), 500)
                    ID += 1

            # list of times
            tList = [0]
            # the time
            t = 0
            # what time step we are at
            timeStep = 0
            # when to end
            endTime = 150
            deltaNList = [n-num];
            # start the time
            while t <= endTime:
                t += 0.01
                timeStep += 1
                seen = []
                switchingCars = []
                # go through each lane
                i = 0
                while i < l:
                    j = 0
                    # go through every car
                    while j < n:
                        # current car's index
                        curCar = mat[i][j]
                        # if no more cars in this lane, that means no cars anywhere after
                        if (curCar == None):
                            break
                        # if we have already seen this car at the current timeStep, we go to the next car
                        if (curCar.ID in seen):
                            j += 1
                            continue                
                        # mark the curCar as seen
                        seen.append(curCar.ID)
                        # next car's index
                        nextCar = mat[i][(j + 1) % n]
                        if (nextCar == None):
                            nextCar = mat[i][0]
                        # current car's position
                        x1 = curCar.getPosition(timeStep - 1)
                        # next car's position
                        x2 = nextCar.getPosition(timeStep - 1)
                        # switch the lane of the curCar if better headway   
                        (shouldSwitch, nextCar, ln) = switch(mat, curCar, (x2-x1) % L, l, L, n, timeStep)
                        # if we should switch, then make the changes
                        if (shouldSwitch):
                            # mark the car to be switched
                            switchingCars.append((curCar, ln))
                            # next car's position again but we will make the actual switch later so the cars
                            # in the other lane do not see this car at current time step, but will see it at the next time step
                            x2 = nextCar.getPosition(timeStep - 1)
                        else:
                            # next car's index
                            nextCar = mat[i][(j + 1) % n]
                            if (nextCar == None):
                                nextCar = mat[i][0]
                        # we have to see if the next car is the same car
                        if (nextCar == curCar):
                            curCar.appendVelocity(func(1, x1, x2, curCar.vMax, curCar.dMin, 0, L))
                        else:     
                            if ((x2 - x1) % L <= curCar.dMin):
                                curCar.appendVelocity(0)
                            else:
                                curCar.appendVelocity(func(1, x1, x2, curCar.vMax, curCar.dMin, 0, L))
                        # get next position
                        curCar.appendPosition((curCar.getPosition(timeStep-1) + 0.01*curCar.getVelocity(timeStep)) % L) 
                        # inc to next car
                        j += 1     
                    i += 1
                # see if some cars need to be switched
                if (len(switchingCars) > 0):
                    for i in range(len(switchingCars)):
                        curCar, ln = switchingCars[i]
                        # print(str(curCar.ID) + " switched: " + str(curCar.lane) + " to " + str(ln))
                        # switch the car
                        mat[ln][len(mat[ln]) - 1] = curCar
                        # remove car from previous lane
                        for a, c in enumerate(mat[curCar.lane]):
                            if (c is not None):
                                if (c.ID == curCar.ID):
                                    mat[curCar.lane][a] = None
                        # sort both lanes
                        mat[ln].sort(key=lambda x : L if x is None else x.getPosition(timeStep-1))
                        mat[curCar.lane].sort(key=lambda x : L if x is None else x.getPosition(timeStep-1))
                        # change lane of the car
                        curCar.lane = ln
                # calculate the deltaN at this time step
                deltaN = 0
                sum = [0, 0];
                for i in range(l):
                    for j in range(n):
                        if (mat[i][j] is not None):
                            sum[i] += 1
                # append the deltaN at this time
                deltaN = abs(sum[0]-sum[1])
                # total the values
                # print(timeStep)
                averageDeltaNList[timeStep] += deltaN
                deltaNList.append(deltaN);
                tList.append(t)
            
            axs[plotNum].plot(tList, deltaNList)
        
        # divide every value by 10 here 
        for idx in range(len(averageDeltaNList)):
            averageDeltaNList[idx] /= 30
        axs[plotNum].plot(tList, averageDeltaNList, label="average")
        axs[plotNum].legend(loc="upper right")
        axs[plotNum].set_xlabel("time")
        axs[plotNum].set_ylabel("deltaN")
        axs[plotNum].set_title(str(n-num) + "-" + str(num))
        plotNum += 1
    plt.show()

if __name__ == "__main__":
    main()

  