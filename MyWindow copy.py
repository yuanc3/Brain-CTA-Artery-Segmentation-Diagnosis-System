import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pydicom import read_file
from os import walk, path
import numpy as np
from PIL import ImageTk

import time
import SimpleITK as sitk
from copy import deepcopy
import NewQslider
import cv2
import vtk
from PyQt5.QtOpenGL import QGLWidget 
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from MyLabel import MyLabel
import math
from vtk.util import numpy_support
from KeyPressInteractorStyle import *
from vtk.util import vtkImageImportFromArray
import createModel
from threading import Thread
import RGwindow
from tkinter import messagebox
import tkinter as tk
from tkinter import StringVar
import newWindow
import socket
import pickle



global winwidth
winwidth = 350
global wincenter
wincenter = 50
global RG3Dwindow

global width, height
graphWidth = 360
graphHeight = 360

global img
img = 0
Label_Direction = 0


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self, slices=np.zeros((1, 512, 512))):
        self.slices = slices
        self.number=0
        self.yPosition=0
        self.xPosition=0
        # 创建File下的选项以及点击的触发事件
        openFile = QAction('Open File', self)
        openFile.triggered.connect(self.open_file)
        openFolder = QAction('Open Folder', self)
        openFolder.triggered.connect(self.open_folder)
        save = QAction('Save', self)
        save.triggered.connect(self.save)
        # 创建菜单栏，附加一个名为File的菜单
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(openFolder)
        fileMenu.addAction(save)
        # 创建菜单栏其他选项下的选项
        copy = QAction('Copy', self)
        delete = QAction('Delete', self)
        UnetSegemnt = QAction('Unet Segment', self)
        UnetSegemnt.triggered.connect(self.unet_segment)
        ThreeDRGSegment = QAction('3D RG Segment', self)
        ThreeDRGSegment.triggered.connect(self.RG_3D_Segment)
        # 创建菜单栏的其他选项
        viewMenu = menubar.addMenu('&View')
        exitMenu = menubar.addMenu('&Exit')
        exitMenu.addAction(copy)
        exitMenu.addAction(delete)
        segmentMenu = menubar.addMenu('&Segment')
        segmentMenu.addAction(UnetSegemnt)
        segmentMenu.addAction(ThreeDRGSegment)
        helpMenu = menubar.addMenu('&Help')
        self.setGeometry(200, 300, 800, 600)
        self.setWindowTitle("MyWindow")
        self.show()

    def myGrid(self):
        # 定义顶级布局管理器
        mainLayout = QHBoxLayout()
        # 定义左侧布局管理器
        leftgrid_layout = QVBoxLayout()
        # 定义右侧布局管理器
        rightgrid_layout = QVBoxLayout()
        # 对右侧布局进行再次布局
        rightgrid_layout_1 = QHBoxLayout()
        rightgrid_layout_2 = QHBoxLayout()
        #对右下侧布局进行再次布局
        rightgrid_layout_21=QHBoxLayout()
        rightgrid_layout_22=QHBoxLayout()
        # 设置主窗口的布局层
        mainlayout_widget = QWidget()
        mainlayout_widget.setLayout(mainLayout)
        self.setCentralWidget(mainlayout_widget)

        # 对左侧frame进行布局
        # 左侧一共有六个组件
        self.label_01 = QLabel()
        # label_01.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_02 = MyLabel("Section Information")
        self.label_02.setFrameShape(QFrame.Box)
        # label_02.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_03 = MyLabel("X:")
        self.label_03.setFrameShape(QFrame.Box)
        # label_03.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_04 = MyLabel("Y:")
        self.label_04.setFrameShape(QFrame.Box)
        # label_04.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_05 = MyLabel("Z:")
        self.label_05.setFrameShape(QFrame.Box)
        # label_05.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_06 = MyLabel("Gray Value:")
        self.label_06.setFrameShape(QFrame.Box)
        self.button_01=QPushButton("3DSeg",self)
        self.button_01.clicked.connect(self.ThreeDGrowSegment)
        # label_06.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 创建对于左侧窗口的布局
        # leftgrid_layout=QGridLayout()
        leftgrid_layout.addStretch(5)
        # leftgrid_layout.addWidget(label_01,0,0)
        leftgrid_layout.addWidget(self.label_01)
        # leftgrid_layout.addWidget(label_02,1,0)
        leftgrid_layout.addWidget(self.label_02)
        # leftgrid_layout.addWidget(label_03,2,0)
        leftgrid_layout.addWidget(self.label_03)
        # leftgrid_layout.addWidget(label_04,3,0)
        leftgrid_layout.addWidget(self.label_04)
        # leftgrid_layout.addWidget(label_05,4,0)
        leftgrid_layout.addWidget(self.label_05)
        # leftgrid_layout.addWidget(label_06,5,0)
        leftgrid_layout.addWidget(self.label_06)
        leftgrid_layout.addWidget(self.button_01)
        leftgrid_layout.addStretch(5)
        # 对右侧进行布局,两个布局分别放置四个组件
        # 对滑块设置大小
        self.graph_01 = MyLabel(text='',connect=[self.label_03,self.label_04],number=self.number)
        self.graph_01.setGeometry(360, 300, 480, 480)
        self.graph_01.setFrameShape(QFrame.Box)
        self.graph_01_width = self.graph_01.width()
        self.graph_01_height = self.graph_01.height()
        print("graph_01_width", self.graph_01_width)
        print("graph_01_height", self.graph_01_height)
        #self.scroll_01 = NewQslider.MyQSlider()
        self.scroll_01=NewQslider.MyQSlider()
        self.scroll_01.setOrientation(Qt.Vertical)
        # print(self.slices.shape)
        # self.scroll_01.setValue((int)((self.slices.shape[0])/2))
        # 设置步长
        self.scroll_01.setSingleStep(1)
        self.scroll_01.setMinimum(1)
        # 为label设置相应的初始图片
        #print("the value of scroll",self.scroll_01.value())
        #pixmap_imgSrc=self.setInitGraph_01(self.scroll_01.value())
        #self.graph_01.setPixmap(pixmap_imgSrc)
        #self.graph_01.setAlignment(Qt.AlignCenter);
        # self.graph_01.setScaledContents(True)
        # 当滑块移动的时候设置相应的事件
        self.scroll_01.sliderMoved.connect(self.sliderMoved_01)
        self.graph_02 = MyLabel(text='',connect=[self.label_03,self.label_04],number=self.number)
        self.graph_02.setGeometry(840, 300, 480, 480)
        self.graph_02.setFrameShape(QFrame.Box)
        #self.scroll_02 = NewQslider.MyQSlider()
        self.scroll_02=NewQslider.MyQSlider()
        self.scroll_02.setOrientation(Qt.Vertical)
        self.scroll_02.setSingleStep(1)
        self.scroll_02.setMinimum(1)
        self.scroll_02.sliderMoved.connect(self.sliderMoved_02)

        self.graph_03 = MyLabel(text='',connect=[self.label_03,self.label_04],number=self.number)
        self.graph_03.setGeometry(840, 780, 480, 480)
        self.graph_03.setFrameShape(QFrame.Box)
        #self.scroll_03 = NewQslider.MyQSlider()
        self.scroll_03=NewQslider.MyQSlider()
        self.scroll_03.setOrientation(Qt.Vertical)
        self.scroll_03.setSingleStep(1)
        self.scroll_03.setMinimum(1)
        self.scroll_03.sliderMoved.connect(self.sliderMoved_03)
        modelFrame,self.vtkWidget=createModel.model(self.fp,self.slices)
        #thread=ModelThread(createModel.model,(self.fp,self.slices))
        #thread.start()
        #thread.join()
        #modelFrame=thread.get_result()

        rightgrid_layout_1.addWidget(self.graph_01)
        rightgrid_layout_1.addWidget(self.scroll_01)
        rightgrid_layout_1.addWidget(self.graph_02)
        rightgrid_layout_1.addWidget(self.scroll_02)
        #在布局中加入vtk体绘制窗口
        #rightgrid_layout_21.addWidget(self.vtkWidget)
        rightgrid_layout_21.addWidget(modelFrame)
        rightgrid_layout_22.addWidget(self.graph_03)
        rightgrid_layout_22.addWidget(self.scroll_03)
        #rightgrid_layout_2.addWidget(self.graph_04)
        #rightgrid_layout_2.addWidget(self.scroll_04)
        #rightgrid_layout_21.addWidget(self.vtkWidget)



        mainLayout.addLayout(leftgrid_layout)
        mainLayout.addLayout(rightgrid_layout)
        rightgrid_layout.addLayout(rightgrid_layout_1)
        rightgrid_layout.addLayout(rightgrid_layout_2)
        rightgrid_layout_2.addLayout(rightgrid_layout_21)
        rightgrid_layout_2.addLayout(rightgrid_layout_22)
        # 设置布局管理器比例系数
        rightgrid_layout_2.setStretchFactor(rightgrid_layout_21,1)
        rightgrid_layout_2.setStretchFactor(rightgrid_layout_22,1)
        mainLayout.setStretchFactor(leftgrid_layout, 1)
        mainLayout.setStretchFactor(rightgrid_layout, 4)

        # 创建一个左侧窗口的窗口对象
        # leftlayout_widget = QWidget(leftFrame)
        # 设置左侧窗口的布局层
        # leftlayout_widget.setLayout(leftgrid_layout)
        # 设置窗口出现的位置以及窗口的宽和高

    
       
    

    # 自定义函数
    def open_file(self):
        # print("Open File")
        array = []
        # 获得选择好的文件
        self.fp = QFileDialog.getOpenFileName()

        imgs = sitk.ReadImage(self.fp[0])
        TestDirection = (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0)
        img3D_array = sitk.GetArrayFromImage(imgs)
        if imgs.GetDirection() == TestDirection:
            for i in range(len(img3D_array)):
                array.append(img3D_array[len(img3D_array) - i - 1, :, :])
            img3D_array = np.stack([s for s in array])
            global Label_Direction
            Label_Direction = 1
        img3D_array = self.preprocessing(img3D_array)
        self.open(img3D_array)
        self.scroll_01.setValue((int)((self.slices.shape[0]) / 2))
        #print("Value",self.slices.shape[0])
        self.scroll_01.setMaximum(self.slices.shape[0])
        pixmap_imgSrc_01 = self.setInitGraph_01(self.scroll_01.value())
        self.graph_01.setPixmap(pixmap_imgSrc_01)
        self.graph_01.setAlignment(Qt.AlignCenter)
        # self.graph_01.setScaledContents(True)

        self.scroll_02.setValue((int)((self.slices.shape[0]) / 2))
        self.scroll_02.setMaximum(self.slices.shape[0])
        pixmap_imgSrc_02 = self.setInitGraph_02(self.scroll_02.value())
        self.graph_02.setPixmap(pixmap_imgSrc_02)
        self.graph_02.setAlignment(Qt.AlignCenter)
        # self.graph_02.setScaledContents(True)

        self.scroll_03.setValue((int)((self.slices.shape[0]) / 2))
        self.scroll_03.setMaximum(self.slices.shape[0])
        pixmap_imgSrc_03 = self.setInitGraph_03(self.scroll_03.value())
        self.graph_03.setPixmap(pixmap_imgSrc_03)
        self.graph_03.setAlignment(Qt.AlignCenter)
        # self.graph_03.setScaledContents(True)

    def open(self, img3D_array):
        # 用lstFilesDCM作为存放DICOM files的列表
        # PathDicom = filePath #与python文件同一个目录下的文件夹
        self.slices = img3D_array
        # print(self.slices.shape)
        HHH = self.slices[len(self.slices) // 2 - 1].sum() / (512 * 512)
        if HHH < 6:
            adj = (6 - HHH) / 10.972
            self.slices = ((pow(abs(self.slices) / 255, 1 - adj) * 255)).astype(np.uint8)
        self.slices[self.slices > 220] = 220
        print("Open:", self.slices.shape)
        self.myGrid()

    def preprocessing(self, img3D_array):
        # global img3D_array_
        image = img3D_array.copy()
        image = image.astype(np.int16)
        img3D_array_ = img3D_array.astype(np.float32)  # 把数据从 int32转为 float32类型
        img3D_array_ = (img3D_array - img3D_array.min()) / (img3D_array.max() - img3D_array.min())
        # 把数据范围变为0--1浮点,或许还有其他转换方法,效果能更好一些.
        img3D_array = (img3D_array_ * 255).astype(np.uint8)  # 转换为0--255的灰度uint8类型
        return img3D_array

    def open_folder(self):
        # print("Open Folder")
        self.fp = QFileDialog.getExistingDirectory()  # 获得选择好的文件夹
        array = []
        for dirName, subdirList, fileList in walk(self.fp[0]):
            for filename in fileList:
                # if ".dcm" in filename.lower(): #判断文件是否为dicom文件
                # import SimpleITK as sitk
                # itk_img = sitk.ReadImage(os.path.join(dirName,filename))
                # img_array = sitk.GetArrayFromImage(itk_img)[0]
                array.append(read_file(path.join(dirName, filename)))
        array.sort(key=lambda x: float(x.ImagePositionPatient[2]), reverse=True)
        img3D_array = np.stack([s.pixel_array for s in array])
        img3D_array = self.preprocessing(img3D_array)
        self.open(img3D_array)

    # 返回加载在初始Label上的图片
    def setInitGraph_01(self, value):
        print(type(self.slices))
        #img = img.astype(np.uint8)
        img = cv2.resize(src=self.slices[value - 1, :, :], dsize=None, fx=1, fy=1)
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 将nparray转化成QImage对象显示在QLabel中
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        pixmap_imgSrc = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        print("Graph", pixmap_imgSrc.width())
        print("Graph", pixmap_imgSrc.height())
        return pixmap_imgSrc

    def setInitGraph_02(self, value):
        print(self.slices.shape)
        #img = img.astype(np.uint8)
        img = cv2.resize(src=self.slices[:, :, value - 1], dsize=None, fx=1, fy=1)
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 将nparray转化成QImage对象显示在QLabel中
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        pixmap_imgSrc = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        return pixmap_imgSrc

    def setInitGraph_03(self, value):
        print(self.slices.shape)
        #img = img.astype(np.uint8)
        img = cv2.resize(src=self.slices[:, value - 1, :], dsize=None, fx=1, fy=1)
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 将nparray转化成QImage对象显示在QLabel中
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        pixmap_imgSrc = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        return pixmap_imgSrc

    def sliderMoved_01(self):
        self.number = self.scroll_01.value()
        print("wowowowow:", self.scroll_01.value())
        print("HAHAAHA: ",self.number)
        # print(self.slices.shape)
        try:
            img = cv2.resize(src=self.slices[self.number - 1, :, :], dsize=None, fx=1, fy=1)
        except:
            print("IndexError")
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #print(img2.mode)
        # 将nparray转化成QImage对象显示在QLabel中
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        pixmap_imgSrc = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        self.graph_01.setPixmap(pixmap_imgSrc)
        # 图片在label中居中显示
        self.graph_01.setAlignment(Qt.AlignCenter);
        self.graph_01.setScaledContents(False)

    def sliderMoved_02(self):
        self.number = self.scroll_02.value()
        try:
            img = cv2.resize(src=self.slices[:, :, self.number - 1], dsize=None, fx=1, fy=1)
        except:
            print("IndexError")
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        pixmap_imgSrc = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        self.graph_02.setPixmap(pixmap_imgSrc)
        self.graph_02.setAlignment(Qt.AlignCenter);
        self.graph_02.setScaledContents(False)

    def sliderMoved_03(self):
        self.number = self.scroll_03.value()
        try:
            img = cv2.resize(src=self.slices[:, self.number - 1, :], dsize=None, fx=1, fy=1)
        except:
            print("IndexError")
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #print("the type of the picture", img2.dtype)
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        pixmap_imgSrc = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        self.graph_03.setPixmap(pixmap_imgSrc)
        self.graph_03.setAlignment(Qt.AlignCenter);
        self.graph_03.setScaledContents(False)

    # 定义鼠标事件
    # 滚轮事件
    def wheelEvent(self, event):
        #        if event.delta() > 0:                                                 # 滚轮上滚,PyQt4
        # This function has been deprecated, use pixelDelta() or angleDelta() instead.
        angle = event.angleDelta() / 8  # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
        angleX = angle.x()  # 水平滚过的距离(此处用不上)
        angleY = angle.y()  # 竖直滚过的距离
        if angleY > 0:
            print("鼠标滚轮上滚")  # 响应测试语句
        else:  # 滚轮下滚
            print("鼠标滚轮下滚")  # 响应测试语句

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        s = event.windowPos()
        self.setMouseTracking(True)
        print("1")

    # 鼠标单击事件
    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.number=self.scroll_01.value()
            self.label_05.setText("Z: " + str(self.number))
            print("self.number:",self.number)
            self.grayValue=self.slices[self.number - 1,self.graph_01.yPosition, self.graph_01.xPosition]
            self.label_06.setText("Gray Value: "+str(self.grayValue))
            self.xPosition=self.graph_01.xPosition
            self.yPosition=self.graph_01.yPosition

        elif event.buttons() == QtCore.Qt.RightButton:  # 右键按下
            print("单击鼠标右键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.MidButton:  # 中键按下
            print("单击鼠标中键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.RightButton:  # 左右键同时按下
            print("单击鼠标左右键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.MidButton:  # 左中键同时按下
            print("单击鼠标左中键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.MidButton | QtCore.Qt.RightButton:  # 右中键同时按下
            print("单击鼠标右中键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.MidButton \
                | QtCore.Qt.RightButton:  # 左中右键同时按下
            print("单击鼠标左中右键")  # 响应测试语句

    def enterEvent(self, e):  # 鼠标移入label
        pass

    def save(self):
        print("Save")

    def RG_3D_Segment(self):
        global RG3Dwindow
        self.slices[self.slices > 254] = 254  # 用254代替255灰度信息，便于后续模型建立
        RG3Dwindow = RGwindow.RGwindow(fp=self.fp, slices=self.slices, number=self.number)
        #RGwindow.RGwindow(fp=self.fp, slices=self.slices, number=self.number)
       

    def ThreeDGrowSegment(self):
        import threeDGrowSeg
        import time
        time_start = time.time()  # 开始计时
        thresh = 8  # 调节灰度取值域
        limit = 1200  # 调节灰度面积取值上限
        changeAccept = 350  # 调节覆盖点变化量上限
        selectSeedRange = 10  # 种子点选择域
        rangeChangeAccept = 2000  # 调节允许灰度面积变化量上限
        seedGray = self.slices[self.number - 1, self.yPosition, self.xPosition]
        self.slices = threeDGrowSeg.Processing(self.slices, self.number, self.xPosition, self.yPosition, thresh, limit,
                                               seedGray,
                                               changeAccept, selectSeedRange, rangeChangeAccept, direction=2)
        time_end = time.time()  # 结束计时
        timeperoid = time_end - time_start
        print(timeperoid)
        # 获取无背景图
        slices_only = deepcopy(self.slices)
        slices_only[slices_only < 250] = 0

        ##导出nii
        # 原图
        # out = sitk.GetImageFromArray(self.slices)
        # 无背景图
        out = sitk.GetImageFromArray(slices_only)
        if Label_Direction == 1:
            out.SetDirection((0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0))
        #sitk.WriteImage(out, 'path_saved.nii.gz')
    def receiveFrom(self, conn):
        buffer=1024 * 100
        info = ''.encode()
        while 1:
            data = conn.recv(buffer)
            info += data
            if not data:
                break

        # 信息的切割，一定要encode， 否则会失败
        info = info.split('####'.encode())

        file_name = info[0].decode()
        file_data = info[1]
        # file_path = '\\'.join(file_name.split('\\')[:-1:])
        file_name=file_name.split("\\")[-1]
        # # 创建路径
        # os.makedirs(file_path, exist_ok=True)
        print("====saved===="+file_name)
        # 保存
        with open(file_name, 'wb') as f:
            f.write(file_data)

    def sendTo(self, sk, path):
        buffer = 1024 * 100
        with open(path, 'rb') as f:
            lenth = 0
            while 1:
                # print("x")
                data = f.read(buffer)
                if lenth:
                    sk.send(data)
                else:
                    sk.send(path.encode() + '####'.encode() + data)
                if len(data) < buffer:
                    break
                lenth += len(data)

    def unet_segment(self):
        
        # fp = filedialog.askopenfilename()
        # imgs = sitk.ReadImage(fp)
        # img3D_array = sitk.GetArrayFromImage(imgs)
        # array=[]
        # for i in range(len(img3D_array)):
        #     array.append(img3D_array[len(img3D_array)-i-1,:,:])
        # img3D_array = np.stack([s for s in array])
        # img3D_array = self.preprocessing(img3D_array)
        seg_img = []
        prUet=[]
        img3D_array = self.slices
        # 处理进度条
        jindutiao = tk.Tk()
        jindutiao.attributes('-topmost',True)
        sw = jindutiao.winfo_screenwidth()
        sh = jindutiao.winfo_screenheight()
        #ww = 440
        ww=500
        wh = 120
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        jindutiao.geometry("%dx%d+%d+%d" % (ww, wh, x, y - 50))
        jindutiao.title('Segmentation')
        # 设置下载进度条
        tk.Label(jindutiao, text='Processing:', ).place(x=0, y=40)
        textVar1 = StringVar()
        textVar2 = StringVar()
        textVar3 = StringVar()
        tk.Label(jindutiao, textvariable=textVar1).place(x=120, y=65)
        tk.Label(jindutiao, textvariable=textVar2).place(x=120, y=85)
        tk.Label(jindutiao, textvariable=textVar3).place(x=350, y=40)
        canvas = tk.Canvas(jindutiao, width=250, height=20, bg="white")
        canvas.place(x=100, y=40)
        # 填充进度条
        fill_line = canvas.create_rectangle(1.5, 1.5, 0, 21, width=0, fill="green")
        x = len(img3D_array)
        n = 250 / x  # 300是矩形填充满的次数

        def end():
            yes = messagebox.askokcancel(title='Warning!',
                                         message='Are you sure to close the window, that means you discard image segmentation!')
            if yes:
                jindutiao.destroy()
                return

        i = 1
        jindutiao.protocol("WM_DELETE_WINDOW", end)
        buffer = 1024 * 100
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.connect(("192.168.3.106", 8000))
        print(self.fp[0])
        self.sendTo(sk, self.fp[0])
        sk.close()
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.connect(("192.168.3.106", 8000))
        print("\nStart segmentation...")
        # from tqdm import tqdm
        # with tqdm(total=len(img3D_array),
        #           desc=f'Processing',
        #           mininterval=0.3) as pbar:
        #     for img in img3D_array:

        #         peroidtime = time.time()
                

                
        #         # path = reset_pic_quality(path)
        #         # print("==begin===")
                

        #         seg_img.append(imgUnet)
        #         prUet.append(pr)
        #         peroid = time.time() - peroidtime
        #         textVar1.set('Time remain: ' + str(int(peroid * (len(img3D_array) - i))) + 's, Speed: ' + str(
        #             round(1 / (time.time() - peroidtime), 1)) + 'it/s')
        #         # textVar2.set('Total: '+str(len(img3D_array))+'slices, Processed: '+ str(i)+'slices')
        #         # textVar3.set(str(int(i*100/len(img3D_array)))+'%')
        #         textVar3.set(str(i) + '/' + str(len(img3D_array)) + ' slices')
        #         pbar.update(1)
        #         n = n + 250 / x
        #         i += 1
        #         canvas.coords(fill_line, (0, 0, n, 60))
        #         jindutiao.update()
        #         time.sleep(0.02)  # 控制进度条流动的速度

        # jindutiao.destroy()
        
        
        self.receiveFrom(sk)
        print("2")
        sk.close()
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.connect(("192.168.3.106", 8000))
        self.receiveFrom(sk)
        print("3")

        seg_imgarray = np.load('1.npz')['arr_0']
        prUetarray = np.load('2.npz')['arr_0']


        print("Finished!")
        

        global window
        window = newWindow.NewWindow(seg_imgarray, self.fp, prUetarray,self.number)
        # img=Image.fromarray(img)
        # img=ImageTk.PhotoImage(img)
        # l1.config(image=img)
        # l1.image=img

    #确定关闭窗口后的事件，将vtk删除干净，否则会出现句柄无效的错误
    def closeEvent(self, event):
        self.vtkWidget.Finalize()
        #self.vtkWidget3DTwo.Finalize()


    
   