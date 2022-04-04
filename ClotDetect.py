from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import pyqtSignal
from numpy import where
import ThreeD
from time import sleep
import resultWindow
import ClotWindow


class ClotDetection():
    _useSignal03=pyqtSignal(str)
    def __init__(self):
        self.size = 0  # 大小
        self.maximum_Area = 0 #最大截面
        self.start_Layer=0 #起始层数
        self.end_Layer=0 #终止层数
        self.layer_Num=0 #分布层数数量
        self.seedArray=[] #种子数
        self.position=""#位置
        self.clotResult=[]
        self.useable=False

    def Processing(self,slices,pre_slices,mark,thresh,flag,windowFlag,ifClosed):
        list = []
        NUM = 1
        judge=False
        self.judgeStr=""
        dim=where(slices==thresh)[0]
        row=where(slices==thresh)[1]
        culumn=where(slices==thresh)[2]

        for i in range (len(slices[slices==thresh])):
            list.append((dim[i],row[i],culumn[i]))
        ClotSet=[ClotDetection() for i in range(128)]

        def clotOver(parameter):
            if parameter=="Closed":
                self.judgeStr="Closed"

        #global clotProcess
        #self.clotProcess=ClotWindow.Process()
        if ifClosed==False:
            self.clotProcess=ClotWindow.Process(False)
        else:
            self.clotProcess=ClotWindow.Process(True)
        self.clotProcess._clotProcessSignal.connect(clotOver)

        
        Times=0
        self.clotProcess.processLabel_02.setText(
            "            Finished Number: " + str(Times))
        while (len(list)!=0):
            if self.judgeStr=="Closed":
                break
            judge=False
            Times+=1
            one=list[0]
            zPosition=one[0]
            xPosition=one[1]
            yPosition=one[2]
            seeds = [ThreeD.Point(zPosition,xPosition, yPosition)]
            slices,ClotSet[NUM-1].seedArray,x_boundary,y_boundary,z_boundary=ThreeD.regionGrow(slices,seeds,slices[zPosition,xPosition,yPosition],1,mark-2)
            ClotSet[NUM-1].size=len(ClotSet[NUM-1].seedArray)
            maximum_Area=0
            for i in range(z_boundary[0],z_boundary[1]+1):
                temArea=0
                for j in range(x_boundary[0],x_boundary[1]+1):
                    for k in range(y_boundary[0], y_boundary[1] + 1):
                        if slices[i,j,k]==mark-2:
                            temArea+=1
                if maximum_Area<temArea:
                    maximum_Area=temArea
            if(y_boundary[0]<256):
                ClotSet[NUM - 1].position="Left"
            else:
                ClotSet[NUM - 1].position = "Right"
            ClotSet[NUM - 1].maximum_Area=maximum_Area
            ClotSet[NUM - 1].start_Layer=z_boundary[0]+1
            ClotSet[NUM - 1].end_Layer=z_boundary[1]+1
            ClotSet[NUM - 1].layer_Num=z_boundary[1]-z_boundary[0]+1
            Delete=where(slices==mark-2)
            #记录(进度条)时间
            totalnum = len(slices[slices == mark-2])
            self.clotProcess.processBar.setValue(0)
            for i in range(totalnum):
                QApplication.processEvents()
                # self.clotProcess.processLabel_04.setText("    ")
                QApplication.processEvents()
                self.clotProcess.processBar.setValue((100 * i) // totalnum)
                QApplication.processEvents()
                sleep(0.008)  # 控制进度条流动的速度
                try:
                    list.remove((Delete[0][i], Delete[1][i], Delete[2][i]))
                except:
                    pass
            QApplication.processEvents()
            # self.clotProcess.processLabel_04.setText("    ")
            QApplication.processEvents()
            self.clotProcess.processBar.setValue((100 * totalnum) //totalnum)
            QApplication.processEvents()
            if(ClotSet[NUM-1].size<3):
                for i in range(z_boundary[0], z_boundary[1] + 1):
                    for j in range(x_boundary[0], x_boundary[1] + 1):
                        for k in range(y_boundary[0], y_boundary[1] + 1):
                            if slices[i, j, k] == mark-2:
                                slices[i, j, k]= pre_slices[i, j, k]
                ClotSet[NUM - 1].start_Layer = -1
            else:
                for i in range(z_boundary[0], z_boundary[1] + 1):
                    for j in range(x_boundary[0], x_boundary[1] + 1):
                        for k in range(y_boundary[0], y_boundary[1] + 1):
                            if slices[i, j, k] == mark-2:
                                for o in range(2):
                                    if (slices[i, j-(o+1), k]== 255) or (slices[i, j-(o+1), k+(o+1)]==255) or(slices[i, j-(o+1), k-(o+1)]==255):
                                        judge=True
                                    if  (slices[i, j, k+(o+1)]==255) or(slices[i, j, k-(o+1)]==255):
                                        judge=True
                                    if (slices[i, j+(o+1), k]== 255) or(slices[i, j+(o+1), k + (o + 1)] == 255) or (slices[i, j+(o+1), k - (o + 1)] == 255):
                                        judge = True
                if judge:
                    NUM += 1
                else:
                    ClotSet[NUM - 1].start_Layer = -1
                    for i in range(z_boundary[0], z_boundary[1] + 1):
                        for j in range(x_boundary[0], x_boundary[1] + 1):
                            for k in range(y_boundary[0], y_boundary[1] + 1):
                                if slices[i, j, k] == mark-2:
                                    slices[i, j, k] = pre_slices[i, j, k]
            self.clotProcess.processLabel_02.setText(
                "            Finished Number: " + str(Times))

            QApplication.processEvents()
            slices[slices == mark - 2]=mark
        if self.judgeStr=="Closed":
            return
        self.clotProcess.hide()
        self.clotProcess.close()
        #self.clotProcess.close()
        #global myResultWindow
        if flag:
            self.myResultWindow=resultWindow.ResultWindow(slices)
            if windowFlag:
                self.myResultWindow.show()
            #print("Create the Result Window")
            self.myResultWindow._useSignal02.connect(self.sendSignal)
            resultStr="Basic patient information:"+"\n"
            #self.myResultWindow.text.moveCursor(QTextCursor.End)
            self.myResultWindow.text.setPlainText(resultStr)
            resultStr="Name:"+"\t\t\t\t"+"Sex:"+"\t\t"+"Age:"+"\t\t\t\t"+"\n"
            self.myResultWindow.text.moveCursor(QTextCursor.End)
            self.myResultWindow.text.append(resultStr)
            resultStr="----------------------------------------------------------------------------------------------------------------------"
            self.myResultWindow.text.moveCursor(QTextCursor.End)
            self.myResultWindow.text.append(resultStr)
            resultStr="Clot:"+"\n"
            self.myResultWindow.text.moveCursor(QTextCursor.End)
            self.myResultWindow.text.append(resultStr)
            #self.getCreateSignal03=self.myResultWindow.getCreateSignal()
            resultStr="ID"+"\t"+"Size"+"    "+"Max Cross Sectional Area"+"    "+"Start Slice"+"    "+" End Slice"+"       "+" Slice Amount"+"        "+"\t"+"Position"
            self.myResultWindow.text.moveCursor(QTextCursor.End)
            self.myResultWindow.text.append(resultStr)
            resultStr="----------------------------------------------------------------------------------------------------------------------"
            self.myResultWindow.text.moveCursor(QTextCursor.End)
            self.myResultWindow.text.append(resultStr)
            # print("Num",NUM)
                # for j in range(ClotSet[i].start_Layer,ClotSet[i].end_Layer+1):
                    # self.clotResult.append(j)
                #self.clotResult.append(ClotSet[i].end_Layer)
                # print("ID:",ClotSet[i].ID," Size:",ClotSet[i].size," maximum_Width",ClotSet[i].maximum_Width,
                #     " maximun_Length:",ClotSet[i].maximum_Length," maximum_Area:",ClotSet[i].maximum_Area,
                #     " start_Layer:",ClotSet[i].start_Layer," end_Layer:",ClotSet[i].end_Layer," layer_Num:",ClotSet[i].layer_Num)
                # resultStr =" "+(str)(ClotSet[i].ID)+"\t"+" "+(str)(ClotSet[i].size)+"\t"+"   "+(str)(ClotSet[i].maximum_Width)+"\t\t"+"   "+(str)(ClotSet[i].maximum_Length)+"\t\t"+"   "+(str)(ClotSet[i].maximum_Area)+"\t\t"+"   "+(str)(ClotSet[i].start_Layer)+"\t\t"+"   "+(str)(ClotSet[i].end_Layer)+"\t\t"+"   "+(str)(ClotSet[i].layer_Num)+"\n"
                # print(resultStr)
                # self.myResultWindow.text.moveCursor(QTextCursor.End)
                # self.myResultWindow.text.append(resultStr)
                # if i!=NUM-2:
                #     resultStr="----------------------------------------------------------------------------------------------------------------------"
                #     self.myResultWindow.text.moveCursor(QTextCursor.End)
                #     self.myResultWindow.text.append(resultStr)
            ClotSet.sort(key=lambda x: x.start_Layer)
            l=ClotSet[1].start_Layer
            r=ClotSet[1].end_Layer

            LargeNUM = 0
            LargeStore = []
            for i in range(128-NUM+1,128):
                if (ClotSet[i].size > 100):
                    LargeNUM = LargeNUM + 1
                    LargeStore.append(i)
                #resultStr =" "+(str)(i-129+NUM+1)+"      "+"   "+(str)(ClotSet[i].size)+"        "+"     "+(str)(ClotSet[i].maximum_Area)+"        "+"          "+(str)(ClotSet[i].start_Layer)+"        "+"        "+(str)(ClotSet[i].end_Layer)+"           "+"       "+(str)(ClotSet[i].layer_Num)+"        "+"      "+ClotSet[i].position+"\n"
                resultStr ="  "+(str)(i-129+NUM+1)+"   "+"\t"+(str)(ClotSet[i].size)+"       "+"\t"+(str)(ClotSet[i].maximum_Area)+"               "+"\t"+(str)(ClotSet[i].start_Layer)+"     "+"\t"+(str)(ClotSet[i].end_Layer)+"      "+"\t"+(str)(ClotSet[i].layer_Num)+"                 "+"\t"+ClotSet[i].position+"\n"
                self.myResultWindow.text.moveCursor(QTextCursor.End)
                self.myResultWindow.text.append(resultStr)
                # print("ID:",i-65+NUM+1," Size:",ClotSet[i].size," maximum_Width",ClotSet[i].maximum_Width,
                # " maximun_Length:",ClotSet[i].maximum_Length," maximum_Area:",ClotSet[i].maximum_Area,
                # " start_Layer:",ClotSet[i].start_Layer," end_Layer:",ClotSet[i].end_Layer," layer_Num:",ClotSet[i].layer_Num)
                if ClotSet[i].start_Layer<=r:
                    r=ClotSet[i].end_Layer
                else:
                    for j in range(l,r+1):
                        self.clotResult.append(j)
                    l=ClotSet[i].start_Layer
                    r=ClotSet[i].end_Layer
            for j in range(l,r+1):
                self.clotResult.append(j)
     
            #self.clotResult.append(j for j in range(l,r+1))
            try:
                self.clotResult.remove(0)
            except:
                pass
            # self.myResultWindow.getClotResult(self.clotResult,1)
            # # self.myResultWindow.printClotResult()
            # clotReport=self.myResultWindow.text.toPlainText()
            # print("ClotReport")
            # print(clotReport)
        resultStr ="----------------------------------------------------------------------------------------------------------------------"+"\n"
        self.myResultWindow.text.moveCursor(QTextCursor.End)
        self.myResultWindow.text.append(resultStr)
        resultStr ="The total number of clots: "+(str)(NUM-1)+", with the amount of larger blood clots:" +(str)(LargeNUM)+"\n"
        self.myResultWindow.text.moveCursor(QTextCursor.End)
        self.myResultWindow.text.append(resultStr)
        if(LargeNUM>0):
            resultStr="Among whom..."+"\n"
            self.myResultWindow.text.moveCursor(QTextCursor.End)
            self.myResultWindow.text.append(resultStr)
        for i in range(128-LargeNUM,128):
            idex=LargeStore.pop()
            resultStr = "The size of the clot is:" + (str)(ClotSet[idex].size) + ", with the start slice serial number:" + (str)(ClotSet[idex].start_Layer)+", the terminating slice serial number:"+(str)(ClotSet[idex].end_Layer)+", and is on " + (str)(ClotSet[idex].position) +" vessel."+"\n"
            self.myResultWindow.text.moveCursor(QTextCursor.End)
            self.myResultWindow.text.append(resultStr)
        self.myResultWindow.getClotResult(self.clotResult,1)
        # self.myResultWindow.printClotResult()
        clotReport=self.myResultWindow.text.toPlainText()
       
        return slices, clotReport, self.clotResult
            # self.maximum_Width = 0  # 最大宽度
            # self.maximum_Length = 0  # 最大长度
            # self.maximum_Area = 0  # 最大截面
            # self.start_Layer = 0  # 起始层数
            # self.end_Layer = 0  # 终止层数
            # self.layer_Num = 0  # 分布层数数量

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




