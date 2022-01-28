import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pydicom import read_file
from os import walk, path
import numpy as np
import SimpleITK as sitk
from copy import deepcopy
import NewQslider
import cv2
from KeyPressInteractorStyle import *
import createModel
import sip


class NewWindow(QMainWindow):
    def __init__(self, slices, fp,pr,number):
        super().__init__()
        self.number=number
        self.contrVal=1
        self.fp = fp
        self.pr=pr
        self.slices = slices
        self.initUI()
        self.open_file()

    def initUI(self):
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
        ThreeDRGSegment = QAction('3D RG Segment', self)
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
        self.setWindowTitle("NewWindow")
        self.show()

    def myGrid(self):
        # 定义顶级布局管理器
        self.mainLayout = QHBoxLayout()
        # 定义左侧布局管理器
        #self.leftgrid_layout = QVBoxLayout()
        # 定义右侧布局管理器
        self.rightgrid_layout = QVBoxLayout()
        # 对右侧布局进行再次布局
        self.rightgrid_layout_1 = QHBoxLayout()
        self.rightgrid_layout_2 = QHBoxLayout()
        #对右下侧布局进行再次布局
        self.rightgrid_layout_21=QHBoxLayout()
        self.rightgrid_layout_22=QHBoxLayout()
        # 设置主窗口的布局层
        self.mainlayout_widget = QWidget()
        self.mainlayout_widget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainlayout_widget)

        # 对左侧frame进行布局
        # 左侧一共有六个组件
        #self.label_01 = QLabel()
        # label_01.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #self.contrast_Label = MyLabel("Contrast Ratio")
        #self.contrast_Label.setFrameShape(QFrame.Box)

        #self.label_02 = MyLabel("Section Information")
        #self.label_02.setFrameShape(QFrame.Box)
        # label_02.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.label_03 = MyLabel("X:")
        #self.label_03.setFrameShape(QFrame.Box)
        # label_03.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.label_04 = MyLabel("Y:")
        #self.label_04.setFrameShape(QFrame.Box)
        # label_04.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.label_05 = MyLabel("Z:")
        #self.label_05.setFrameShape(QFrame.Box)
        # label_05.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.label_06 = MyLabel("Gray Value:")
        #self.label_06.setFrameShape(QFrame.Box)
        #self.button_01=QPushButton("3DSeg",self)
        #self.button_01.clicked.connect(self.ThreeDGrowSegment)

        #对画笔和橡皮进行布局
        #self.drawToolFrame=QFrame()
        #self.drawToolFrame.setFrameShape(QFrame.Box)
        #self.drawLayout=QVBoxLayout()
        #self.drawLayout_1=QVBoxLayout()
        #self.drawLayout_2=QHBoxLayout()
        #self.drawLayout_21=QVBoxLayout()
        #self.drawLayout_22=QVBoxLayout()
        #self.drawToolFrame.setLayout(self.drawLayout)
        #self.drawLayout.addLayout(self.drawLayout_1)
        #self.drawLayout.addLayout(self.drawLayout_2)
        #self.drawLayout.setStretchFactor(self.drawLayout_1,2)
        #self.drawLayout.setStretchFactor(self.drawLayout_2,1)
        #self.drawLayout_2.addLayout(self.drawLayout_21)
        #self.drawLayout_2.addLayout(self.drawLayout_22)

        #self.eraseFrame=QFrame()
        #self.eraseFrame.setFrameShape(QFrame.Box)
        #self.eraseLayout=QVBoxLayout()
        #self.eraseFrame.setLayout(self.eraseLayout)

        #self.button_02 = QPushButton("Pen", self)
        #self.button_02.clicked.connect(self.MyPen)
        #self.button_03 = QPushButton("Rubber", self)
        #self.button_03.clicked.connect(self.MyRubber)
        #self.button_04 = QPushButton("vessel", self)
        #self.button_04.clicked.connect(self.MyVessel)
        #self.button_05 = QPushButton("clot", self)
        #self.button_05.clicked.connect(self.MyClot)
        # 对比度滑轮
        #self.contrast = ConstratSlider.ConstratQSlider()
        #self.contrast.setOrientation(Qt.Horizontal)
        #self.contrast.setSingleStep(1)
        #self.contrast.setMinimum(0)
        #self.contrast.setMaximum(99)
        #self.contrast.sliderMoved.connect(self.changeContrast)
        #笔滑轮
        #self.penSlider = ConstratSlider.ConstratQSlider()
        #self.penSlider.setOrientation(Qt.Horizontal)
        #self.penSlider.setSingleStep(1)
        #self.penSlider.setMinimum(1)
        #self.penSlider.setMaximum(10)
        #self.penSlider.sliderMoved.connect(self.changePen)
        #橡皮滑轮
        #self.rubberSlider = ConstratSlider.ConstratQSlider()
        #self.rubberSlider.setOrientation(Qt.Horizontal)
        #self.rubberSlider.setSingleStep(1)
        #self.rubberSlider.setMinimum(1)
        #self.rubberSlider.setMaximum(10)
        #self.rubberSlider.sliderMoved.connect(self.changeRubber)
        # label_06.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 创建对于左侧窗口的布局
        # leftgrid_layout=QGridLayout()
        #self.leftgrid_layout.addStretch(13)
        #self.leftgrid_layout.addWidget(self.drawToolFrame)
        # leftgrid_layout.addWidget(label_01,0,0)
        #self.leftgrid_layout.addWidget(self.button_02)
        #self.drawLayout_1.addWidget(self.button_02)
        #self.leftgrid_layout.addWidget(self.penSlider)
        #self.drawLayout_1.addWidget(self.penSlider)
        #self.leftgrid_layout.addWidget(self.button_04)
        #self.drawLayout_21.addWidget(self.button_04)
        #self.leftgrid_layout.addWidget(self.button_05)
        #self.drawLayout_22.addWidget(self.button_05)
        #self.drawLayout_2.setStretchFactor(self.drawLayout_21,1)
        #self.drawLayout_2.setStretchFactor(self.drawLayout_22,1)

        #self.leftgrid_layout.addWidget(self.eraseFrame)
        #self.eraseLayout.addWidget(self.button_03)
        #self.eraseLayout.addWidget(self.rubberSlider)
        

        #self.leftgrid_layout.addWidget(self.button_03)
        #self.leftgrid_layout.addWidget(self.rubberSlider)
        #self.leftgrid_layout.addWidget(self.contrast_Label)
        #self.leftgrid_layout.addWidget(self.contrast)
        #self.leftgrid_layout.addWidget(self.label_01)
        # leftgrid_layout.addWidget(label_02,1,0)
        #self.leftgrid_layout.addWidget(self.label_02)
        # leftgrid_layout.addWidget(label_03,2,0)
        #self.leftgrid_layout.addWidget(self.label_03)
        # leftgrid_layout.addWidget(label_04,3,0)
        #self.leftgrid_layout.addWidget(self.label_04)
        # leftgrid_layout.addWidget(label_05,4,0)
        #self.leftgrid_layout.addWidget(self.label_05)
        # leftgrid_layout.addWidget(label_06,5,0)
        #self.leftgrid_layout.addWidget(self.label_06)
        #self.leftgrid_layout.addWidget(self.button_01)
        #self.leftgrid_layout.addStretch(13)
        # 对右侧进行布局,两个布局分别放置四个组件
        # 对滑块设置大小
        #self.graph_01 = MyLabel(text='',connect=[self.label_03,self.label_04],number=self.number)
        self.graph_01=QLabel()
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
        #self.graph_02 = MyLabel(text='',connect=[self.label_03,self.label_04],number=self.number)
        self.graph_02=QLabel()
        self.graph_02.setGeometry(840, 300, 480, 480)
        self.graph_02.setFrameShape(QFrame.Box)
        #self.scroll_02 = NewQslider.MyQSlider()
        self.scroll_02=NewQslider.MyQSlider()
        self.scroll_02.setOrientation(Qt.Vertical)
        self.scroll_02.setSingleStep(1)
        self.scroll_02.setMinimum(1)
        self.scroll_02.sliderMoved.connect(self.sliderMoved_02)

        #self.graph_03 = MyLabel(text='',connect=[self.label_03,self.label_04],number=self.number)
        self.graph_03=QLabel()
        self.graph_03.setGeometry(840, 780, 480, 480)
        self.graph_03.setFrameShape(QFrame.Box)
        #self.scroll_03 = NewQslider.MyQSlider()
        self.scroll_03=NewQslider.MyQSlider()
        self.scroll_03.setOrientation(Qt.Vertical)
        self.scroll_03.setSingleStep(1)
        self.scroll_03.setMinimum(1)
        self.scroll_03.sliderMoved.connect(self.sliderMoved_03)
        self.frame3D, self.vtkWidget3D=createModel.model(self.fp,self.pr)
        #thread=ModelThread(createModel.model,(self.fp,self.slices))
        #thread.start()
        #thread.join()
        #modelFrame=thread.get_result()

        self.rightgrid_layout_1.addWidget(self.graph_01)
        self.rightgrid_layout_1.addWidget(self.scroll_01)
        self.rightgrid_layout_1.addWidget(self.graph_02)
        self.rightgrid_layout_1.addWidget(self.scroll_02)
        #在布局中加入vtk体绘制窗口
        #rightgrid_layout_21.addWidget(self.vtkWidget)
        self.rightgrid_layout_21.addWidget(self.frame3D)
        self.rightgrid_layout_22.addWidget(self.graph_03)
        self.rightgrid_layout_22.addWidget(self.scroll_03)
        #rightgrid_layout_2.addWidget(self.graph_04)
        #rightgrid_layout_2.addWidget(self.scroll_04)
        #rightgrid_layout_21.addWidget(self.vtkWidget)



        #self.mainLayout.addLayout(self.leftgrid_layout)
        self.mainLayout.addLayout(self.rightgrid_layout)
        self.rightgrid_layout.addLayout(self.rightgrid_layout_1)
        self.rightgrid_layout.addLayout(self.rightgrid_layout_2)
        self.rightgrid_layout_2.addLayout(self.rightgrid_layout_21)
        self.rightgrid_layout_2.addLayout(self.rightgrid_layout_22)
        # 设置布局管理器比例系数
        self.rightgrid_layout_2.setStretchFactor(self.rightgrid_layout_21,1)
        self.rightgrid_layout_2.setStretchFactor(self.rightgrid_layout_22,1)
        #self.mainLayout.setStretchFactor(self.leftgrid_layout, 1)
        #self.mainLayout.setStretchFactor(self.rightgrid_layout, 4)

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
        #self.fp = QFileDialog.getOpenFileName()
        # print(self.fp[0])
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
        self.number = self.scroll_01.value()
        img = cv2.resize(src=self.slices[value - 1, :, :], dsize=None, fx=1, fy=1)
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 将nparray转化成QImage对象显示在QLabel中
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        self.pixmap_imgSrc_1 = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        return self.pixmap_imgSrc_1

    def setInitGraph_02(self, value):
        self.number_2 = self.scroll_02.value()
        print(self.slices.shape)
        #img = img.astype(np.uint8)
        img = cv2.resize(src=self.slices[:, :, value - 1], dsize=None, fx=1, fy=1)
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 将nparray转化成QImage对象显示在QLabel中
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        self.pixmap_imgSrc_2 = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        return self.pixmap_imgSrc_2

    def setInitGraph_03(self, value):
        self.number_3 = self.scroll_03.value()
        print(self.slices.shape)
        #img = img.astype(np.uint8)
        img = cv2.resize(src=self.slices[:, value - 1, :], dsize=None, fx=1, fy=1)
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 将nparray转化成QImage对象显示在QLabel中
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        self.pixmap_imgSrc_3 = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        return self.pixmap_imgSrc_3

    def changeContrast(self):
        self.contrVal=1-self.contrast.value()*0.01
        img = abs(self.slices[self.number - 1, :, :] )/ 255
        img = (pow(img, self.contrVal) * 255).astype(np.uint8)  # 转换为0--255的灰度uint8类型
        self.refeshGraph_01(img)
        img = abs(self.slices[:, :, self.number_2] )/ 255
        img = (pow(img, self.contrVal) * 255).astype(np.uint8)  # 转换为0--255的灰度uint8类型
        self.refeshGraph_02(img)
        img = abs(self.slices[:, self.number_3, :] )/ 255
        img = (pow(img, self.contrVal) * 255).astype(np.uint8)  # 转换为0--255的灰度uint8类型
        self.refeshGraph_03(img)

    def changePen(self):
        self.penSize=self.penSlider.value()-1
        print("PenSizeValue",self.penSlider.value())
        print("Pensize",self.penSize)

    def changeRubber(self):
        self.rubberSize=self.rubberSlider.value()-1
        
    def refeshGraph_01(self,img):
        try:
            img = cv2.resize(src=img, dsize=None, fx=1, fy=1)
        except:
            print("IndexError")

        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img2[np.where((img2 == [255, 255, 255]).all(axis=2))] = [255, 0, 0]
        img2[np.where((img2 == [254, 254, 254]).all(axis=2))] = [0, 255, 0]


        # 将nparray转化成QImage对象显示在QLabel中
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        self.pixmap_imgSrc_1 = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        self.graph_01.setPixmap(self.pixmap_imgSrc_1)
        # 图片在label中居中显示
        self.graph_01.setAlignment(Qt.AlignCenter)
        self.graph_01.setScaledContents(False)

    def refeshGraph_02(self,img):
        try:
            img = cv2.resize(src=img, dsize=None, fx=1, fy=1)
        except:
            print("IndexError")
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img2[np.where((img2 == [255, 255, 255]).all(axis=2))] = [255, 0, 0]
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        self.pixmap_imgSrc_2 = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        self.graph_02.setPixmap(self.pixmap_imgSrc_2)
        self.graph_02.setAlignment(Qt.AlignCenter)
        self.graph_02.setScaledContents(False)

    def refeshGraph_03(self,img):
        try:
            img = cv2.resize(src=img, dsize=None, fx=1, fy=1)
        except:
            print("IndexError")
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img2[np.where((img2 == [255, 255, 255]).all(axis=2))] = [255, 0, 0]
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        self.pixmap_imgSrc_3 = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        self.graph_03.setPixmap(self.pixmap_imgSrc_3)
        self.graph_03.setAlignment(Qt.AlignCenter)
        self.graph_03.setScaledContents(False)

    def sliderMoved_01(self):
        self.number = self.scroll_01.value()
        img = abs(self.slices[self.number - 1, :, :] )/ 255
        img = (pow(img, self.contrVal) * 255).astype(np.uint8)  # 转换为0--255的灰度uint8类型
        self.refeshGraph_01(img)


    def sliderMoved_02(self):
        self.number_2 = self.scroll_02.value()
        img = abs(self.slices[:, :, self.number_2 - 1] )/ 255
        img = (pow(img, self.contrVal) * 255).astype(np.uint8)  # 转换为0--255的灰度uint8类型
        self.refeshGraph_02(img)


    def sliderMoved_03(self):
        self.number_3 = self.scroll_03.value()
        img = abs(self.slices[:,self.number_3 - 1,:] )/ 255
        img = (pow(img, self.contrVal) * 255).astype(np.uint8)  # 转换为0--255的灰度uint8类型
        self.refeshGraph_03(img)


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
        if event.buttons() == QtCore.Qt.LeftButton:
            self.number=self.scroll_01.value()
            self.label_05.setText("Z: " + str(self.number))
            self.grayValue=self.slices[self.number - 1,self.graph_01.yPosition, self.graph_01.xPosition]
            self.label_06.setText("Gray Value: "+str(self.grayValue))
            self.xPosition=self.graph_01.xPosition
            self.yPosition=self.graph_01.yPosition
            if (self.PenFlag):
                print(self.PenFlag)
                if(self.penSize==0):
                    if(self.VesselFlag):
                        self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition] = 255
                    else:
                        self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition] = 254
                else:
                    for i in range(-self.penSize, self.penSize):
                        for j in range(-self.penSize, self.penSize):
                            if(self.VesselFlag):
                                self.slices[self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j] = 255
                            elif(self.ClotFlag):
                                self.slices[
                                    self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j] = 254
                img=self.slices[self.number - 1, :, :]
                self.refeshGraph_01(img)
            if (self.RubberFlag):

                if(self.rubberSize==0):
                    self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition] \
                        = self.slicesRGB[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition]
                else:
                    for i in range(-self.rubberSize,self.rubberSize):
                        for j in range(-self.rubberSize,self.rubberSize):
                            self.slices[self.number - 1, self.graph_01.yPosition+i, self.graph_01.xPosition+j] =\
                                self.slicesRGB[self.number - 1, self.graph_01.yPosition+i, self.graph_01.xPosition+j]
                img = self.slices[self.number - 1, :, :]
                self.refeshGraph_01(img)

    # 鼠标单击事件
    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.number = self.scroll_01.value()
            self.label_05.setText("Z: " + str(self.number))
            self.grayValue = self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition]
            self.label_06.setText("Gray Value: " + str(self.grayValue))
            self.xPosition = self.graph_01.xPosition
            self.yPosition = self.graph_01.yPosition
            if (self.PenFlag):
                print(self.PenFlag)
                if (self.penSize == 0):
                    if (self.VesselFlag):
                        self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition] = 255
                    else:
                        self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition] = 254
                else:
                    for i in range(-self.penSize, self.penSize):
                        for j in range(-self.penSize, self.penSize):
                            if (self.VesselFlag):
                                self.slices[
                                    self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j] = 255
                            elif (self.ClotFlag):
                                self.slices[
                                    self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j] = 254
                img = self.slices[self.number - 1, :, :]
                self.refeshGraph_01(img)
            if (self.RubberFlag):

                if (self.rubberSize == 0):
                    self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition] \
                        = self.slicesRGB[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition]
                else:
                    for i in range(-self.rubberSize, self.rubberSize):
                        for j in range(-self.rubberSize, self.rubberSize):
                            self.slices[self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j] = \
                                self.slicesRGB[
                                    self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j]
                img = self.slices[self.number - 1, :, :]
                self.refeshGraph_01(img)




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

    def MyPen(self):
        if (self.PenFlag):
            self.setCursor(Qt.ArrowCursor)
            self.PenFlag = False
            self.RubberFlag = False
        else:
            self.setCursor(Qt.CrossCursor)
            self.PenFlag=True
            self.RubberFlag=False

    def MyRubber(self):
        if(self.RubberFlag):
            self.setCursor(Qt.ArrowCursor)
            self.PenFlag = False
            self.RubberFlag = False
        else:
            self.setCursor(Qt.IBeamCursor)
            self.RubberFlag = True
            self.PenFlag=False

    def MyVessel(self):
        self.VesselFlag=True
        self.ClotFlag = False

    def MyClot(self):
        self.ClotFlag=True
        self.VesselFlag = False


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
        #删除控件并更新
        self.vtkWidget3D.Finalize()
        self.rightgrid_layout_21.removeWidget(self.frame3D)
        sip.delete(self.frame3D)
        self.frame3DTwo, self.vtkWidget3DTwo=createModel.model(self.fp,self.slices)
        self.rightgrid_layout_21.addWidget(self.frame3DTwo)
        self.vtkWidget3DTwo.Finalize()

    #确定关闭窗口后的事件，将vtk删除干净，否则会出现句柄无效的错误
    def closeEvent(self, event):
        self.vtkWidget3D.Finalize()
        #self.vtkWidget3DTwo.Finalize()
