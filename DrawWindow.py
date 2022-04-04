from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtWidgets import QMainWindow,QLabel,QVBoxLayout,QWidget,QHBoxLayout,QPushButton,QFrame,QApplication,QDesktopWidget
from PyQt5.QtGui import QImage,QPixmap,QIcon
from numpy import where,uint8,int16,float32
from SimpleITK import GetImageFromArray
from copy import deepcopy
import NewQslider
import ConstratSlider
from cv2 import resize,cvtColor,COLOR_BGR2RGB
from MyLabel import MyLabel
import pickle
import threeDGrowSeg

Label_Direction = 0

class DrawWindow(QMainWindow):
    #定义发送信号
    _signal = pyqtSignal(bytes)
    def __init__(self,slices,number,slicesRGB):
        super().__init__()
        self.clickNumber=0
        self.contrVal = 1
        self.slices=deepcopy(slices)
        self.number=number
        self.initUI()
        self.openNewWin()
        self.PenFlag = False
        self.RubberFlag = False
        self.VesselFlag=True
        self.ClotFlag = False
        self.needAddUndo=False
        self.penSize=0
        self.rubberSize=0
        self.RedoStack = [[], [], []]
        self.RedoCounter = []
        self.RedoStackValue = []
        self.UndoStack = [[], [], []]
        self.UndoStackValue = []
        self.UndoCounter = []
        self.tempStepCounter = 0
        self.slicesRGB=slicesRGB

    def initUI(self):
        self.yPosition=0
        self.xPosition=0
        
        desktop = QApplication.desktop()
        self.height=desktop.height()-150
        #width=desktop.width()
        self.length=(self.height/5)*6
        self.setGeometry(200, 300, self.length, self.height)
        self.setWindowIcon(QIcon("Seg.png"))
        self.setWindowFlags(Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)
        self.setWindowTitle("CTA Segmentation")
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(int(newLeft),int(newTop))
        self.show()

    def myGrid(self):
        # 定义顶级布局管理器
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.mainLayout = QHBoxLayout()
        # 定义左侧布局管理器
        self.leftgrid_layout = QVBoxLayout()
        # 定义右侧布局管理器
        self.rightgrid_layout = QHBoxLayout()
        # 对右侧布局进行再次布局
        # self.rightgrid_layout_1 = QHBoxLayout()
        # self.rightgrid_layout_2 = QHBoxLayout()
        #对右下侧布局进行再次布局
        # self.rightgrid_layout_21=QHBoxLayout()
        # self.rightgrid_layout_22=QHBoxLayout()
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
        #label_02.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_03 = MyLabel("X:")
        self.label_03.setFrameShape(QFrame.Box)
        #label_03.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_04 = MyLabel("Y:")
        self.label_04.setFrameShape(QFrame.Box)
        #label_04.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_05 = MyLabel("Z:")
        self.label_05.setFrameShape(QFrame.Box)
        #label_05.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_06 = MyLabel("Gray Value:")
        self.label_06.setFrameShape(QFrame.Box)
        self.button_01=QPushButton("Save",self)
        self.button_01.clicked.connect(self.save)

        #对画笔和橡皮进行布局
        self.drawToolFrame=QFrame()
        self.drawToolFrame.setFrameShape(QFrame.Box)
        self.drawLayout=QVBoxLayout()
        self.drawLayout_1=QVBoxLayout()
        self.drawLayout_2=QHBoxLayout()
        self.drawLayout_21=QVBoxLayout()
        self.drawLayout_22=QVBoxLayout()
        self.drawToolFrame.setLayout(self.drawLayout)
        self.drawLayout.addLayout(self.drawLayout_1)
        self.drawLayout.addLayout(self.drawLayout_2)
        self.drawLayout.setStretchFactor(self.drawLayout_1,2)
        self.drawLayout.setStretchFactor(self.drawLayout_2,1)
        self.drawLayout_2.addLayout(self.drawLayout_21)
        self.drawLayout_2.addLayout(self.drawLayout_22)

        self.eraseFrame=QFrame()
        self.eraseFrame.setFrameShape(QFrame.Box)
        self.eraseLayout=QVBoxLayout()
        self.eraseFrame.setLayout(self.eraseLayout)

        self.button_02 = QPushButton("Pen", self)
        self.button_02.clicked.connect(self.MyPen)
        self.button_03 = QPushButton("Rubber", self)
        self.button_03.clicked.connect(self.MyRubber)
        self.button_04 = QPushButton("vessel", self)
        self.button_04.clicked.connect(self.MyVessel)
        self.button_05 = QPushButton("clot", self)
        self.button_05.clicked.connect(self.MyClot)
        self.button_06 = QPushButton("Undo", self)
        self.button_06.clicked.connect(self.MyUndo)
        self.button_07 = QPushButton("Redo", self)
        self.button_07.clicked.connect(self.MyRedo)
        # 对比度滑轮
        self.contrast = ConstratSlider.ConstratQSlider()
        self.contrast.setOrientation(Qt.Horizontal)
        self.contrast.setSingleStep(1)
        self.contrast.setMinimum(0)
        self.contrast.setMaximum(99)
        self.contrast.sliderMoved.connect(self.changeContrast)
        #笔滑轮
        self.penSlider = ConstratSlider.ConstratQSlider()
        self.penSlider.setOrientation(Qt.Horizontal)
        self.penSlider.setSingleStep(1)
        self.penSlider.setMinimum(1)
        self.penSlider.setMaximum(10)
        self.penSlider.valueChanged.connect(self.changePen)
        #橡皮滑轮
        self.rubberSlider = ConstratSlider.ConstratQSlider()
        self.rubberSlider.setOrientation(Qt.Horizontal)
        self.rubberSlider.setSingleStep(1)
        self.rubberSlider.setMinimum(1)
        self.rubberSlider.setMaximum(10)
        self.rubberSlider.valueChanged.connect(self.changeRubber)
        # label_06.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 创建对于左侧窗口的布局
        # leftgrid_layout=QGridLayout()
        self.leftgrid_layout.addStretch(13)
        self.leftgrid_layout.addWidget(self.drawToolFrame)
        # leftgrid_layout.addWidget(label_01,0,0)
        #self.leftgrid_layout.addWidget(self.button_02)
        self.drawLayout_1.addWidget(self.button_06)
        self.drawLayout_1.addWidget(self.button_07)
        self.drawLayout_1.addWidget(self.button_02)
        #self.leftgrid_layout.addWidget(self.penSlider)
        self.drawLayout_1.addWidget(self.penSlider)
        #self.leftgrid_layout.addWidget(self.button_04)
        self.drawLayout_21.addWidget(self.button_04)
        #self.leftgrid_layout.addWidget(self.button_05)
        self.drawLayout_22.addWidget(self.button_05)
        self.drawLayout_2.setStretchFactor(self.drawLayout_21,1)
        self.drawLayout_2.setStretchFactor(self.drawLayout_22,1)

        self.leftgrid_layout.addWidget(self.eraseFrame)
        self.eraseLayout.addWidget(self.button_03)
        self.eraseLayout.addWidget(self.rubberSlider)
        

        #self.leftgrid_layout.addWidget(self.button_03)
        #self.leftgrid_layout.addWidget(self.rubberSlider)
        self.leftgrid_layout.addWidget(self.contrast_Label)
        self.leftgrid_layout.addWidget(self.contrast)
        self.leftgrid_layout.addWidget(self.label_01)
        #leftgrid_layout.addWidget(label_02,1,0)
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
        self.leftgrid_layout.addStretch(13)
        # 对右侧进行布局,两个布局分别放置四个组件
        # 对滑块设置大小
        self.graph_01 = MyLabel(text='',connect=[self.label_03,self.label_04],IsClicked=False)
        self.graph_01.setGeometry(400, 300, self.height, self.height)
        self.graph_01.setFrameShape(QFrame.Box)
        self.graph_01_width = self.graph_01.width()
        self.graph_01_height = self.graph_01.height()
        # print("graph_01_width", self.graph_01_width)
        # print("graph_01_height", self.graph_01_height)




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
        self.scroll_01.valueChanged.connect(self.sliderMoved_01)
        # self.graph_02 = MyLabel(text='',connect=[self.label_03,self.label_04],number=self.number)
        # self.graph_02.setGeometry(840, 300, 480, 480)
        # self.graph_02.setFrameShape(QFrame.Box)
        #self.scroll_02 = NewQslider.MyQSlider()
        # self.scroll_02=NewQslider.MyQSlider()
        # self.scroll_02.setOrientation(Qt.Vertical)
        # self.scroll_02.setSingleStep(1)
        # self.scroll_02.setMinimum(1)
        # self.scroll_02.sliderMoved.connect(self.sliderMoved_02)

        # self.graph_03 = MyLabel(text='',connect=[self.label_03,self.label_04],number=self.number)
        # self.graph_03.setGeometry(840, 780, 480, 480)
        # self.graph_03.setFrameShape(QFrame.Box)
        #self.scroll_03 = NewQslider.MyQSlider()
        # self.scroll_03=NewQslider.MyQSlider()
        # self.scroll_03.setOrientation(Qt.Vertical)
        # self.scroll_03.setSingleStep(1)
        # self.scroll_03.setMinimum(1)
        # self.scroll_03.sliderMoved.connect(self.sliderMoved_03)
        # self.frame3D, self.vtkWidget3D=createModel.model(self.fp,self.slices)
        #thread=ModelThread(createModel.model,(self.fp,self.slices))
        #thread.start()
        #thread.join()
        #modelFrame=thread.get_result()

        self.rightgrid_layout.addWidget(self.graph_01)
        self.rightgrid_layout.addWidget(self.scroll_01)
        # self.rightgrid_layout_1.addWidget(self.graph_02)
        # self.rightgrid_layout_1.addWidget(self.scroll_02)
        #在布局中加入vtk体绘制窗口
        #rightgrid_layout_21.addWidget(self.vtkWidget)
        # self.rightgrid_layout_21.addWidget(self.frame3D)
        # self.rightgrid_layout_22.addWidget(self.graph_03)
        # self.rightgrid_layout_22.addWidget(self.scroll_03)
        #rightgrid_layout_2.addWidget(self.graph_04)
        #rightgrid_layout_2.addWidget(self.scroll_04)
        #rightgrid_layout_21.addWidget(self.vtkWidget)



        self.mainLayout.addLayout(self.leftgrid_layout)
        self.mainLayout.addLayout(self.rightgrid_layout)
        # self.rightgrid_layout.addLayout(self.rightgrid_layout_1)
        # self.rightgrid_layout.addLayout(self.rightgrid_layout_2)
        # self.rightgrid_layout_2.addLayout(self.rightgrid_layout_21)
        # self.rightgrid_layout_2.addLayout(self.rightgrid_layout_22)
        # 设置布局管理器比例系数
        # self.rightgrid_layout_2.setStretchFactor(self.rightgrid_layout_21,1)
        # self.rightgrid_layout_2.setStretchFactor(self.rightgrid_layout_22,1)
        self.mainLayout.setStretchFactor(self.leftgrid_layout, 1)
        self.mainLayout.setStretchFactor(self.rightgrid_layout, 5)

        # 创建一个左侧窗口的窗口对象
        # leftlayout_widget = QWidget(leftFrame)
        # 设置左侧窗口的布局层
        # leftlayout_widget.setLayout(leftgrid_layout)
        # 设置窗口出现的位置以及窗口的宽和高
    

    def openNewWin(self):
        # array = []
        # imgs = sitk.ReadImage(self.fp[0])
        # TestDirection = (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0)
        # img3D_array = sitk.GetArrayFromImage(imgs)
        # if imgs.GetDirection() == TestDirection:
        #     for i in range(len(img3D_array)):
        #         array.append(img3D_array[len(img3D_array) - i - 1, :, :])
        #     img3D_array = np.stack([s for s in array])
        #     global Label_Direction
        #     Label_Direction = 1
        # img3D_array = self.preprocessing(img3D_array)
        # self.open(img3D_array)
        self.myGrid()
        self.scroll_01.setValue((int)((self.slices.shape[0]) / 2))
        #print("Value",self.slices.shape[0])
        self.scroll_01.setMaximum(self.slices.shape[0])
        pixmap_imgSrc_01 = self.setInitGraph_01(self.scroll_01.value())
        self.graph_01.setPixmap(pixmap_imgSrc_01)
        self.graph_01.setAlignment(Qt.AlignCenter)


    def preprocessing(self, img3D_array):
        # global img3D_array_
        image = img3D_array.copy()
        image = image.astype(int16)
        img3D_array_ = img3D_array.astype(float32)  # 把数据从 int32转为 float32类型
        img3D_array_ = (img3D_array - img3D_array.min()) / (img3D_array.max() - img3D_array.min())
        # 把数据范围变为0--1浮点,或许还有其他转换方法,效果能更好一些.
        img3D_array = (img3D_array_ * 255).astype(uint8)  # 转换为0--255的灰度uint8类型
        return img3D_array


    # 返回加载在初始Label上的图片
    def setInitGraph_01(self, value):
        self.number = self.scroll_01.value()
        # print("Init Value",self.scroll_01.value())
        img = resize(src=self.slices[value- 1, :, :], dsize=None, fx=1, fy=1)
        img2 = cvtColor(img, COLOR_BGR2RGB)
        img2[where((img2 == [255, 255, 255]).all(axis=2))] = [255, 0, 0]
        img2[where((img2 == [254, 254, 254]).all(axis=2))] = [0, 255, 0]
        # 将nparray转化成QImage对象显示在QLabel中
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        self.pixmap_imgSrc_1 = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        return self.pixmap_imgSrc_1

    def refeshGraph_01(self,img):
        img = img.astype(uint8)  # 转换为0--255的灰度uint8类型
        try:
            img = resize(src=img, dsize=None, fx=1, fy=1)
        except:
            print("IndexError")
        # print(img.shape)
        img2 = cvtColor(img, COLOR_BGR2RGB)
        img2[where((img2 == [255, 255, 255]).all(axis=2))] = [255, 0, 0]
        img2[where((img2 == [254, 254, 254]).all(axis=2))] = [0, 255, 0]


        # 将nparray转化成QImage对象显示在QLabel中
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        self.pixmap_imgSrc_1 = QPixmap.fromImage(image).scaled(self.graph_01_width, self.graph_01_height)
        self.graph_01.setPixmap(self.pixmap_imgSrc_1)
        # 图片在label中居中显示
        self.graph_01.setAlignment(Qt.AlignCenter)
        self.graph_01.setScaledContents(False)

    def sliderMoved_01(self):
        # print("do the process 2")
        self.number = self.scroll_01.getSlicesNumber()
        #self.number=self.scroll_01.value()
        # print("number: ",self.number)
        img = abs(self.slices[self.number - 1, :, :] )/ 255
        img = (pow(img, self.contrVal) * 255)
        self.refeshGraph_01(img)

    # 定义鼠标事件
    # 鼠标移动事件
    def mousePressEvent(self, event):
        if(self.graph_01.xPosition>511):
            self.graph_01.xPosition=511
        if(self.graph_01.yPosition>511):
            self.graph_01.yPosition = 511
        if event.buttons() == Qt.LeftButton:
            if (self.graph_01.IsClicked ):
                if (self.PenFlag and self.graph_01.IsClicked):
                    self.needAddUndo = True
                    if (self.penSize == 0):
                        self.tempStepCounter += 1
                        if (self.VesselFlag):
                            self.UndoStackValue.append(
                                self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition])
                            self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition] = 255
                            self.UndoStack[0].append(self.number - 1)
                            self.UndoStack[1].append(self.graph_01.yPosition)
                            self.UndoStack[2].append(self.graph_01.xPosition)

                        else:
                            self.UndoStackValue.append(
                                self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition])
                            self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition] = 254
                            self.UndoStack[0].append(self.number - 1)
                            self.UndoStack[1].append(self.graph_01.yPosition)
                            self.UndoStack[2].append(self.graph_01.xPosition)
                    else:
                        for i in range(-self.penSize, self.penSize):
                            for j in range(-self.penSize, self.penSize):
                                if (self.VesselFlag):
                                    try:
                                        self.tempStepCounter += 1
                                        if((511-self.graph_01.yPosition + i)<0):
                                            i=511-self.graph_01.yPosition
                                        if ((511 - self.graph_01.xPosition + j) < 0):
                                            j = 511 - self.graph_01.xPosition
                                        self.UndoStackValue.append(
                                            self.slices[
                                                self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j])
                                        self.slices[
                                            self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j] = 255
                                        self.UndoStack[0].append(self.number - 1)
                                        self.UndoStack[1].append(self.graph_01.yPosition + i)
                                        self.UndoStack[2].append(self.graph_01.xPosition + j)
                                    except:
                                        pass
                                elif (self.ClotFlag):
                                    try:
                                        self.tempStepCounter += 1
                                        self.UndoStackValue.append(
                                            self.slices[
                                                self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j])
                                        self.slices[
                                            self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j] = 254
                                        self.UndoStack[0].append(self.number - 1)
                                        self.UndoStack[1].append(self.graph_01.yPosition + i)
                                        self.UndoStack[2].append(self.graph_01.xPosition + j)
                                    except:
                                        pass
                    img = self.slices[self.number - 1, :, :]
                    self.refeshGraph_01(img)
                if (self.RubberFlag and self.graph_01.IsClicked):
                    self.needAddUndo = True
                    self.graph_01.setIsClicked(False)
                    if (self.rubberSize == 0):
                        self.tempStepCounter += 1
                        self.UndoStackValue.append(
                            self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition])
                        self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition] \
                            = self.slicesRGB[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition]
                        self.UndoStack[0].append(self.number - 1)
                        self.UndoStack[1].append(self.graph_01.yPosition)
                        self.UndoStack[2].append(self.graph_01.xPosition)
                    else:
                        for i in range(-self.rubberSize, self.rubberSize):
                            for j in range(-self.rubberSize, self.rubberSize):
                                try:
                                    if ((511 - self.graph_01.yPosition + i) < 0):
                                        i = 511 - self.graph_01.yPosition
                                    if ((511 - self.graph_01.xPosition + j) < 0):
                                        j = 511 - self.graph_01.xPosition
                                    self.tempStepCounter += 1
                                    self.UndoStackValue.append(
                                        self.slices[
                                            self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j])
                                    self.slices[self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j] = \
                                        self.slicesRGB[
                                            self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j]
                                    self.UndoStack[0].append(self.number - 1)
                                    self.UndoStack[1].append(self.graph_01.yPosition + i)
                                    self.UndoStack[2].append(self.graph_01.xPosition + j)
                                except:
                                    pass
                    img = self.slices[self.number - 1, :, :]
                    self.refeshGraph_01(img)
                self.graph_01.setIsClicked(False)
                self.number = self.scroll_01.value()
                ###################
                self.number_2 = round(len(self.slices) * (self.graph_01.xPosition / 512))
                self.number_3 = round(len(self.slices[0, 0]) * (self.graph_01.yPosition / 512))
                self.label_03.setText("X: " + str(self.graph_01.xPosition))
                self.label_04.setText("Y: " + str(self.graph_01.yPosition))
                ###################
                self.label_05.setText("Z: " + str(self.number))
                self.grayValue = self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition]
                self.label_06.setText("Gray Value: " + str(self.grayValue))
                self.xPosition = self.graph_01.xPosition
                self.yPosition = self.graph_01.yPosition


    # 鼠标单击事件
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            if (self.graph_01.IsClicked):
                if (self.PenFlag and self.graph_01.IsClicked):
                    self.needAddUndo = True
                    if (self.penSize == 0):
                        self.tempStepCounter += 1
                        if (self.VesselFlag):
                            self.UndoStackValue.append(
                                self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition])
                            self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition] = 255
                            self.UndoStack[0].append(self.number - 1)
                            self.UndoStack[1].append(self.graph_01.yPosition)
                            self.UndoStack[2].append(self.graph_01.xPosition)

                        else:
                            self.UndoStackValue.append(
                                self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition])
                            self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition] = 254
                            self.UndoStack[0].append(self.number - 1)
                            self.UndoStack[1].append(self.graph_01.yPosition)
                            self.UndoStack[2].append(self.graph_01.xPosition)
                    else:
                        for i in range(-self.penSize, self.penSize):
                            for j in range(-self.penSize, self.penSize):
                                if ((511 - self.graph_01.yPosition + i) < 0):
                                    i = 511 - self.graph_01.yPosition
                                if ((511 - self.graph_01.xPosition + j) < 0):
                                    j = 511 - self.graph_01.xPosition
                                if (self.VesselFlag):
                                    self.tempStepCounter += 1
                                    try:
                                        self.UndoStackValue.append(
                                            self.slices[
                                                self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j])
                                        self.slices[
                                            self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j] = 255
                                        self.UndoStack[0].append(self.number - 1)
                                        self.UndoStack[1].append(self.graph_01.yPosition + i)
                                        self.UndoStack[2].append(self.graph_01.xPosition + j)
                                    except:
                                        pass
                                elif (self.ClotFlag):
                                    self.tempStepCounter += 1
                                    try:
                                        self.UndoStackValue.append(
                                            self.slices[
                                                self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j])
                                        self.slices[
                                            self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j] = 254
                                        self.UndoStack[0].append(self.number - 1)
                                        self.UndoStack[1].append(self.graph_01.yPosition + i)
                                        self.UndoStack[2].append(self.graph_01.xPosition + j)
                                    except:
                                        pass
                    img = self.slices[self.number - 1, :, :]
                    self.refeshGraph_01(img)
                if (self.RubberFlag and self.graph_01.IsClicked):
                    self.needAddUndo = True
                    self.graph_01.setIsClicked(False)
                    if (self.rubberSize == 0):
                        self.tempStepCounter += 1
                        self.UndoStackValue.append(
                            self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition])
                        self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition] \
                            = self.slicesRGB[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition]
                        self.UndoStack[0].append(self.number - 1)
                        self.UndoStack[1].append(self.graph_01.yPosition)
                        self.UndoStack[2].append(self.graph_01.xPosition)
                    else:
                        for i in range(-self.rubberSize, self.rubberSize):
                            for j in range(-self.rubberSize, self.rubberSize):
                                try:
                                    if ((511 - self.graph_01.yPosition + i) < 0):
                                        i = 511 - self.graph_01.yPosition
                                    if ((511 - self.graph_01.xPosition + j) < 0):
                                        j = 511 - self.graph_01.xPosition
                                    self.tempStepCounter += 1
                                    self.UndoStackValue.append(
                                        self.slices[
                                            self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j])
                                    self.slices[self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j] = \
                                        self.slicesRGB[
                                            self.number - 1, self.graph_01.yPosition + i, self.graph_01.xPosition + j]
                                    self.UndoStack[0].append(self.number - 1)
                                    self.UndoStack[1].append(self.graph_01.yPosition + i)
                                    self.UndoStack[2].append(self.graph_01.xPosition + j)
                                except:
                                    pass
                    img = self.slices[self.number - 1, :, :]
                    self.refeshGraph_01(img)
                self.graph_01.setIsClicked(False)
                self.number = self.scroll_01.value()
                ###################
                self.number_2 = round(len(self.slices) * (self.graph_01.xPosition / 512))
                self.number_3 = round(len(self.slices[0, 0]) * (self.graph_01.yPosition / 512))
                self.label_03.setText("X: " + str(self.graph_01.xPosition))
                self.label_04.setText("Y: " + str(self.graph_01.yPosition))
                ###################
                self.label_05.setText("Z: " + str(self.number))
                self.grayValue = self.slices[self.number - 1, self.graph_01.yPosition, self.graph_01.xPosition]
                self.label_06.setText("Gray Value: " + str(self.grayValue))
                self.xPosition = self.graph_01.xPosition
                self.yPosition = self.graph_01.yPosition


    def mouseReleaseEvent(self, event):
        if(self.needAddUndo):
            self.needAddUndo=False
            self.UndoCounter.append(self.tempStepCounter)
            self.tempStepCounter = 0
    
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

    def MyUndo(self):
        try:
            shape=[0,0,0]
            undoNum=self.UndoCounter.pop()
            # print(self.UndoStack)
            # print(undoNum)
            self.RedoCounter.append(undoNum)
            for i in range(undoNum):
                # print(i)
                shape[0]=self.UndoStack[0].pop()
                shape[1]=self.UndoStack[1].pop()
                shape[2] = self.UndoStack[2].pop()
                self.RedoStack[0].append(shape[0])
                self.RedoStack[1].append(shape[1])
                self.RedoStack[2].append(shape[2])
                self.RedoStackValue.append(self.slices[shape[0],shape[1],shape[2]])
                self.slices[shape[0],shape[1],shape[2]]=self.UndoStackValue.pop()
            self.refeshGraph_01(self.slices[shape[0],:,:])
            self.scroll_01.setValue(shape[0]+1)
        except:
            pass



    def MyRedo(self):
        try:
            shape = [0, 0, 0]
            RedoNum = self.RedoCounter.pop()
            self.UndoCounter.append(RedoNum)
            for i in range(RedoNum):
                shape[0] = self.RedoStack[0].pop()
                shape[1] = self.RedoStack[1].pop()
                shape[2] = self.RedoStack[2].pop()
                self.UndoStack[0].append(shape[0])
                self.UndoStack[1].append(shape[1])
                self.UndoStack[2].append(shape[2])
                self.UndoStackValue.append(self.slices[shape[0], shape[1], shape[2]])
                self.slices[shape[0], shape[1], shape[2]] = self.RedoStackValue.pop()
            self.refeshGraph_01(self.slices[shape[0], :, :])
            self.scroll_01.setValue(shape[0] + 1)
        except:
            pass

    
    def changeContrast(self):
        self.contrVal=1-self.contrast.value()*0.01
        img = abs(self.slices[self.number - 1, :, :] )/ 255
        img = (pow(img, self.contrVal) * 255).astype(uint8)  # 转换为0--255的灰度uint8类型
        self.refeshGraph_01(img)

    def changePen(self):
        self.penSize=self.penSlider.value()-1
        # print("PenSizeValue",self.penSlider.value())
        # print("Pensize",self.penSize)

    def changeRubber(self):
        self.rubberSize=self.rubberSlider.value()-1

#发送信号
    def save(self):
        self._signal.emit(self.encodeTransformData(self.slices))
        self.close()

    def encodeTransformData(self, input):
        return pickle.dumps(input, 2)

    def ThreeDGrowSegment(self):
        

        thresh = 8  # 调节灰度取值域
        limit = 1200  # 调节灰度面积取值上限
        changeAccept = 350  # 调节覆盖点变化量上限
        selectSeedRange = 10  # 种子点选择域
        rangeChangeAccept = 2000  # 调节允许灰度面积变化量上限
        seedGray = self.slices[self.number - 1, self.yPosition, self.xPosition]
        self.slices = threeDGrowSeg.Processing(self.slices, self.number, self.xPosition, self.yPosition, thresh, limit,
                                               seedGray,
                                               changeAccept, selectSeedRange, rangeChangeAccept, direction=2)
        # self.vtkWidget3D.Finalize()
        # self.rightgrid_layout_21.removeWidget(self.frame3D)
        # self.frame3D, self.vtkWidget3D=createModel.model(self.fp,self.slices)
        #self.rightgrid_layout_21.removeWidget(self.frame3D)
        # self.rightgrid_layout_21.addWidget(self.frame3D)

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
        #sitk.WriteImage(out, 'path_saved.nii.gz')
    
    

                
                



