import matplotlib.pyplot as plt
import math
import random

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
    L = 400
    # the switching time list
    switchingTList = []
    # total velocity
    totalVel = []
    switchingT = 1
    
    while switchingT <= 150:
        # SIMULATION
        mat = [[None]*(n+1) for _ in range(l)]
        cars = [n//2, n//2]
        hBar = [0]*l
        for i in range(len(cars)):
            if (cars[i]):
                hBar[i] = L/cars[i]
        # place the cars
        ID = 0
        for i in range(l):
            for j in range(cars[i]):
                mat[i][j] = Car(ID, j*hBar[i], i, 40)
                ID += 1
        signal = 0
        light = TrafficLight(300, signal)
        mat[signal][len(mat[signal])-1] = light
        mat[signal].sort(key=lambda x: L if x is None else x.getPosition(0))
        # how many switches we made
        count = 0
        # current total velocity
        curTotal = 0
        # the time
        t = 0
        # what time step we are at
        timeStep = 0
        count = 0
        # when to end
        endTime = 10*switchingT
        # print("switching time: " + str(switchingT))
        # start the time
        while t <= endTime:
            t += 0.01
            timeStep += 1
            # go through each lane
            if ((timeStep % (switchingT/0.01)) == 0):
                # remove from previous lane
                for i, c in enumerate(mat[signal]):
                    if (isinstance(c, TrafficLight)):
                        mat[signal][i] = None
                        mat[signal].sort(key=lambda x: L if x is None else x.getPosition(timeStep-1))
                # change signal
                if (signal):
                    signal = 0
                else:
                    signal = 1
                # add to new lane
                light.lane = signal
                mat[signal][len(mat[signal])-1] = light
                mat[signal].sort(key=lambda x: L if x is None else x.getPosition(timeStep-1))
                
                # print("switched!: " + str(timeStep))
            # calculate at current time step
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
                    if (isinstance(curCar, TrafficLight)):
                        j += 1
                        continue
                    # next car's index
                    nextCar = mat[i][(j + 1) % n]
                    if (nextCar == None):
                        nextCar = mat[i][0]
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
                i += 1
            # if it is 1 or 3 then we find the total velocities and average
            if ((timeStep >= (endTime-2*switchingT)/0.01) and (timeStep <= (endTime/0.01))):
                # calculate the total velocities at this time step
                count += 1
                total = 0
                for i in range(l):
                    for j in range(n):
                        if (mat[i][j] is not None and isinstance(mat[i][j], Car)):
                            total += mat[i][j].getVelocity(timeStep) 
                curTotal += total
                # print("timeStep: " + str(timeStep) + " total: " + str(total))
                    
        # switching t
        switchingTList.append(switchingT)
        # inc
        if (switchingT < 10):
            switchingT += 1
        else:
            switchingT += 5
        # total velocity
        totalVel.append(curTotal / count)

    
    plt.plot(switchingTList, totalVel)
    plt.xlabel("switching time")
    plt.ylabel("total velocity")
    plt.show()

if __name__ == "__main__":
    main()

  