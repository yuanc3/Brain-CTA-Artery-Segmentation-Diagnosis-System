from numpy import zeros
from copy import deepcopy


class Point(object):
    def __init__(self, z,x, y):
        self.x = x
        self.y = y
        self.z = z

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z


def getGrayDiff(img, seedGray, tmpPoint):
    return abs(seedGray - int(img[tmpPoint.z,tmpPoint.x, tmpPoint.y]))



def selectConnects(p):
    if p != 0:
        connects = [Point(0,-1, -1), Point(0,0, -1), Point(0,1, -1), Point(0,1, 0), Point(0,1, 1), \
                    Point(0,0, 1), Point(0,-1, 1), Point(0,-1, 0),Point(1,-1, -1), Point(1,0, -1), Point(1,1, -1), Point(1,1, 0), Point(1,1, 1), \
                    Point(1,0, 1), Point(1,-1, 1), Point(1,-1, 0),Point(-1,-1, -1), Point(-1,0, -1), Point(-1,1, -1), Point(-1,1, 0), Point(-1,1, 1), \
                    Point(-1,0, 1), Point(-1,-1, 1), Point(-1,-1, 0)]
    else:
        connects = [Point(0,0, -1), Point(0,1, 0), Point(0,0, 1), Point(0,-1, 0),Point(1,0, -1), Point(1,1, 0), Point(1,0, 1), Point(1,-1, 0),
                    Point(-1,0, -1), Point(-1,1, 0), Point(-1,0, 1), Point(-1,-1, 0)]
    return connects


def regionGrow(slices, seeds, seedGray,thresh,mark):
    x_boundary=[]
    y_boundary=[]
    z_boundary=[]

    dim,height, weight = slices.shape

    seedMark =zeros(slices.shape)
    slices_=deepcopy(slices)
    seedList = []

    seedArray=[]
    judge=0
    seedNum=0
    for seed in seeds:
        grayDiff = getGrayDiff(slices, seedGray, Point(seed.z,seed.x, seed.y))
        if grayDiff < thresh:

            seedList.append(seed)

    label = mark
    connects = selectConnects(1)
    times=0
    while (len(seedList) > 0):
        times+=1
        currentPoint = seedList.pop(0)
        if(times==1):
            x_boundary=[0,0]
            y_boundary = [0, 0]
            z_boundary = [0, 0]
            x_boundary[0] = currentPoint.x
            x_boundary[1] = currentPoint.x
            y_boundary[0] = currentPoint.y
            y_boundary[1] = currentPoint.y
            z_boundary[0] = currentPoint.z
            z_boundary[1] = currentPoint.z
        slices_[currentPoint.z,currentPoint.x, currentPoint.y] = label
        if(seedMark[currentPoint.z,currentPoint.x, currentPoint.y]==0):
            seedArray.append(Point(currentPoint.z,currentPoint.x, currentPoint.y))
            seedMark[currentPoint.z,currentPoint.x, currentPoint.y]=1
        for i in range(24):
            tmpX = currentPoint.x + connects[i].x
            tmpY = currentPoint.y + connects[i].y
            tmpZ = currentPoint.z + connects[i].z
            if tmpX < 0 or tmpY < 0 or tmpZ<0 or tmpX >= height or tmpY >= weight or tmpZ >= dim:
                continue
            grayDiff = getGrayDiff(slices, seedGray, Point(tmpZ,tmpX, tmpY))

            if grayDiff < thresh  and seedMark[tmpZ,tmpX, tmpY] == 0:
                seedNum+=1
                seedMark[tmpZ,tmpX, tmpY] = 1
                slices_[tmpZ,tmpX,tmpY]=label
                seedList.append(Point(tmpZ,tmpX, tmpY))
                seedArray.append( Point(tmpZ,tmpX,tmpY))
                x_boundary[0] = min(x_boundary[0], tmpX)
                x_boundary[1] = max(x_boundary[1], tmpX)
                y_boundary[0] = min(y_boundary[0], tmpY)
                y_boundary[1] = max(y_boundary[1], tmpY)
                z_boundary[0] = min(z_boundary[0], tmpZ)
                z_boundary[1] = max(z_boundary[1], tmpZ)


    return slices_,seedArray,x_boundary,y_boundary,z_boundary

