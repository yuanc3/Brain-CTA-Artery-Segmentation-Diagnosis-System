from random import choice
import twoDGrowSeg
from copy import deepcopy


def Processing(slices,number,xPosition,yPosition,thresh,limit,seedGray,changeAccept,selectSeedRange,rangeChangeAccept,direction):
    
    seeds = [twoDGrowSeg.Point(yPosition, xPosition)]
    x_new = []
    y_new = []
    x_mid = yPosition
    y_mid = xPosition
    seedBranch_1 = []
    seedBranch_2 = []
    Branch=0
    seedArray=[]
    tempSeedGray = []
    label=0
    if direction ==2 or direction==0:
        # 下生长
        i = number
        times = 0
        while i < len(slices):
            times += 1
            recentImage = deepcopy(slices[i, :, :])
            if (times >= 2):
                previousTempArea = len(seedArray)
            binaryImg, x_boundary, y_boundary, judge, seedArray = twoDGrowSeg.regionGrow(slices[i, :, :], seeds, seedGray,
                                                                                         x_mid, y_mid,thresh,limit)

            seedBranch_1.clear()
            seedBranch_1.append(twoDGrowSeg.Point(seedArray[len(seedArray)//2].x,seedArray[len(seedArray)//2].y))
            binaryImg_, x_boundary_, y_boundary_, judge_, seedArray_ = twoDGrowSeg.regionGrow(binaryImg, seedBranch_1,
                                                                                         255,x_mid, y_mid, 5, limit)
            #更新参考选择灰度
            seedGray=0
            for j in range(100):
                randomSeed=choice(seedArray)
                seedGray+=slices[i,randomSeed.x,randomSeed.y]
            seedGray=seedGray//100

            recentTempArea = len(seedArray)
            if (times >= 2 and (abs(
                    recentTempArea - previousTempArea) > changeAccept or judge == 1 or recentTempArea == 0)):
                slices[i, :, :] = recentImage
                break
            # if(len(seedArray)!=len(seedArray_)):
            #     print(i,"开始分叉")


            x_min = x_boundary[0]
            x_max = x_boundary[1]
            y_min = y_boundary[0]
            y_max = y_boundary[1]
            x_mid=(x_min+x_max)//2
            y_mid=(y_min+y_max)//2
            slices[i, :, :] = deepcopy(binaryImg)




            for x in range(selectSeedRange-1):
                for y in range(selectSeedRange-1):
                    x_new.append(x_min + round((x_max - x_min) * (x + 1) / selectSeedRange))
                    y_new.append(y_min + round((y_max - y_min) * (y + 1) / selectSeedRange))

            seeds.clear()
            for seed in range((selectSeedRange - 1) * (selectSeedRange - 1)):
                seeds.append(twoDGrowSeg.Point(x_new.pop(), y_new.pop()))

            i += 1
    if direction==1 or direction==2:
        # 上生长
        seeds.clear()
        seeds = [twoDGrowSeg.Point(yPosition, xPosition)]
        seedGray = slices[number - 1, yPosition, xPosition]
        x_mid = yPosition
        y_mid = xPosition
        x_new.clear()
        y_new.clear()
        seedArray.clear()
        previousArea = 0
        for i in range(number - 1):
            recentImage = deepcopy(slices[number - i - 1, :, :])
            if (i >= 1):
                previousTempArea = len(seedArray)
                previousArea = abs(x_max - x_min) * abs(y_max - y_min)
            binaryImg, x_boundary, y_boundary, judge, seedArray = twoDGrowSeg.regionGrow(slices[number - i - 1, :, :], seeds,
                                                                                         seedGray, x_mid, y_mid,thresh,limit)
            # 更新参考选择灰度
            if len(seedArray)!=0:
                tempSeedGray.clear()
                for j in range(100):
                    randomSeed = choice(seedArray)
                    tempSeedGray.append(slices[number - i - 1, randomSeed.x, randomSeed.y])
                tempSeedGray.sort()
                seedGray = tempSeedGray[60]

            x_min = x_boundary[0]
            x_max = x_boundary[1]
            y_min = y_boundary[0]
            y_max = y_boundary[1]
            x_mid = (x_min + x_max) // 2
            y_mid = (y_min + y_max) // 2
            recentTempArea = len(seedArray)
            recentArea=abs(x_max-x_min)*abs(y_max-y_min)
            if recentArea==0:
                Density=0
            else:
                Density=recentTempArea / recentArea
            slices[number - i - 1, :, :] = deepcopy(binaryImg)

            #检测异常
            Test=0
            Num=0
            Max_Num=0
            hhh=0
            if (i >= 1 and  abs(recentArea-previousArea)>200 ):
                for q in range(x_max-x_min):
                    for w in range(y_max-y_min):
                        if Test==1 and slices[number-i-1,q+x_min,w+y_min]!=255:
                            Num+=1
                        if Test==2 and slices[number-i-1,q+x_min,w+y_min]==255:
                            Num+=1
                        if slices[number-i-1,q+x_min,w+y_min]==255:
                            Test=1
                        else:
                            Test=2
                    if Num>Max_Num:
                        Max_Num=Num
                    Num=0
                    Test=0
                    hhh=Max_Num

                Test = 0
                Num = 0
                Max_Num = 0
                for w in range(y_max - y_min):
                    for q in range(x_max - x_min):
                        if Test == 1 and slices[number - i - 1, q + x_min, w + y_min] != 255:
                            Num += 1
                        if Test == 2 and slices[number - i - 1, q + x_min, w + y_min] == 255:
                            Num += 1
                        if slices[number - i - 1, q + x_min, w + y_min] >250:
                            Test = 1
                        else:
                            Test = 2
                    if Num > Max_Num:
                        Max_Num = Num
                    Num = 0
                    Test = 0
                Max_Num += hhh

                if(Max_Num>10):
                    slices[number - i - 1, :, :] = deepcopy(recentImage)
                    break

            if (i >= 1 and (abs(recentTempArea - previousTempArea) > changeAccept or judge == 1 or recentTempArea==0
                            or abs(recentArea-previousArea)>rangeChangeAccept ) ):
                slices[number - i - 1, :, :] =deepcopy(recentImage)
                # print("SeedArea:",recentTempArea - previousTempArea,"Area:",recentArea-previousArea,"Density:",Density)

                break
            if (i >= 1 and len(seedArray) < 60):
                label = 1
            if (label == 1 and abs(recentTempArea - previousTempArea) > 70 and abs(recentArea - previousArea) > 70):
                slices[number - i - 1, :, :] = deepcopy(recentImage)
                break
            seedBranch_1.clear()
            seedBranch_1.append(choice(seedArray))
            binaryImg_, x_boundary_, y_boundary_, judge_, seedArray_ = twoDGrowSeg.regionGrow(binaryImg, seedBranch_1,
                                                                                              252, x_mid, y_mid, 5, limit)
            # print(len(seedArray), len(seedArray_))
            if (len(seedArray) != len(seedArray_)):
                slices[number - i - 1, :, :] = deepcopy(recentImage)
                # print(number - i, "开始分叉")
                for r in range(100):
                    if abs(int(slices[number-i-1,seedBranch_1[0].x,seedBranch_1[0].y])-seedGray)>2:
                        seedBranch_1.clear()
                        seedBranch_1.append(choice(seedArray_))
                    else:
                        break

                for j in range(35):
                    slices[number - i - 1, :, :] = deepcopy(recentImage)
                    seedBranch_2.clear()
                    RandomSeed = choice(seedArray)
                    seedBranch_2.append(RandomSeed)
                    for r in range(100):

                        if abs(int(slices[number - i - 1, seedBranch_2[0].x, seedBranch_2[0].y]) - seedGray) > 2:
                            seedBranch_2.clear()
                            RandomSeed = choice(seedArray)
                            seedBranch_2.append(RandomSeed)
                        else:
                            break
                    slices[number - i - 1, :, :] = deepcopy(binaryImg)
                    binaryImg_1, x_boundary_1, y_boundary_1, judge_1, seedArray_1 = twoDGrowSeg.regionGrow(
                        binaryImg, seedBranch_2,
                        252, x_mid, y_mid, 5, limit)

                    if(abs(len(seedArray_1)+len(seedArray_)-len(seedArray))<5 and len(seedArray_1)>5 and len(seedArray_)>5 ):
                        slices[number - i - 1, :, :] = deepcopy(recentImage)
                        # print("找到分叉")

                        Branch=1
                        break



            if(Branch==1):

                if len(seedArray_)>5:
                    slices=deepcopy(Processing(slices,number-i,seedBranch_1[0].y, seedBranch_1[0].x, thresh,limit,seedGray,changeAccept,selectSeedRange,rangeChangeAccept,1))
                if len(seedArray_1)>5:
                    slices=deepcopy(Processing(slices, number - i , seedBranch_2[0].y, seedBranch_2[0].x, thresh, limit,seedGray,changeAccept, selectSeedRange,rangeChangeAccept,1))
                break


            for x in range(selectSeedRange-1):
                for y in range(selectSeedRange-1):
                    x_new.append(x_min + round((x_max - x_min) * (x + 1) / selectSeedRange))
                    y_new.append(y_min + round((y_max - y_min) * (y + 1) / selectSeedRange))

            seeds.clear()
            for seed in range((selectSeedRange-1)*(selectSeedRange-1)):
                seeds.append(twoDGrowSeg.Point(x_new.pop(), y_new.pop()))


        # for seed in seedArray:
        #     seeds.append(seed)
    return slices



