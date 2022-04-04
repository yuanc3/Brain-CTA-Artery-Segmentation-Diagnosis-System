from PyQt5.QtWidgets import QMainWindow,QVBoxLayout,QWidget,QHBoxLayout,QPushButton,QTextEdit,QDesktopWidget
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QIcon
import PDFPreviewWindow
import base64
import os
from seg_ico import imglogo

class ResultWindow(QMainWindow):
    _useSignal02=pyqtSignal(str)
    _closeSignal02=pyqtSignal(str)
    # _resultSignal03 = pyqtSignal(str)
    # _resultSignal04 = pyqtSignal(str)
    def __init__(self,slices):
        super().__init__()
        #声明一个数组存储,使用.append加入元素
        self.clotResult=[]
        self.vesselResult=[]
        #当值为1的时候为血块，当值为2的时候为血管
        self.choice=0
        # self.getFlag01=False
        # self.getFlag02=False
        self.slices=slices
        self.setWindowTitle("Report")
        self.setGeometry(400, 400, 1100, 800)
        #使窗口居中
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(int(newLeft),int(newTop))
        #self.show()
        self.setup_ui()
        

    def setup_ui(self):
        #定义主文本框
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.mainLayout = QVBoxLayout()
        self.mainlayout_widget = QWidget()
        self.mainlayout_widget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainlayout_widget)

        self.upLayout=QHBoxLayout()
        self.downLayout=QHBoxLayout()
        self.mainLayout.addLayout(self.upLayout)
        self.mainLayout.addLayout(self.downLayout)

        self.text=QTextEdit()
        self.PDFButton=QPushButton("PDF Preview")
        self.PDFButton.clicked.connect(self.PDFPreview)
        self.cursor=self.text.textCursor()
        self.upLayout.addWidget(self.text)
        self.downLayout.addWidget(self.PDFButton)
        # print(self.text.toPlainText())
        #self.mainLayout.addWidget(self.text)
    def PDFPreview(self):
        self.setWindowFlags(Qt.Widget)
        self.setGeometry(200, 300, 800, 600)
        tmp = open('in.ico', 'wb')
        tmp.write(base64.b64decode(imglogo))
        tmp.close()
        self.setWindowIcon(QIcon("in.ico"))
        os.remove('in.ico')
        if self.choice==1:
            self.previewWindow=PDFPreviewWindow.PDFPreviewWindow(self.text.toPlainText(),self.slices,self.clotResult,True)
            self.previewWindow._closeSignal01.connect(self.sendCloseSignal)
        # elif self.choice==2:
        #     print("Generate Vesssel Report")
        #     self.previewWindow=PDFVesselPreview.PDFPreviewWindow(self.text.toPlainText(),self.slices,self.vesselResult)
        # else:
        #     print("Generate Clot Report")
        #     self.previewWindow=PDFPreviewWindow.PDFPreviewWindow(self.text.toPlainText(),self.slices,self.clotResult)
        #self.previewWindow._useableSignal01.connect(self.sendSignal)
        self._useSignal02.emit("Useable")
        #self.getCreateSignal02=self.previewWindow.getCreateSignal()
        # self.previewWindow._resultSignal01.connect(self.getScreenShot01)
        # self.previewWindow._resultSignal02.connect(self.getScreenShot02)
    
    # def sendSignal(self,parameter):
    #     print("Send Signal resultWindow",parameter)
    #     self._useSignal02.emit(parameter)

    # def getCreateSignal(self):
    #     return self.getCreateSignal02


    # def getScreenShot01(self):
    #     self.getFlag01=True
    #     self._resultSignal03.emit("First")
    
    # def getScreenShot02(self):
    #     self.getFlag02=True
    #     self._resultSignal04.emit("Second")

    
    def getImage(self,image):
        self.image=image
        self.previewWindow.getImage(image)

    #获得血块的数量
    def getClotResult(self,clotNumber,choice):
        self.clotResult=clotNumber
        self.choice=choice

    def getVesselDetect(self, vesselNumber,choice):
        self.vesselResult=vesselNumber
        self.choice=choice
    
    def sendClotResult(self):
        self.previewWindow.getClotResult(self.clotResult)
    
    def sendCloseSignal(self):
        self._closeSignal02.emit("Close")



    