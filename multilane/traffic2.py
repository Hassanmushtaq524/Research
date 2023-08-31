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
        # minimum headway
        self.dMin = 5
        # maximum velocity of car
        self.vMax = 40
        # lane of car
        self.lane = lane
        # previous time step position
        self.curPosition = self.posArr[0]

    def getPosition(self, timeStep):
        return self.posArr[timeStep]
    
    def getVelocity(self, timeStep):
        return self.velArr[timeStep]

    def appendVelocity(self, v):
        self.velArr.append(v)

    def appendPosition(self, x):
        self.posArr.append(x)
        self.curPosition = self.posArr[len(self.posArr) - 1]

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

   
def main():
    # number of cars
    n = 3
    # lanes
    l = 2
    # length of the road
    L = 100
    # represents the lanes
    mat = []
    # intialize the lanes
    for i in range(l):
        temp = []
        # every lane can have maximum of n cars
        for j in range(n):
            temp.append(None)
        mat.append(temp)

    # random initial positions
    mat[0][0] = Car(0, 20, 0)
    mat[0][1] = Car(1, 40, 0)
    mat[1][0] = Car(2, 20, 1)
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
            # go through every car
            j = 0
            while j < n:
                # current car's index
                curCar = mat[i][j]
                # if no more cars in this lane, that means no cars anywhere after
                if (curCar == None):
                    break
                # if we have already seen this car, continue
                if (curCar.ID in seen):
                    j += 1
                    continue
                # mark the curCar as seen
                seen.append(curCar.ID)
                # next car's index
                nextCar = mat[i][(j + 1) % n]
                if (nextCar == None):
                    nextCar = mat[i][0]

                # switch car1
                if (t >= 40 and curCar.ID == 1):
                    # switch the car
                    if (curCar.lane == 0):
                        
                        # place the car in lane 1
                        mat[1][len(mat[1])-1] = curCar
                        curCar.lane = 1
                        # remove from current position
                        mat[i][j] = None
                        mat[1].sort(key=lambda x : L if x is None else x.getPosition(timeStep - 1))
                        mat[i].sort(key=lambda x : L if x is None else x.getPosition(timeStep - 1))
                        # print(mat)
                        # get the next car again
                        nextCar = None
                        for a, b in enumerate(mat[1]):
                            if (b is not None):
                                if (b.ID == curCar.ID):
                                    nextCar = mat[1][(a + 1) % n]
                                    if (nextCar == None):
                                        nextCar = mat[1][0]     
                        j -= 1
                        # for a in range(len(mat)):
                        #     for b in range(len(mat[i])):
                        #         if (mat[a][b] is not None):
                        #             print(str(mat[a][b].ID) + "-" + str(mat[a][b].lane), end=" ")
                        #     print("\n")
                                                                        
                # current car's position
                x1 = curCar.getPosition(timeStep - 1)
                # next car's position
                # print(str(curCar.ID) + " " + str(nextCar.ID) + " " + str(timeStep))
                x2 = nextCar.getPosition(timeStep - 1)
                # get next velocity of curCar based on the function
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
                j += 1
            i += 1 
        tList.append(t)
    

    figs, axs = plt.subplots(2, 1)
    for i in range(l):
        for j in range(n):
            if (mat[i][j] is not None):
                carLabel = "Car " + str(mat[i][j].ID);
                axs[0].plot(tList, mat[i][j].velArr, label=carLabel)
                axs[0].set_xlabel("time")
                axs[0].set_ylabel("velocity")
                axs[0].legend(loc="upper left")

    for i in range(l):
        for j in range(n):
            if (mat[i][j] is not None):
                carLabel = "Car " + str(mat[i][j].ID);
                axs[1].plot(tList, mat[i][j].posArr, label=carLabel)
                axs[1].set_xlabel("time")
                axs[1].set_ylabel("position")
                axs[1].legend(loc="upper left")

    plt.show()
if __name__ == "__main__":
    main()