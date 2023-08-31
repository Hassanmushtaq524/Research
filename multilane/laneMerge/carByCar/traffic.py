import matplotlib.pyplot as plt
import math
import random

# Car Class
class Car:

    def __init__(self, ID, initialPos, lane, vMax) -> None:
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
        # previous time step position
        self.curPosition = self.posArr[0]
        # count the tolerance
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
        if (self.impatience > 500):
            self.impatience = 0
            return True
        else:
            return False


# Closed lane traffic light
class TrafficLight:

    def __init__(self, position, lane):
        self.position = position
        self.lane = lane

    def getPosition(self, timestep):
        return self.position

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
    n = 10
    # lanes
    l = 2
    # length of the road
    L = 3000
    # SETTING UP CARS
    # represents the lanes
    mat = [[None]*(n+1) for _ in range(l+1)] # lane 2 is the merge lane 
    # stores number of cars in each lane
    cars = [5, 5]
    # place the cars
    ID = 0
    for i in range(l):
        for j in range(cars[i]):
            mat[i][j] = Car(ID, j*5, i, 40)
            ID += 1
    # display the initial positions
    for a in range(l + 1):
        for b in range(n):
            if (mat[a][b] is None):
                print(None, end=" ")
            else:
                if (isinstance(mat[a][b], Car)):
                    print(str(mat[a][b].ID) + "-" + str(mat[a][b].getPosition(0)), end=" ")
                else:
                    print("T-" + str(mat[a][b].getPosition(0)), end=" ")
        print("\n")
    # list of times
    tList = [0]
    # the time
    t = 0
    # what time step we are at
    timeStep = 0
    # when to end
    endTime = 300

    # TRAFFIC LIGHT PARAMS
    # leading car's index
    leadingIdx = n//2 - 1
    # when lane 0 closes
    mergeTime = 0.1
    # signal means the lane the car is in
    signal = 1
    # set the crossing point
    crossingPoint = 0
    # SIMULATION
    # start the time
    while t <= endTime:
        t += 0.01
        timeStep += 1
        seen = []
        switchingCars = []
        # its time to close lane 0
        if (timeStep == (mergeTime/0.01)):
            for a in range(len(mat[signal])):
                if (mat[signal][a] is None):
                    # we reached the first none slot, use the leading car's position to place the traffic light
                    crossingPoint = mat[signal][a - 1].getPosition(timeStep - 1) + 5
                    mat[signal][a] = TrafficLight(crossingPoint, signal)
                    break
            # display the positions
            for a in range(l + 1):
                for b in range(n):
                    if (mat[a][b] is None):
                        print(None, end=" ")
                    else:
                        if (isinstance(mat[a][b], Car)):
                            print(str(mat[a][b].ID) + "-" + str(mat[a][b].getPosition(timeStep - 1)), end=" ")
                        else:
                            print("T-" + str(mat[a][b].getPosition(0)), end=" ")
                print("\n")
            print(timeStep)
        # see if the leading car that needs to merge has crossed the crossing point
        if (leadingIdx >= 0):
            if (timeStep >= (mergeTime/0.01) and mat[int(not signal)][leadingIdx].getPosition(timeStep-1) > crossingPoint):
                # switch the car that crossed
                curCar, ln = mat[int(not signal)][leadingIdx], 2
                print(str(curCar.ID) + " switched: " + str(curCar.lane) + " to " + str(ln) + " timeStep: " + str(timeStep))
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
                # reduce the leadingIdx if both mat[0][leadingIdx] and mat[1][leadingIdx] are empty
                if ((mat[0][leadingIdx] is None or isinstance(mat[0][leadingIdx], TrafficLight)) and 
                    (mat[1][leadingIdx] is None or isinstance(mat[1][leadingIdx], TrafficLight))):
                    leadingIdx -= 1
                        

                # now we switch the traffic light
                for i in range(len(mat[signal])):
                    if (isinstance(mat[signal][i], TrafficLight)):
                        # switch to the other lane
                        mat[signal][i] = None
                        signal = int(not signal)
                        mat[signal][len(mat[signal]) - 1] = TrafficLight(crossingPoint, signal)
                        mat[signal].sort(key=lambda x : L if x is None else x.getPosition(timeStep-1))
                        break
                # display the positions
                for a in range(l + 1):
                    for b in range(n):
                        if (mat[a][b] is None):
                            print(None, end=" ")
                        else:
                            if (isinstance(mat[a][b], Car)):
                                print(str(mat[a][b].ID) + "-" + str(mat[a][b].getPosition(timeStep - 1)), end=" ")
                            else:
                                print("T-" + str(mat[a][b].getPosition(0)), end=" ")
                    print("\n")


        # go through each lane
        i = 0
        while i < l + 1:
            j = 0
            # go through every car
            while j < n:
                # current car's index
                curCar = mat[i][j]
                # if no more cars in this lane, that means no cars anywhere after
                if (curCar == None):
                    break
                # if current car is a traffic light, skip
                if (isinstance(curCar, TrafficLight)):
                    j += 1
                    continue         
                # mark the curCar as seen
                seen.append(curCar.ID)
                # next car's index
                nextCar = mat[i][(j + 1) % n]
                if (nextCar == None):
                    # see if merged lane ahead has a car
                    if (mat[2][0] == None):
                        nextCar = mat[i][0]
                    else:
                        nextCar = mat[2][0]
                    
                # current car's position
                x1 = curCar.getPosition(timeStep - 1)
                # next car's position
                x2 = nextCar.getPosition(timeStep - 1)
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
            # inc to next lane
            i += 1
        # append to the times
        tList.append(t)
    
    # DISPLAYING RESULTS
    figs, axs = plt.subplots(2, 1)
    for i in range(l + 1):
        for j in range(n):
            if (mat[i][j] is not None and isinstance(mat[i][j], Car)):
                carLabel = "Car " + str(mat[i][j].ID);
                axs[0].plot(tList, mat[i][j].velArr, label=carLabel)
                axs[0].set_xlabel("time")
                axs[0].set_ylabel("velocity")
                axs[0].legend(loc="upper right")
    for i in range(l + 1):
        for j in range(n):
            if (mat[i][j] is not None and isinstance(mat[i][j], Car)):
                carLabel = "Car " + str(mat[i][j].ID);
                axs[1].plot(tList, mat[i][j].posArr, label=carLabel)
                axs[1].set_xlabel("time")
                axs[1].set_ylabel("position")
                axs[1].legend(loc="upper right")
    plt.show()

if __name__ == "__main__":
    main()

  