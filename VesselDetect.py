import math
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QTextCursor
from numpy import where
import ThreeD
from time import sleep
import resultWindow
import VesselWindow
from decimal import Decimal


class VesselDetection():
    def __init__(self):
        self.ID = 0  # 序号
        self.size = 0  # 大小
        self.maximum_Width=0 # 最大宽度
        self.maximum_Length=0 #最大长度
        self.maximum_Area = 0 #最大截面
        self.start_Layer=0 #起始层数
        self.end_Layer=0 #终止层数
        self.layer_Num=0 #分布层数数量
        self.position=""
        self.crossArea=[]
        self.crossAreaSlice=[]
        self.avgArea=0
        self.stenosis=[]
        self.stenosisSlice=[]

        self.seedArray=[] #种子数
        self.vesselResult=[]

    def Processing(self,slices,pre_slices,mark,thresh,flag,windowFlag,ifClosed):

        list = []
        NUM = 1
        self.judgeStr=""
        dim=where(slices==thresh)[0]
        row=where(slices==thresh)[1]
        culumn=where(slices==thresh)[2]

        for i in range (len(slices[slices==thresh])):
            list.append((dim[i],row[i],culumn[i]))
        VesselSet=[VesselDetection() for i in range(128)]

        def clotOver(parameter):
            if parameter=="Closed":
                self.judgeStr="Closed"

        #global clotProcess
        #self.clotProcess=ClotWindow.Process()
        if ifClosed==False:
            self.vesselProcess=VesselWindow.Process(False)
        else:
            self.vesselProcess=VesselWindow.Process(True)
        self.vesselProcess._vesselProcessSignal.connect(clotOver)
        

        Times=0

        self.vesselProcess.processLabel_02.setText(
            "            Finished Number: " + str(Times))
        while (len(list)!=0):
            if self.judgeStr=="Closed":
                break
            Times+=1
            VesselSet[NUM-1].ID=NUM
            one=list[0]
            zPosition=one[0]
            xPosition=one[1]
            yPosition=one[2]
            seeds = [ThreeD.Point(zPosition,xPosition, yPosition)]
            slices,VesselSet[NUM-1].seedArray,x_boundary,y_boundary,z_boundary=ThreeD.regionGrow(slices,seeds,slices[zPosition,xPosition,yPosition],1,(mark-2))
            VesselSet[NUM-1].size=len(VesselSet[NUM-1].seedArray)
            maximum_Area=0
            for i in range(z_boundary[0],z_boundary[1]+1):
                temArea=0
                for j in range(x_boundary[0],x_boundary[1]+1):
                    for k in range(y_boundary[0], y_boundary[1] + 1):
                        if slices[i,j,k]==mark-2:
                            VesselSet[NUM-1].avgArea+=1
                            temArea+=1
                try:
                    if (i!=z_boundary[0] and i!=z_boundary[1]):
                        VesselSet[NUM - 1].crossArea.append(temArea)
                        VesselSet[NUM - 1].crossAreaSlice.append(i+1)
                except:
                    pass
                if maximum_Area < temArea:
                    maximum_Area = temArea
            if (y_boundary[0] < 256):
                VesselSet[NUM - 1].position = "Left"
            else:
                VesselSet[NUM - 1].position = "Right"
            VesselSet[NUM - 1].avgArea = VesselSet[NUM - 1].avgArea / (z_boundary[1] - z_boundary[0] + 1)
            NASCET=0
            slice=0

            avgRadius=math.sqrt(VesselSet[NUM - 1].avgArea/math.pi)
            for i in range(z_boundary[0]+1, z_boundary[1]):
                NASCET=VesselSet[NUM - 1].crossArea.pop()
                slice=VesselSet[NUM - 1].crossAreaSlice.pop()
                NASCET=(avgRadius-math.sqrt(NASCET/math.pi))/avgRadius
    
                NASCET=Decimal(NASCET).quantize(Decimal('0.000'))
               
                #NASCET=round(NASCET,3)
                #NASCET=(float)('%.3f'%NASCET)
                #NASCET=round(NASCET,3)
                if(NASCET>0.4):
                    VesselSet[NUM - 1].stenosis.append(NASCET)
                    VesselSet[NUM - 1].stenosisSlice.append(slice)



     
            VesselSet[NUM - 1].maximum_Area=maximum_Area
            VesselSet[NUM - 1].maximum_Width=x_boundary[1]-x_boundary[0]+1
            VesselSet[NUM - 1].maximum_Length=y_boundary[1]-y_boundary[0]+1
            VesselSet[NUM - 1].start_Layer=z_boundary[0]+1
            VesselSet[NUM - 1].end_Layer=z_boundary[1]+1
            VesselSet[NUM - 1].layer_Num=z_boundary[1]-z_boundary[0]+1
  
            Delete=where(slices==mark-2)
            # 记录(进度条)时间
    
            totalnum=len(slices[slices == mark-2])
            self.vesselProcess.processBar.setValue(0)
            for i in range(totalnum):
                try:
                    if(i%(totalnum//100)==0):
                        # self.vesselProcess.processLabel_04.setText("    ")
                        QApplication.processEvents()
                        self.vesselProcess.processBar.setValue((100 * i) / totalnum)
                        QApplication.processEvents()
                        sleep(0.003)  # 控制进度条流动的速度
                    try:
                        list.remove((Delete[0][i], Delete[1][i], Delete[2][i]))
                    except:
                        pass
                except:
                    #self.vesselProcess.processLabel_04.setText("    ")
                    QApplication.processEvents()
                    self.vesselProcess.processBar.setValue((100 * i) / totalnum)
                    QApplication.processEvents()
                    sleep(0.002)  # 控制进度条流动的速度
                    list.remove((Delete[0][i], Delete[1][i], Delete[2][i]))

            QApplication.processEvents()
            #self.vesselProcess.processLabel_04.setText("    ")
            QApplication.processEvents()
            self.vesselProcess.processBar.setValue((100 * totalnum) / totalnum)
            QApplication.processEvents()
            if(VesselSet[NUM-1].size<1000):
                for i in range(z_boundary[0], z_boundary[1] + 1):
                    for j in range(x_boundary[0], x_boundary[1] + 1):
                        for k in range(y_boundary[0], y_boundary[1] + 1):
                            if slices[i, j, k] == mark-2:
                                slices[i, j, k]= pre_slices[i, j, k]
                VesselSet[NUM-1].start_Layer=-1
            else:
                NUM += 1
            self.vesselProcess.processLabel_02.setText(
                "            Finished Number: " + str(Times))
            QApplication.processEvents()
            slices[slices == mark - 2]=mark
        if self.judgeStr=="Closed":
            return
        self.vesselProcess.hide()
        self.vesselProcess.close()

        moderate = 0
        severe = 0
        if flag:
            self.myResultWindow=resultWindow.ResultWindow(slices)
            if windowFlag:
                self.myResultWindow.show()
            resultStr="----------------------------------------------------------------------------------------------------------------------"+"\n"
            self.myResultWindow.text.setPlainText(resultStr)
            resultStr="Vessel:"+"\n"
            self.myResultWindow.text.moveCursor(QTextCursor.End)
            self.myResultWindow.text.append(resultStr)
            resultStr="ID "+"    "+"Slice "+"    "+"NASCET "+"        "+"Stenosis Degree "+"           "+"\t"+"Position "+"\n"
            self.myResultWindow.text.moveCursor(QTextCursor.End)
            self.myResultWindow.text.append(resultStr)
            resultStr="----------------------------------------------------------------------------------------------------------------------"+"\n"
            self.myResultWindow.text.moveCursor(QTextCursor.End)
            self.myResultWindow.text.append(resultStr)
            VesselSet.sort(key=lambda x: x.start_Layer)
            l=VesselSet[0].start_Layer
            r=VesselSet[0].end_Layer
            Degree=""
            total=0
            for i in range(128-NUM+1,128):
                for j in range(len(VesselSet[i].stenosis)):
                    total+=1
                    NASCET=VesselSet[i].stenosis.pop()
                    #NASCET = (float)('%.3f' % NASCET)
                    NASCET=Decimal(NASCET).quantize(Decimal('0.000'))
                    stenosisSlice=VesselSet[i].stenosisSlice.pop()
                    if (NASCET >= 0.7):
                        severe += 1
                        Degree="Severe"
                    if (NASCET > 0.4 and NASCET<0.7):
                        moderate+= 1
                        Degree="Moderate"
                    resultStr =" "+(str)(total)+"    "+"\t"+(str)(stenosisSlice)+"    "+"\t"+(str)(NASCET)+"        "+"\t"+Degree+"        "+"       \t"+"\t"+(str)(VesselSet[i].position)+"\n"
                    self.myResultWindow.text.moveCursor(QTextCursor.End)
                    self.myResultWindow.text.append(resultStr)
                    #print("ID:",(str)(total)," Slice:",(str)(stenosisSlice)," NASCET:",(str)(NASCET)," Degree:",Degree," Position:",(str)(VesselSet[i].position))
                    if VesselSet[i].start_Layer<=r:
                            r=VesselSet[i].end_Layer
                    else:
                        for j in range(l,r+1):
                            self.vesselResult.append(j)
                        l=VesselSet[i].start_Layer
                        r=VesselSet[i].end_Layer
        resultStr = "----------------------------------------------------------------------------------------------------------------------"
        self.myResultWindow.text.moveCursor(QTextCursor.End)
        self.myResultWindow.text.append(resultStr)
        resultStr = "The total number of Vascular Stenosis is: "+str(severe+moderate)+". Among them, there were "+str(moderate)+\
                    " moderate stenosis vascular layers (0.4 < NASCET < 0.7) and "+str(severe)+" severe stenosis vascular layers (NASCET ≥ 0.7)."+"\n"
        self.myResultWindow.text.moveCursor(QTextCursor.End)
        self.myResultWindow.text.append(resultStr)
        for j in range(l,r+1):
            self.vesselResult.append(j)
        #self.clotResult.append(j for j in range(l,r+1))
        #self.myResultWindow.getVesselDetect(self.vesselResult,2)
        # self.myResultWindow.printVesselResult()
        vesselReport=self.myResultWindow.text.toPlainText()
        return slices, vesselReport,self.vesselResult
            # self.maximum_Width = 0  # 最大宽度
            # self.maximum_Length = 0  # 最大长度
            # self.maximum_Area = 0  # 最大截面
            # self.start_Layer = 0  # 起始层数
            # self.end_Layer = 0  # 终止层数
            # self.layer_Num = 0  # 分布层数数量
    def sendImage(self,image):
        self.image=image
        self.myResultWindow.getImage(image)
    def sendSignal(self,parameter):
        pass
        #self._useSignal03.emit(parameter)
        # if parameter=="Useable":
        #     self.useable=True

    def getSignal(self):
        return self.useable
    # def getCreateSignal(self):
    #     return self.getCreateSignal03


