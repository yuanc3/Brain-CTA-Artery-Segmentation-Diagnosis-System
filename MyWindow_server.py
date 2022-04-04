import base64
import os
from seg_ico import imglogo
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow,QLabel,QVBoxLayout,QWidget,QHBoxLayout,QPushButton,QFrame,QApplication,QDesktopWidget,QAction,QMessageBox,QFileDialog
from PyQt5.QtGui import QImage,QPixmap,QIcon
from numpy import where,uint8,int16,float32,int64,zeros,stack,reshape,frombuffer,array,pad
from PIL import Image
from SimpleITK import ReadImage,GetArrayFromImage,GetImageFromArray,WriteImage
from copy import deepcopy
import NewQslider
import ConstratSlider
from cv2 import resize,cvtColor,COLOR_BGR2RGB
from MyLabel import MyLabel
from ScreenShot import WScreenShot
import createModel
import socket
from pickle import loads
import ClotDetect
import VesselDetect
import socket
import DrawWindow
import ProcessWindow

from time import time,sleep
import jumpWindow
import threeDGrowSeg
import PDFPreviewWindow
import sip



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
        self.contrVal = 1
        self.numberOfScreen = 0
        self.initUI()
        self.PenFlag = False
        self.RubberFlag = False
        self.VesselFlag = True
        self.ClotFlag = False
        self.vtkFlag = False
        self.reportNeedChange = True
        self.clotReportNeedChange = True
        self.vesselReportNeedChange = True
        self.labelFalg = False  # 如果是标签就将此值设为True
        self.windowUpdate = True
        self.openFileNumber = 0

    def initUI(self, slices=zeros((1, 512, 512))):
        self.slices = slices
        self.number = 0
        self.yPosition = 0
        self.xPosition = 0
        # 创建File下的选项以及点击的触发事件
        openFile = QAction('Open File', self)
        openFile.triggered.connect(self.open_file)
        # openFolder = QAction('Open Folder', self)
        # openFolder.triggered.connect(self.open_folder)
        self.saveMenu = QAction('Save', self)
        self.saveMenu.setEnabled(False)
        self.saveMenu.triggered.connect(self.save)
        # 创建菜单栏，附加一个名为File的菜单
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        # fileMenu.addAction(openFolder)
        fileMenu.addAction(self.saveMenu)
        # 创建菜单栏其他选项下的选项
        # copy = QAction('Copy', self)
        # delete = QAction('Delete', self)
        self.DLSegment = QAction('Deep learning Segment', self)
        self.DLSegment.setEnabled(False)
        self.DLSegment.triggered.connect(self.deepLearning_segment)
        self.ThreeD = QAction('Traditional 3D Segment', self)
        self.ThreeD.setEnabled(False)
        self.ThreeD.triggered.connect(self.ThreeDGrowSegment)
        self.Drawing = QAction('Drawing', self)
        self.Drawing.setEnabled(False)
        self.Drawing.triggered.connect(self.drawNewWin)
        self.ClotDetection = QAction('Generate Report', self)
        self.ClotDetection.setEnabled(False)
        self.ClotDetection.triggered.connect(self.DoOneAll)
        # self.ClotDetection.triggered.connect(self.DoOneClot)
        # self.VesselDetection=QAction('Generate Vessel Report', self)
        # self.VesselDetection.setEnabled(False)
        # self.VesselDetection.triggered.connect(self.DoOneVessel)
        # self.AllDetection=QAction('Generate Complete Report', self)
        # self.AllDetection.setEnabled(False)
        # self.AllDetection.triggered.connect(self.DoOneAll)
        # ThreeDRGSegment = QAction('3D RG Segment', self)
        # ThreeDRGSegment.triggered.connect(self.RG_3D_Segment)
        # 创建菜单栏的其他选项
        # viewMenu = menubar.addMenu('&View')
        exitMenu = menubar.addMenu('&Edit')
        exitMenu.addAction(self.Drawing)
        exitMenu.addAction(self.ClotDetection)
        # exitMenu.addAction(self.VesselDetection)
        # exitMenu.addAction(self.AllDetection)
        # exitMenu.addAction(delete)
        segmentMenu = menubar.addMenu('&Segment')
        segmentMenu.addAction(self.DLSegment)
        segmentMenu.addAction(self.ThreeD)
        # segmentMenu.addAction(ThreeDRGSegment)

        self.aboutUsWindow = QAction('About Us', self)
        self.aboutUsWindow.triggered.connect(self.aboutUs)
        # self.contactUsWindow = QAction('Contact Us', self)
        # self.contactUsWindow.triggered.connect(self.contactUs)
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(self.aboutUsWindow)
        # helpMenu.addAction(self.contactUsWindow)
        # self.aboutUsWindow = QAction('About Us', self)
        # self.aboutUsWindow.triggered.connect(self.aboutUs)
        # self.contactUsWindow = QAction('Contact Us', self)
        # self.contactUsWindow.triggered.connect(self.contactUs)

        self.setGeometry(200, 300, 800, 600)
        tmp = open('in.ico', 'wb')
        tmp.write(base64.b64decode(imglogo))
        tmp.close()
        self.setWindowIcon(QIcon("in.ico"))
        os.remove('in.ico')
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.windowName = "Brain CTA Artery Segmentation & Diagnosis System"
        self.setWindowTitle(self.windowName)
        # 使窗口居中
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(int(newLeft), int(newTop))
        self.show()

    def aboutUs(self):

        # self.aboutWindow=QWidget()
        aboutStr = "Development Completion Date: 2022/3/22" + "\n" + "Developer: Yuan chao, Wang yanbo, Zhao xinchen" + "\n" + "If you have any questions,please contact us through 19722073@bjtu.edu.cn"
        msg_box = QMessageBox(QMessageBox.Information, 'About Us', aboutStr)
        msg_box.exec_()

    # def contactUs(self):
    #     print("contactUs")

    def myGrid(self):

        # 定义顶级布局管理器
        self.mainLayout = QHBoxLayout()
        # 定义左侧布局管理器
        self.leftgrid_layout = QVBoxLayout()
        # 定义右侧布局管理器
        self.rightgrid_layout = QVBoxLayout()
        # 对右侧布局进行再次布局
        self.rightgrid_layout_1 = QHBoxLayout()
        self.rightgrid_layout_2 = QHBoxLayout()
        # 对右下侧布局进行再次布局
        self.rightgrid_layout_21 = QHBoxLayout()
        self.rightgrid_layout_22 = QHBoxLayout()
        # 设置主窗口的布局层
        self.mainlayout_widget = QWidget()
        self.mainlayout_widget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainlayout_widget)

        # 对左侧frame进行布局
        # 左侧一共有六个组件
        self.label_01 = QLabel()
        # label_01.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.contrast_Label = MyLabel("Contrast Ratio")
        self.contrast_Label.setFrameShape(QFrame.Box)

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
        self.button_01 = QPushButton("ScreenShot", self)
        self.button_01.setEnabled(False)
        self.button_01.clicked.connect(self.screenShotFun)
        self.vtkButton = QPushButton("Change VTK Mode", self)
        self.vtkButton.clicked.connect(self.vtkDeal)

        # 对比度滑轮
        self.contrast = ConstratSlider.ConstratQSlider()
        self.contrast.setOrientation(Qt.Horizontal)
        self.contrast.setSingleStep(1)
        self.contrast.setMinimum(0)
        self.contrast.setMaximum(99)
        self.contrast.sliderMoved.connect(self.changeContrast)

        # 创建对于左侧窗口的布局
        # leftgrid_layout=QGridLayout()
        self.leftgrid_layout.addStretch(13)

        self.leftgrid_layout.addWidget(self.contrast_Label)
        self.leftgrid_layout.addWidget(self.contrast)
        self.leftgrid_layout.addWidget(self.label_01)
        # leftgrid_layout.addWidget(label_02,1,0)
        self.leftgrid_layout.addWidget(self.label_02)
        # leftgrid_layout.addWidget(label_03,2,0)
        self.leftgrid_layout.addWidget(self.label_03)
        # leftgrid_layout.addWidget(label_04,3,0)
        self.leftgrid_layout.addWidget(self.label_04)
        # leftgrid_layout.addWidget(label_05,4,0)
        self.leftgrid_layout.addWidget(self.label_05)
        # leftgrid_layout.addWidget(label_06,5,0)
        self.leftgrid_layout.addWidget(self.label_06)
        self.leftgrid_layout.addWidget(self.button_01)
        self.leftgrid_layout.addWidget(self.vtkButton)
        self.leftgrid_layout.addStretch(13)
        # 对右侧进行布局,两个布局分别放置四个组件
        # 对滑块设置大小
        self.graph_01 = MyLabel(text='', connect=[self.label_03, self.label_04], IsClicked=False)
        # self.graph_01.setGeometry(360, 300, 450, 450)
        self.graph_01.setFixedSize(450, 450)
        self.graph_01.setFrameShape(QFrame.Box)
        self.graph_01_width = self.graph_01.width()
        self.graph_01_height = self.graph_01.height()
        # print("graph_01_width", self.graph_01_width)
        # print("graph_01_height", self.graph_01_height)

        # self.scroll_01 = NewQslider.MyQSlider()
        self.scroll_01 = NewQslider.MyQSlider()
        self.scroll_01.setOrientation(Qt.Vertical)
        # print(self.slices.shape)
        # self.scroll_01.setValue((int)((self.slices.shape[0])/2))
        # 设置步长
        self.scroll_01.setSingleStep(1)
        self.scroll_01.setMinimum(1)
        # 为label设置相应的初始图片
        # 当滑块移动的时候设置相应的事件
        self.scroll_01.valueChanged.connect(self.sliderMoved_01)
        self.graph_02 = MyLabel(text='', connect=[self.label_03, self.label_04], IsClicked=False)
        # self.graph_02.setGeometry(840, 300, 450, 450)
        self.graph_01.setFixedSize(450, 450)
        self.graph_02.setFrameShape(QFrame.Box)
        # self.scroll_02 = NewQslider.MyQSlider()
        self.scroll_02 = NewQslider.MyQSlider()
        self.scroll_02.setOrientation(Qt.Vertical)
        self.scroll_02.setSingleStep(1)
        self.scroll_02.setMinimum(1)
        self.scroll_02.valueChanged.connect(self.sliderMoved_02)

        self.graph_03 = MyLabel(text='', connect=[self.label_03, self.label_04], IsClicked=False)
        # self.graph_03.setGeometry(840, 780, 450, 450)
        self.graph_01.setFixedSize(450, 450)
        self.graph_03.setFrameShape(QFrame.Box)
        # self.scroll_03 = NewQslider.MyQSlider()
        self.scroll_03 = NewQslider.MyQSlider()
        self.scroll_03.setOrientation(Qt.Vertical)
        self.scroll_03.setSingleStep(1)
        self.scroll_03.setMinimum(1)
        self.scroll_03.valueChanged.connect(self.sliderMoved_03)
        self.frame3D, self.vtkWidget3D = createModel.model(self.fp, self.slices, self.vtkFlag, self.labelFalg)

        self.rightgrid_layout_1.addWidget(self.graph_01)
        self.rightgrid_layout_1.addWidget(self.scroll_01)
        self.rightgrid_layout_1.addWidget(self.graph_02)
        self.rightgrid_layout_1.addWidget(self.scroll_02)
        # 在布局中加入vtk体绘制窗口
        # rightgrid_layout_21.addWidget(self.vtkWidget)
        self.rightgrid_layout_21.addWidget(self.frame3D)
        self.rightgrid_layout_22.addWidget(self.graph_03)
        self.rightgrid_layout_22.addWidget(self.scroll_03)
        # rightgrid_layout_2.addWidget(self.graph_04)
        # rightgrid_layout_2.addWidget(self.scroll_04)
        # rightgrid_layout_21.addWidget(self.vtkWidget)

        self.mainLayout.addLayout(self.leftgrid_layout)
        self.mainLayout.addLayout(self.rightgrid_layout)
        self.rightgrid_layout.addLayout(self.rightgrid_layout_1)
        self.rightgrid_layout.addLayout(self.rightgrid_layout_2)
        self.rightgrid_layout_2.addLayout(self.rightgrid_layout_21)
        self.rightgrid_layout_2.addLayout(self.rightgrid_layout_22)
        # 设置布局管理器比例系数
        self.rightgrid_layout_2.setStretchFactor(self.rightgrid_layout_21, 1)
        self.rightgrid_layout_2.setStretchFactor(self.rightgrid_layout_22, 1)
        self.mainLayout.setStretchFactor(self.leftgrid_layout, 1)
        self.mainLayout.setStretchFactor(self.rightgrid_layout, 4)

        # 创建一个左侧窗口的窗口对象
        # leftlayout_widget = QWidget(leftFrame)
        # 设置左侧窗口的布局层
        # leftlayout_widget.setLayout(leftgrid_layout)
        # 设置窗口出现的位置以及窗口的宽和高

    def vtkDeal(self):
        if (self.vtkFlag == False):
            self.vtkFlag = True
        else:
            self.vtkFlag = False
        self.vtkWidget3D.Finalize()
        self.rightgrid_layout_21.removeWidget(self.frame3D)
        self.frame3D, self.vtkWidget3D = createModel.model(self.fp, self.slices, self.vtkFlag, self.labelFalg)
        self.frame3D.setFocusPolicy(Qt.NoFocus)
        self.rightgrid_layout_21.addWidget(self.frame3D)

    # 自定义函数
    def open_file(self):
        # 重新启用按钮
        self.saveMenu.setEnabled(True)
        self.DLSegment.setEnabled(True)
        # self.ClotDetection.setEnabled(True)
        # self.VesselDetection.setEnabled(True)
        # self.AllDetection.setEnabled(True)
        array = []
        # 获得选择好的文件
        # try:
        self.fp = QFileDialog.getOpenFileName()
        smallStr = ".nii"
        imageFlag = smallStr in self.fp[0]
        if imageFlag == False:
            return
        # print(self.fp[0])
        self.graphName = self.fp[0].split("/")
        self.length = len(self.graphName)
        self.openFileNumber += 1
        if self.openFileNumber > 1:
            self.Drawing.setEnabled(False)
            self.ClotDetection.setEnabled(False)
            print("OPEN")
            # print(self.openFileNumber)
            print(self.fp[0])
            if self.fp[0] != "":
                print("FP is not null")
                # print("MAKABAKA",self.fp[0])
                self.vtkWidget3D.Finalize()
                self.rightgrid_layout_21.removeWidget(self.frame3D)
        # print(self.fp[0])
        imgs = ReadImage(self.fp[0])
        TestDirection = (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0)
        img3D_array = GetArrayFromImage(imgs)
        # except:
        #     print("Error")
        #     self.windowUpdate = False
        #     return

        if imgs.GetDirection() == TestDirection:
            for i in range(len(img3D_array)):
                array.append(img3D_array[len(img3D_array) - i - 1, :, :])
            img3D_array = stack([s for s in array])
            global Label_Direction
            Label_Direction = 1
        img3D_array = self.preprocessing(img3D_array)
        self.open(img3D_array)
        self.move(450, 0)
        self.imageLength = self.slices.shape[0]
        # print(self.imageLength)
        self.scroll_01.setValue((int)((self.slices.shape[0]) / 2))
        # self.scroll_01.setValue(84)
        # print("Value",self.slices.shape[0])
        self.scroll_01.setMaximum(self.slices.shape[0])
        pixmap_imgSrc_01 = self.setInitGraph_01(self.scroll_01.value())
        self.graph_01.setPixmap(pixmap_imgSrc_01)
        self.graph_01.setAlignment(Qt.AlignCenter)
        # self.graph_01.setScaledContents(True)

        self.scroll_02.setValue((int)((self.slices.shape[1]) / 2))
        self.scroll_02.setMaximum(self.slices.shape[1])
        pixmap_imgSrc_02 = self.setInitGraph_02(self.scroll_02.value())
        self.graph_02.setPixmap(pixmap_imgSrc_02)
        self.graph_02.setAlignment(Qt.AlignCenter)
        # self.graph_02.setScaledContents(True)

        self.scroll_03.setValue((int)((self.slices.shape[2]) / 2))
        self.scroll_03.setMaximum(self.slices.shape[2])
        pixmap_imgSrc_03 = self.setInitGraph_03(self.scroll_03.value())
        self.graph_03.setPixmap(pixmap_imgSrc_03)
        self.graph_03.setAlignment(Qt.AlignCenter)
        # self.graph_03.setScaledContents(True)

    # except:
    #     print("Error")

    def open(self, img3D_array):
        self.reportNeedChange = True
        self.clotReportNeedChange = True
        self.vesselReportNeedChange = True
        self.setWindowTitle(self.windowName + "-" + self.graphName[self.length - 1])
        # 用lstFilesDCM作为存放DICOM files的列表
        # PathDicom = filePath #与python文件同一个目录下的文件夹
        self.slices = img3D_array
        # print(self.slices.shape)
        HHH = self.slices[len(self.slices) // 2 - 1].sum() / (512 * 512)
        if HHH < 6:
            adj = (6 - HHH) / 10.972
            self.slices = ((pow(abs(self.slices) / 255, 1 - adj) * 255)).astype(uint8)
        self.slices[self.slices > 220] = 220
        # 存一个slices的备份
        self.slices_Wang = self.slices
        self.slices_Yuan = self.slices
        # print("Open:", self.slices.shape)
        self.slicesRGB = deepcopy(self.slices)
        # if self.windowUpdate:
        self.myGrid()
        # else:
        #     return

    def preprocessing(self, img3D_array):
        # global img3D_array_
        image = img3D_array.copy()
        image = image.astype(int16)
        img3D_array_ = img3D_array.astype(float32)  # 把数据从 int32转为 float32类型
        img3D_array_ = (img3D_array - img3D_array.min()) / (img3D_array.max() - img3D_array.min())
        # 把数据范围变为0--1浮点,或许还有其他转换方法,效果能更好一些.
        img3D_array = (img3D_array_ * 255).astype(uint8)  # 转换为0--255的灰度uint8类型
        return img3D_array

    def open_folder(self):
        pass
        # print("Open Folder")
        # self.fp = QFileDialog.getExistingDirectory()  # 获得选择好的文件夹
        # array = []
        # for dirName, subdirList, fileList in walk(self.fp[0]):
        #     for filename in fileList:
        #         # if ".dcm" in filename.lower(): #判断文件是否为dicom文件
        #         # import SimpleITK as sitk
        #         # itk_img = sitk.ReadImage(os.path.join(dirName,filename))
        #         # img_array = sitk.GetArrayFromImage(itk_img)[0]
        #         array.append(read_file(path.join(dirName, filename)))
        # array.sort(key=lambda x: float(x.ImagePositionPatient[2]), reverse=True)
        # img3D_array = np.stack([s.pixel_array for s in array])
        # img3D_array = self.preprocessing(img3D_array)
        # self.open(img3D_array)

    # 返回加载在初始Label上的图片
    def setInitGraph_01(self, value):
        self.number = self.scroll_01.value()
        # print("Init Value", self.scroll_01.value())
        img = resize(src=self.slices[value - 1, :, :], dsize=None, fx=1, fy=1)
        img2 = cvtColor(img, COLOR_BGR2RGB)
        # 将nparray转化成QImage对象显示在QLabel中
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        self.pixmap_imgSrc_1 = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        return self.pixmap_imgSrc_1

    def setInitGraph_02(self, value):
        self.number_2 = self.scroll_02.value()
        # print(self.slices.shape)
        # img = img.astype(np.uint8)
        img = resize(src=self.slices[:, :, value - 1], dsize=None, fx=1, fy=1)
        img2 = cvtColor(img, COLOR_BGR2RGB)
        # 将nparray转化成QImage对象显示在QLabel中
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        self.pixmap_imgSrc_2 = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        return self.pixmap_imgSrc_2

    def setInitGraph_03(self, value):
        self.number_3 = self.scroll_03.value()
        # print(self.slices.shape)
        # img = img.astype(np.uint8)
        img = resize(src=self.slices[:, value - 1, :], dsize=None, fx=1, fy=1)
        img2 = cvtColor(img, COLOR_BGR2RGB)
        # 将nparray转化成QImage对象显示在QLabel中
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        self.pixmap_imgSrc_3 = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        return self.pixmap_imgSrc_3

    def refeshGraph_01(self, img):

        img = img.astype(uint8)  # 转换为0--255的灰度uint8类型
        try:
            img = resize(src=img, dsize=None, fx=1, fy=1)
        except:
            print("IndexError")
        # print(img.shape)
        img2 = cvtColor(img, COLOR_BGR2RGB)
        img2[where((img2 == [255, 255, 255]).all(axis=2))] = [255, 0, 0]
        img2[where((img2 == [254, 254, 254]).all(axis=2))] = [0, 255, 0]
        img2[where((img2 == [253, 253, 253]).all(axis=2))] = [152, 245, 255]

        # 将nparray转化成QImage对象显示在QLabel中
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        self.pixmap_imgSrc_1 = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        self.graph_01.setPixmap(self.pixmap_imgSrc_1)
        # 图片在label中居中显示
        self.graph_01.setAlignment(Qt.AlignCenter)
        self.graph_01.setScaledContents(False)

    def refeshGraph_02(self, img):
        img = img.astype(uint8)  # 转换为0--255的灰度uint8类型
        try:
            img = resize(src=img, dsize=None, fx=1, fy=1)
        except:
            print("IndexError")
        img2 = cvtColor(img, COLOR_BGR2RGB)
        img2[where((img2 == [255, 255, 255]).all(axis=2))] = [255, 0, 0]
        img2[where((img2 == [254, 254, 254]).all(axis=2))] = [0, 255, 0]
        img2[where((img2 == [253, 253, 253]).all(axis=2))] = [152, 245, 255]
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        self.pixmap_imgSrc_2 = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        self.graph_02.setPixmap(self.pixmap_imgSrc_2)
        self.graph_02.setAlignment(Qt.AlignCenter)
        self.graph_02.setScaledContents(False)

    def refeshGraph_03(self, img):
        img = img.astype(uint8)  # 转换为0--255的灰度uint8类型
        try:
            img = resize(src=img, dsize=None, fx=1, fy=1)
        except:
            print("IndexError")
        img2 = cvtColor(img, COLOR_BGR2RGB)
        img2[where((img2 == [255, 255, 255]).all(axis=2))] = [255, 0, 0]
        img2[where((img2 == [254, 254, 254]).all(axis=2))] = [0, 255, 0]
        img2[where((img2 == [253, 253, 253]).all(axis=2))] = [152, 245, 255]
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        self.pixmap_imgSrc_3 = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        self.graph_03.setPixmap(self.pixmap_imgSrc_3)
        self.graph_03.setAlignment(Qt.AlignCenter)
        self.graph_03.setScaledContents(False)

    def sliderMoved_01(self):
        self.number = self.scroll_01.getSlicesNumber()
        # self.number=self.scroll_01.value()
        img = abs(self.slices[self.number - 1, :, :]) / 255
        # img = abs(self.slices[self.imageLength-self.number, :, :]) / 255
        img = (pow(img, self.contrVal) * 255)
        self.refeshGraph_01(img)

    def sliderMoved_02(self):
        # print("Slider 2 has moved")
        self.number_2 = self.scroll_02.getSlicesNumber()
        img = abs(self.slices[:, :, self.number_2 - 1]) / 255
        img = (pow(img, self.contrVal) * 255)
        self.refeshGraph_02(img)

    def sliderMoved_03(self):
        self.number_3 = self.scroll_03.getSlicesNumber()
        img = abs(self.slices[:, self.number_3 - 1, :]) / 255
        img = (pow(img, self.contrVal) * 255).astype(uint8)
        self.refeshGraph_03(img)

    # 定义鼠标事件

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        try:
            if event.buttons() == Qt.LeftButton:
                try:
                    self.slices = deepcopy(self.Pre_slices)
                except:
                    pass

                self.Pre_slices = deepcopy(self.slices)

                if (self.graph_01.IsClicked and self.graph_02.IsClicked == False and self.graph_03.IsClicked == False):
                    self.graph_01.setIsClicked(False)

                    self.number = self.scroll_01.value()
                    ###################
                    self.number_2 = round(len(self.slices[0, 0]) * (self.graph_01.xPosition / 512))
                    self.number_3 = round(len(self.slices[0, 0]) * (self.graph_01.yPosition / 512))

                    self.label_03.setText("X: " + str(self.graph_01.xPosition))
                    self.label_04.setText("Y: " + str(self.graph_01.yPosition))
                    ###################
                    self.label_05.setText("Z: " + str(self.number))
                    self.grayValue = self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition]
                    self.label_06.setText("Gray Value: " + str(self.grayValue))
                    self.xPosition = self.graph_01.xPosition
                    self.yPosition = self.graph_01.yPosition

                    try:
                        self.slices[self.number - 1, :, self.graph_01.xPosition] = 253
                        self.slices[self.number - 1, :, self.graph_01.xPosition - 1] = 253
                        self.slices[self.number - 1, self.graph_01.yPosition, :] = 253
                        self.slices[self.number - 1, self.graph_01.yPosition - 1, :] = 253
                        self.slices[:, self.number_3 - 1, self.number_2 - 1] = 253
                        self.slices[:, self.number_3, self.number_2 - 1] = 253
                        self.slices[:, self.number_3 - 1, self.number_2] = 253
                    except:
                        pass

                    self.refeshGraph_01(self.slices[self.number - 1, :, :])
                    self.refeshGraph_02(self.slices[:, :, self.number_2 - 1])
                    self.refeshGraph_03(self.slices[:, self.number_3 - 1, :])
                    self.scroll_02.setValue(self.number_2)
                    self.scroll_03.setValue(self.number_3)
                    self.ThreeD.setEnabled(True)
                if (self.graph_01.IsClicked == False and self.graph_02.IsClicked and self.graph_03.IsClicked == False):
                    self.graph_02.setIsClicked(False)
                    self.number = round(len(self.slices) * (self.graph_02.yPosition / 512))
                    self.number_3 = round(len(self.slices[0, 0]) * (self.graph_02.xPosition / 512))
                    self.label_03.setText("X: " + str(self.number_2))
                    self.label_04.setText("Y: " + str(self.graph_02.xPosition))
                    self.label_05.setText("Z: " + str(self.number))
                    self.grayValue = self.slices[self.number - 1, self.graph_02.xPosition, self.number_2 - 1]
                    self.label_06.setText("Gray Value: " + str(self.grayValue))

                    self.Pre_slices = deepcopy(self.slices)
                    try:
                        self.slices[self.number - 1, :, self.number_2] = 253
                        self.slices[self.number - 1, :, self.number_2 - 1] = 253
                        self.slices[self.number - 1, self.graph_02.xPosition, :] = 253
                        self.slices[self.number - 1, self.graph_02.xPosition - 1, :] = 253
                        self.slices[:, self.number_3 - 1, self.number_2 - 1] = 253
                        self.slices[:, self.number_3, self.number_2 - 1] = 253
                        self.slices[:, self.number_3 - 1, self.number_2] = 253
                    except:
                        pass

                    self.refeshGraph_01(self.slices[self.number - 1, :, :])
                    self.refeshGraph_02(self.slices[:, :, self.number_2 - 1])
                    self.refeshGraph_03(self.slices[:, self.number_3 - 1, :])
                    self.scroll_01.setValue(self.number)
                    self.scroll_03.setValue(self.number_3)
                    self.ThreeD.setEnabled(True)

                if (self.graph_01.IsClicked == False and self.graph_02.IsClicked == False and self.graph_03.IsClicked):
                    self.graph_03.setIsClicked(False)
                    self.number = round(len(self.slices) * (self.graph_03.yPosition / 512))
                    self.number_2 = round(len(self.slices[0, 0]) * (self.graph_03.xPosition / 512))
                    self.label_03.setText("X: " + str(self.graph_03.xPosition))
                    self.label_04.setText("Y: " + str(self.number_3))
                    self.label_05.setText("Z: " + str(self.number))
                    self.grayValue = self.slices[self.number - 1,
                                                 self.number_3 - 1, self.graph_03.xPosition]
                    self.label_06.setText("Gray Value: " + str(self.grayValue))
                    self.Pre_slices = deepcopy(self.slices)
                    try:
                        self.slices[self.number - 1, :, self.graph_03.xPosition] = 253
                        self.slices[self.number - 1, :, self.graph_03.xPosition - 1] = 253
                        self.slices[self.number - 1, self.number_3, :] = 253
                        self.slices[self.number - 1, self.number_3 - 1, :] = 253
                        self.slices[:, self.number_3 - 1, self.number_2 - 1] = 253
                        self.slices[:, self.number_3, self.number_2 - 1] = 253
                        self.slices[:, self.number_3 - 1, self.number_2] = 253
                    except:
                        pass
                    self.refeshGraph_01(self.slices[self.number - 1, :, :])
                    self.refeshGraph_02(self.slices[:, :, self.number_2 - 1])
                    self.refeshGraph_03(self.slices[:, self.number_3 - 1, :])
                    self.scroll_01.setValue(self.number)
                    self.scroll_02.setValue(self.number_2)
                    self.ThreeD.setEnabled(True)

        except:
            pass

    # 鼠标单击事件
    def mousePressEvent(self, event):
        try:
            if event.buttons() == Qt.LeftButton:
                try:
                    self.slices = deepcopy(self.Pre_slices)
                except:
                    pass

                self.Pre_slices = deepcopy(self.slices)

                if (self.graph_01.IsClicked and self.graph_02.IsClicked == False and self.graph_03.IsClicked == False):
                    self.graph_01.setIsClicked(False)

                    self.number = self.scroll_01.value()
                    ###################
                    self.number_2 = round(len(self.slices[0, 0]) * (self.graph_01.xPosition / 512))
                    self.number_3 = round(len(self.slices[0, 0]) * (self.graph_01.yPosition / 512))

                    self.label_03.setText("X: " + str(self.graph_01.xPosition))
                    self.label_04.setText("Y: " + str(self.graph_01.yPosition))
                    ###################
                    self.label_05.setText("Z: " + str(self.number))
                    self.grayValue = self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition]
                    self.label_06.setText("Gray Value: " + str(self.grayValue))
                    self.xPosition = self.graph_01.xPosition
                    self.yPosition = self.graph_01.yPosition

                    try:
                        self.slices[self.number - 1, :, self.graph_01.xPosition] = 253
                        self.slices[self.number - 1, :, self.graph_01.xPosition - 1] = 253
                        self.slices[self.number - 1, self.graph_01.yPosition, :] = 253
                        self.slices[self.number - 1, self.graph_01.yPosition - 1, :] = 253
                        self.slices[:, self.number_3 - 1, self.number_2 - 1] = 253
                        self.slices[:, self.number_3, self.number_2 - 1] = 253
                        self.slices[:, self.number_3 - 1, self.number_2] = 253
                    except:
                        pass

                    self.refeshGraph_01(self.slices[self.number - 1, :, :])
                    self.refeshGraph_02(self.slices[:, :, self.number_2 - 1])
                    self.refeshGraph_03(self.slices[:, self.number_3 - 1, :])
                    self.scroll_02.setValue(self.number_2)
                    self.scroll_03.setValue(self.number_3)
                    self.ThreeD.setEnabled(True)
                if (self.graph_01.IsClicked == False and self.graph_02.IsClicked and self.graph_03.IsClicked == False):
                    self.graph_02.setIsClicked(False)
                    self.number = round(len(self.slices) * (self.graph_02.yPosition / 512))
                    self.number_3 = round(len(self.slices[0, 0]) * (self.graph_02.xPosition / 512))
                    self.label_03.setText("X: " + str(self.number_2))
                    self.label_04.setText("Y: " + str(self.graph_02.xPosition))
                    self.label_05.setText("Z: " + str(self.number))
                    self.grayValue = self.slices[self.number - 1, self.graph_02.xPosition, self.number_2 - 1]
                    self.label_06.setText("Gray Value: " + str(self.grayValue))

                    self.Pre_slices = deepcopy(self.slices)
                    try:
                        self.slices[self.number - 1, :, self.number_2] = 253
                        self.slices[self.number - 1, :, self.number_2 - 1] = 253
                        self.slices[self.number - 1, self.graph_02.xPosition, :] = 253
                        self.slices[self.number - 1, self.graph_02.xPosition - 1, :] = 253
                        self.slices[:, self.number_3 - 1, self.number_2 - 1] = 253
                        self.slices[:, self.number_3, self.number_2 - 1] = 253
                        self.slices[:, self.number_3 - 1, self.number_2] = 253
                    except:
                        pass

                    self.refeshGraph_01(self.slices[self.number - 1, :, :])
                    self.refeshGraph_02(self.slices[:, :, self.number_2 - 1])
                    self.refeshGraph_03(self.slices[:, self.number_3 - 1, :])
                    self.scroll_01.setValue(self.number)
                    self.scroll_03.setValue(self.number_3)
                    self.ThreeD.setEnabled(True)

                if (self.graph_01.IsClicked == False and self.graph_02.IsClicked == False and self.graph_03.IsClicked):
                    self.graph_03.setIsClicked(False)
                    self.number = round(len(self.slices) * (self.graph_03.yPosition / 512))
                    self.number_2 = round(len(self.slices[0, 0]) * (self.graph_03.xPosition / 512))
                    self.label_03.setText("X: " + str(self.graph_03.xPosition))
                    self.label_04.setText("Y: " + str(self.number_3))
                    self.label_05.setText("Z: " + str(self.number))
                    self.grayValue = self.slices[self.number - 1,
                                                 self.number_3 - 1, self.graph_03.xPosition]
                    self.label_06.setText("Gray Value: " + str(self.grayValue))
                    self.Pre_slices = deepcopy(self.slices)
                    try:
                        self.slices[self.number - 1, :, self.graph_03.xPosition] = 253
                        self.slices[self.number - 1, :, self.graph_03.xPosition - 1] = 253
                        self.slices[self.number - 1, self.number_3, :] = 253
                        self.slices[self.number - 1, self.number_3 - 1, :] = 253
                        self.slices[:, self.number_3 - 1, self.number_2 - 1] = 253
                        self.slices[:, self.number_3, self.number_2 - 1] = 253
                        self.slices[:, self.number_3 - 1, self.number_2] = 253
                    except:
                        pass
                    self.refeshGraph_01(self.slices[self.number - 1, :, :])
                    self.refeshGraph_02(self.slices[:, :, self.number_2 - 1])
                    self.refeshGraph_03(self.slices[:, self.number_3 - 1, :])
                    self.scroll_01.setValue(self.number)
                    self.scroll_02.setValue(self.number_2)
                    self.ThreeD.setEnabled(True)
        except:
            pass

    def mouseReleaseEvent(self, event):
        try:
            self.slices = deepcopy(self.Pre_slices)
            self.refeshGraph_01(self.slices[self.number - 1, :, :])
            self.refeshGraph_02(self.slices[:, :, self.number_2 - 1])
            self.refeshGraph_03(self.slices[:, self.number_3 - 1, :])
            del self.Pre_slices
        except:
            pass

    def save(self):
        len = self.slices.shape[0]
        self.otherSlices = zeros((len, 512, 512))
        for i in range(0, self.slices.shape[0]):
            self.otherSlices[i] = self.slices[len - 1 - i]
        # fd= QFileDialog.getSaveFileName(self, "文件保存", "/", "图片文件 (*.png);;(*.jpeg)")
        # fp = QFileDialog.getExistingDirectory()
        # fp=fp+"/simpleitk_save.nii.gz"
        name = QFileDialog.getSaveFileName(None, "Save File", "simpleitk_save.nii.gz", "*.nii.gz")
        fp = name[0]
        # if len(fp) != 0:
        # lineedit = "文件夹所在位置:" + fp
        # print(lineedit)
        # for i in range(len(slices)):
        # img = Image.fromarray(slices[self.number - 1 - i, :, :])
        # img.save(os.path.join(fp, str(i) + ".jpg"))
        # print("Yes")
        # else:
        # print("文件夹不存在")
        out = GetImageFromArray(self.otherSlices)
        WriteImage(out, fp)

    # def RG_3D_Segment(self):
    #     global RG3Dwindow
    #     self.slices[self.slices > 254] = 254  # 用254代替255灰度信息，便于后续模型建立
    #     RG3Dwindow = RGwindow.RGwindow(fp=self.fp, slices=self.slices, number=self.number)
    #     #将生成的窗口置于顶层
    #     RG3Dwindow.activateWindow()
    #     RG3Dwindow.setWindowState(RG3Dwindow.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
    #     RG3Dwindow.showNormal()

    def ThreeDGrowSegment(self):

        # time_start = time.time()  # 开始计时
        thresh = 8  # 调节灰度取值域
        limit = 1200  # 调节灰度面积取值上限
        changeAccept = 350  # 调节覆盖点变化量上限
        selectSeedRange = 10  # 种子点选择域
        rangeChangeAccept = 2000  # 调节允许灰度面积变化量上限
        seedGray = self.slices[self.number - 1, self.yPosition, self.xPosition]
        self.slices = threeDGrowSeg.Processing(self.slices, self.number, self.xPosition, self.yPosition, thresh, limit,
                                               seedGray,
                                               changeAccept, selectSeedRange, rangeChangeAccept, direction=2)
        self.vtkWidget3D.Finalize()
        self.rightgrid_layout_21.removeWidget(self.frame3D)
        self.frame3D, self.vtkWidget3D = createModel.model(self.fp, self.slices, self.vtkFlag, self.labelFalg)
        self.frame3D.setFocusPolicy(Qt.NoFocus)
        # self.rightgrid_layout_21.removeWidget(self.frame3D)
        self.rightgrid_layout_21.addWidget(self.frame3D)
        # time_end = time.time()  # 结束计时
        # timeperoid = time_end - time_start
        # print(timeperoid)
        # 获取无背景图
        slices_only = deepcopy(self.slices)
        slices_only[slices_only < 250] = 0

        ##导出nii
        # 原图
        # out = sitk.GetImageFromArray(self.slices)
        # 无背景图
        out = GetImageFromArray(slices_only)
        if Label_Direction == 1:
            out.SetDirection((0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0))
        # sitk.WriteImage(out, 'path_saved.nii.gz')
        self.refeshGraph_01(self.slices[self.number - 1, :, :])
        self.refeshGraph_02(self.slices[:, :, self.number_2 - 1])
        self.refeshGraph_03(self.slices[:, self.number_3 - 1, :])
        self.ClotDetection.setEnabled(True)
        self.Drawing.setEnabled(True)
        # self.VesselDetection.setEnabled(True)
        # self.AllDetection.setEnabled(True)

    def deepLearning_segment(self):
        self.ClotDetection.setEnabled(True)
        # self.VesselDetection.setEnabled(True)
        # self.AllDetection.setEnabled(True)
        self.judgeStr = ""

        def back(parameter):
            if parameter == "Closed":
                self.judgeStr = parameter
                # print(self.judgeStr)

        # try:
        prUet = []
        img3D_array = self.slices_Yuan
        # global processWindow
        # self.processWindow = ProcessWindow.Process()
        # self.processWindow._processSignal.connect(back)

        def ndarray2str(a):
            return a.tostring()

        def str2ndarray(a):
            return reshape(frombuffer(a, dtype=int64), (256, 256))

        i = 1
        # print("\nStart segmentation...")
        buffer = 4096 * 100
        try:
            sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sk.connect(("10.141.255.252", 8000))
        except ConnectionRefusedError:
            sk.close()
            # global processWindow
            # self.processWindow = ProcessWindow.Process()
            # self.processWindow._processSignal.connect(back)
            self.jumpPage = jumpWindow.Process()
            # self.processWindow.hide()
            # self.processWindow.close()
            return
        global processWindow
        self.processWindow = ProcessWindow.Process()
        self.processWindow._processSignal.connect(back)
        sk.send(str(len(img3D_array)).encode())
        # with tqdm(total=len(img3D_array),
        #         # pbar为终端显示的进度条
        #         desc=f'Processing',
        #         mininterval=0.3) as pbar:
        for img in img3D_array:
            if self.judgeStr == "Closed":
                # pbar.close()
                break
            peroidtime = time()
            img = Image.fromarray(img)
            box = (125, 125, 381, 381)
            img = array(img.crop(box))
            # print(type(img[0][0]))

            img = ndarray2str(img)

            head = len(img)
            sk.send(str(head).encode())
            sk.recv(buffer)
            sk.send(img)
            pr = ''.encode()
            head = int(sk.recv(buffer).decode())
            while len(pr) != head:
                data = sk.recv(buffer)
                pr += data
            pr = str2ndarray(pr)
            pr = pad(pr, ((125, 131), (125, 131)), 'constant', constant_values=(0, 0))

            prUet.append(pr)
            peroid = time() - peroidtime
            self.processWindow.processLabel_02.setText(
                "Time remain: " + str(int(peroid * (len(img3D_array) - i))) + "s, Speed: " + str(
                    round(1 / (time() - peroidtime), 1)) + "it/s")
            QApplication.processEvents()
            self.processWindow.processLabel_04.setText(str(i) + '/' + str(len(img3D_array)) + ' slices')
            QApplication.processEvents()
            self.processWindow.processBar.setValue((100 * i) / len(img3D_array))
            QApplication.processEvents()
            # pbar.update(1)
            i += 1
            # canvas.coords(fill_line, (0, 0, n, 60))
            sleep(0.001)  # 控制进度条流动的速度
        sk.close()
        # self.processWindow.exit()
        # 分割完成后将按钮设置为可以使用
        self.Drawing.setEnabled(True)

        # print("Finished!")
        if self.judgeStr == "Closed":
            return
        self.processWindow.hide()
        # print("HAHA",self.processWindow.isHidden())
        self.processWindow.close()
        # self.processWindow.close()
        # slices
        prUetarray = stack([s for s in prUet])
        # print("prUetarray: ", prUetarray.shape)
        self.slices[where((prUetarray == 1))] = 254
        self.slices[where((prUetarray == 2))] = 255

        # 后续噪声处理
        mark_1 = 250  # 内部血块标记灰度
        mark_2 = 251  # 内部血管标记灰度
        self.obj = ClotDetect.ClotDetection()
        self.objFlag = 1
        # self.obj._useSignal03.connect(self.hasCreated)
        self.obj_2 = VesselDetect.VesselDetection()
        # self.objFlag = 2
        self.slices, self.vesselReport, self.vesselReportResult = self.obj_2.Processing(self.slices, self.slicesRGB,
                                                                                        mark_2, thresh=255,
                                                                                        flag=True, windowFlag=False,
                                                                                        ifClosed=False)
        self.slices[self.slices == mark_2] = 255
        self.slices, self.clotReport, self.clotReportResult = self.obj.Processing(self.slices, self.slicesRGB,
                                                                                  mark_1, thresh=254, flag=True,
                                                                                  windowFlag=False, ifClosed=False)
        # self.obj.myResultWindow._useSignal02.connect(self.hasCreated)
        # if self.obj.getCreateSignal()==True:
        #     self.button_01.setEnabled(True)

        self.slices[self.slices == mark_1] = 254

        self.refeshGraph_01(self.slices[self.number - 1, :, :])
        self.refeshGraph_02(self.slices[:, :, self.number_2 - 1])
        self.refeshGraph_03(self.slices[:, self.number_3 - 1, :])
        self.vtkWidget3D.Finalize()
        self.rightgrid_layout_21.removeWidget(self.frame3D)
        self.frame3D, self.vtkWidget3D = createModel.model(self.fp, self.slices, self.vtkFlag,self.labelFalg)
        self.frame3D.setFocusPolicy(Qt.NoFocus)
        self.rightgrid_layout_21.addWidget(self.frame3D)
        self.reportNeedChange = False
        self.clotReportNeedChange = False
        self.vesselReportNeedChange = False
        # except BaseException as e:
        #     print(e)

    def hasCreated(self, parameter):
        if parameter == "Useable":
            self.button_01.setEnabled(True)

    # 确定关闭窗口后的事件，将vtk删除干净，否则会出现句柄无效的错误
    def closeEvent(self, event):
        if self.openFileNumber == 0:
            self.close()
        else:
            self.vtkWidget3D.Finalize()
            self.close()

    def DoOneAll(self):
        if (self.reportNeedChange):
            self.objFlag = 3
            mark_1 = 250  # 内部血块标记灰度
            mark_2 = 251  # 内部血管标记灰度
            self.obj = ClotDetect.ClotDetection()
            self.obj_2 = VesselDetect.VesselDetection()
            if (self.vesselReportNeedChange == True):
                self.slices, self.vesselReport, self.vesselReportResult = self.obj_2.Processing(self.slices,
                                                                                                self.slicesRGB, mark_2,
                                                                                                thresh=255, flag=True,
                                                                                                windowFlag=False,
                                                                                                ifClosed=True)
                self.slices[self.slices == mark_2] = 255
            if (self.clotReportNeedChange == True):
                self.slices, self.clotReport, self.clotReportResult = self.obj.Processing(self.slices, self.slicesRGB,
                                                                                          mark_1, thresh=254, flag=True,
                                                                                          windowFlag=False,
                                                                                          ifClosed=True)
                self.slices[self.slices == mark_1] = 254
            self.clotReportNeedChange = False
            self.vesselReportNeedChange = False
            self.reportNeedChange = False
        self.allReportResult = self.clotReport + "\n" + self.vesselReport
        self.pdfAllPreview = PDFPreviewWindow.PDFPreviewWindow(self.allReportResult, self.slices, self.clotReportResult,
                                                               True, self.graphName[self.length - 1])
        # self.pdfAllPreview = PDFPreviewWindow.PDFPreviewWindow(self.allReportResult, self.slices, self.clotReportResult)
        self.button_01.setEnabled(True)
        self.refeshGraph_01(self.slices[self.number - 1, :, :])
        self.refeshGraph_02(self.slices[:, :, self.number_2 - 1])
        self.refeshGraph_03(self.slices[:, self.number_3 - 1, :])

    def MyPen(self):
        if (self.PenFlag):
            self.setCursor(Qt.ArrowCursor)
            self.PenFlag = False
            self.RubberFlag = False
        else:
            self.setCursor(Qt.CrossCursor)
            self.PenFlag = True
            self.RubberFlag = False

    def MyRubber(self):
        if (self.RubberFlag):
            self.setCursor(Qt.ArrowCursor)
            self.PenFlag = False
            self.RubberFlag = False
        else:
            self.setCursor(Qt.IBeamCursor)
            self.RubberFlag = True
            self.PenFlag = False

    def MyVessel(self):
        self.VesselFlag = True
        self.ClotFlag = False

    def MyClot(self):
        self.ClotFlag = True
        self.VesselFlag = False

    def changeContrast(self):
        self.contrVal = 1 - self.contrast.value() * 0.01
        img = abs(self.slices[self.number - 1, :, :]) / 255
        img = (pow(img, self.contrVal) * 255).astype(uint8)  # 转换为0--255的灰度uint8类型
        self.refeshGraph_01(img)
        img = abs(self.slices[:, :, self.number_2]) / 255
        img = (pow(img, self.contrVal) * 255).astype(uint8)  # 转换为0--255的灰度uint8类型
        self.refeshGraph_02(img)
        img = abs(self.slices[:, self.number_3, :]) / 255
        img = (pow(img, self.contrVal) * 255).astype(uint8)  # 转换为0--255的灰度uint8类型
        self.refeshGraph_03(img)

    def changePen(self):
        self.penSize = self.penSlider.value() - 1
        # print("PenSizeValue", self.penSlider.value())
        # print("Pensize", self.penSize)

    def changeRubber(self):
        self.rubberSize = self.rubberSlider.value() - 1

    def drawNewWin(self):
        self.drawNewWindow = DrawWindow.DrawWindow(self.slices, self.number, self.slicesRGB)
        self.drawNewWindow._signal.connect(self.getData)

    def getData(self, paramater):
        self.slices = self.decodeTransformData(paramater)
        self.vtkWidget3D.Finalize()
        self.rightgrid_layout_21.removeWidget(self.frame3D)
        self.frame3D, self.vtkWidget3D = createModel.model(self.fp, self.slices, self.vtkFlag, self.labelFalg)
        self.frame3D.setFocusPolicy(Qt.NoFocus)
        self.rightgrid_layout_21.addWidget(self.frame3D)
        self.reportNeedChange = True
        self.clotReportNeedChange = True
        self.vesselReportNeedChange = True

    def decodeTransformData(self, input):
        return loads(input)

    def screenShotFun(self, event):
        if self.numberOfScreen < 2:
            self.numberOfScreen += 1
            self.screenWindow = WScreenShot()
            self.screenWindow.pixmapSignal.connect(self.sendScreenShot)

    def sendScreenShot(self, parameter):

        self.pdfAllPreview.getImage(parameter)
        # if self.objFlag==1:
        #     self.pdfAllPreview.getImage(parameter)
        # if self.objFlag==2:
        #     self.obj_2.sendImage(parameter)
        # if self.objFlag==3:
        #     self.pdfAllPreview.getImage(parameter)

        # self.screenWindow.close()

    def PDFPreviewClosed(self, parameter):
        if parameter == "Close":
            self.button_01.setEnabled(False)

