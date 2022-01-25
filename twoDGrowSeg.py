import numpy as np
import copy


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y


def getGrayDiff(img, seedGray, tmpPoint):
    return abs(seedGray - int(img[tmpPoint.x, tmpPoint.y]))



def selectConnects(p):
    if p != 0:
        connects = [Point(-1, -1), Point(0, -1), Point(1, -1), Point(1, 0), Point(1, 1), \
                    Point(0, 1), Point(-1, 1), Point(-1, 0)]
    else:
        connects = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]
    return connects


def regionGrow(img, seeds, seedGray,x_mid,y_mid,thresh,limit):

    height, weight = img.shape

    seedMark =np.zeros(img.shape)
    img_=copy.deepcopy(img)
    seedList = []
    x_boundary=[0,0]
    y_boundary=[0,0]
    x_boundary[0]=x_mid
    x_boundary[1]=x_mid
    y_boundary[0]=y_mid
    y_boundary[1]=y_mid
    seedArray=[]
    judge=0
    seedNum=0
    for seed in seeds:
        grayDiff = getGrayDiff(img, seedGray, Point(seed.x, seed.y))
        if grayDiff < thresh:

            seedList.append(seed)

    label = 255
    connects = selectConnects(0)
    while (len(seedList) > 0):
        if seedNum>limit:
            judge=1
            break
        currentPoint = seedList.pop(0)
        img_[currentPoint.x, currentPoint.y] = label
        if(seedMark[currentPoint.x, currentPoint.y]==0):
            seedArray.append(Point(currentPoint.x, currentPoint.y))
            seedMark[currentPoint.x, currentPoint.y]=1
        for i in range(4):
            tmpX = currentPoint.x + connects[i].x
            tmpY = currentPoint.y + connects[i].y
            if tmpX < 0 or tmpY < 0 or tmpX >= height or tmpY >= weight:
                continue
            grayDiff = getGrayDiff(img, seedGray, Point(tmpX, tmpY))
            # print(currentPoint.getX(),currentPoint.getY(),tmpX,tmpY)
            # print(img[currentPoint.x,currentPoint.y],img[tmpX,tmpY])

            if grayDiff < thresh  and seedMark[tmpX, tmpY] == 0:
                seedNum+=1
                seedMark[tmpX, tmpY] = 1
                img_[tmpX,tmpY]=label
                seedList.append(Point(tmpX, tmpY))
                seedArray.append( Point(tmpX,tmpY))
                x_boundary[0] = min(x_boundary[0], tmpX)
                x_boundary[1] = max(x_boundary[1], tmpX)
                y_boundary[0] = min(y_boundary[0], tmpY)
                y_boundary[1] = max(y_boundary[1], tmpY)

    return img_,x_boundary,y_boundary,judge,seedArray

