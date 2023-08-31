import matplotlib.pyplot as plt
import math

class Car:

    def __init__(self, ID, initialPos, lane) -> None:
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
        self.vMax = 40
        # lane of car
        self.lane = lane
        # previous time step position
        self.curPosition = self.posArr[0]
        # count the tolerance
        self.tolerance = 0
        
    def getPosition(self, timeStep):
        return self.posArr[timeStep]
    
    def getVelocity(self, timeStep):
        return self.velArr[timeStep]

    def appendVelocity(self, v):
        self.velArr.append(v)

    def appendPosition(self, x):
        self.posArr.append(x)
        self.curPosition = self.posArr[len(self.posArr) - 1]

    def toleranceExceeded(self):
        if (self.tolerance > 1000):
            self.tolerance = 0
            return True
        else:
            return False

# lambd - slope dv/dh
# x1 - position of current car
# x2 - position of next car
# vMax - maximum velocity of current car
# dMin - minimum headway of current car
# delta - reaction time
def func(lambd, x1, x2, vMax, dMin, L):
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
        return (False, -1)
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
                # add to the tolerance counter
                curCar.tolerance += 1
                # if we have exceeded the tolerance for the current car then switch
                if (curCar.toleranceExceeded()):
                    return (True, ln)
                else: 
                    return (False, -1)
                
    return (False, -1)
   
def main():
   
    # lanes
    l = 2
    # length of the road
    L = 100
    # note total velocity
    totalVel = []
    carList = []
    maxVel = 0
    maxCar = 0

    for n in range(0, 31):
        # represents the lanes
        if (n == 0):
            carList.append(n)
            totalVel.append(0)
            continue
        if (n == 1):
            carList.append(n)
            totalVel.append(func(1, 0, 0, 40, 5, L))
            continue

        mat = [[None] * n for _ in range(l) ]
        # stores hBar for each lane
        hBar = [0]*l
        if (n % l == 0):
            for i in range(l):
                hBar[i] = L/(math.floor(n/l))
        else:
            hBar[0] = L/(math.floor(n/l) + 1)
            for i in range(1, l):
                hBar[i] = L/(math.floor(n/l))
        # place the cars
        ID = 0
        cars = n
        i = 0
        while i < n:
            for ln in range(l):
                if (cars > 0):        
                    mat[ln][i] = Car(ID, i*hBar[ln], ln)
                    ID += 1
                    cars -= 1
            i += 1
        # list of times
        tList = [0]
        # the time
        t = 0
        # what time step we are at
        timeStep = 0
        # when to end
        endTime = 100
        # start the time
        while t <= endTime:
            t += 0.01
            timeStep += 1
            seen = []
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
                    shouldSwitch, ln = switch(mat, curCar, (x2-x1) % L, l, L, n, timeStep)
                    # if we should switch, then make the changes
                    if (shouldSwitch):

                        # OUTDATED ------------








                        
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
                        seen.remove(curCar.ID)
                        # Because of sorting, some cars might have missed calculation, so go back and do it again.
                        j = -1
                        i = -1
                        break
                            
                    # get next velocity of curCar based on the function
                    # we have to see if the next car is the same car
                    if (nextCar == curCar):
                        curCar.appendVelocity(func(1, x1, x2, curCar.vMax, curCar.dMin, L))
                    else:     
                        if ((x2 - x1) % L <= curCar.dMin):
                            curCar.appendVelocity(0)
                        else:
                            curCar.appendVelocity(func(1, x1, x2, curCar.vMax, curCar.dMin, L))
                    # get next position
                    curCar.appendPosition((curCar.getPosition(timeStep-1) + 0.01*curCar.getVelocity(timeStep)) % L) 
                    curCar.laneArr.append(curCar.lane)
                    # inc to next car
                    j += 1     
                i += 1
            tList.append(t)
        
        # get the total velocity at the end
        total = 0
        for i in range(l):
            for j in range(n):
                if (mat[i][j] is not None):
                    total += mat[i][j].getVelocity(timeStep)
        if (total > maxVel):
            maxVel = total
            maxCar = n
        # append the total velocity
        totalVel.append(total)
        carList.append(n)



    # plot results 
    plt.plot(carList, totalVel)
    plt.xlabel("# of cars")
    plt.ylabel("total velocity")
    plt.annotate(f"# of cars: {maxCar}, velocity: {maxVel}", xy=(maxCar, maxVel), xytext=(maxCar + 2, maxVel + 2), arrowprops=dict(facecolor='black', width=0.2, headlength=1.5, headwidth=2))
    plt.show()

if __name__ == "__main__":
    main()