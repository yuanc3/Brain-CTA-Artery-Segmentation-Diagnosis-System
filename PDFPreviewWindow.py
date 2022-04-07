from PyQt5.QtWidgets import QMainWindow,QLabel,QVBoxLayout,QWidget,QHBoxLayout,QPushButton,QFrame,QDesktopWidget,QFileDialog,QTextEdit
from PyQt5.QtGui import QPagedPaintDevice,QPagedPaintDevice,QPdfWriter,QPixmap,QImage,QPainter,QIcon
from PyQt5.QtCore import Qt,QFile,QIODevice,pyqtSignal,QMarginsF,QRect
from cv2 import resize,cvtColor,COLOR_BGR2RGB
from numpy import where,uint8,array
import NewQslider
import base64
import os
from seg_ico import imglogo

class PDFPreviewWindow(QMainWindow):
    _useableSignal01=pyqtSignal(str)
    _closeSignal01=pyqtSignal(str)
    # _resultSignal01 = pyqtSignal(str)
    # _resultSignal02 = pyqtSignal(str)
    def __init__(self,content,slices,clot,myflag,name):
        super().__init__()
        print("Enter Again")
        self.myflag=myflag
        self.getScreenShotFlag=False
        self.i=0
        print(self.i)
        self.clotResult=clot
        self.content=content
        self.slices=slices
        self.name="Report "+name 
        self.setWindowTitle(self.name)
        #self.setGeometry(400, 400, 1200, 800)
        self.setFixedSize(1200,800)
        self.setGeometry(200, 300, 800, 600)
        tmp = open('in.ico', 'wb')
        tmp.write(base64.b64decode(imglogo))
        tmp.close()
        self.setWindowIcon(QIcon("in.ico"))
        os.remove('in.ico')
        # if self.myflag==True:
        #     self.setWindowFlags(Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)
        #self. _useableSignal01.emit("Useable")
        self.createFlag=True
        #使窗口居中
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(int(newLeft),int(newTop))
        self.show()
        self.setup_ui()
    def getCreateSignal(self):
        return self.createFlag  

    def setup_ui(self):
        if self.clotResult==[]:
            self.mainLayout = QVBoxLayout()
            self.mainlayout_widget = QWidget()
            self.mainlayout_widget.setLayout(self.mainLayout)
            self.setCentralWidget(self.mainlayout_widget)

            self.layout01=QHBoxLayout()
            self.layout02=QHBoxLayout()
            self.layout021=QHBoxLayout()
            #self.layout022=QHBoxLayout()
            self.layout023=QHBoxLayout()

            self.layout03=QHBoxLayout()
            # self.layout04=QHBoxLayout()

            self.mainLayout.addLayout(self.layout01)
            self.mainLayout.addLayout(self.layout02)
            # self.mainLayout.addLayout(self.layout04)
            self.mainLayout.addLayout(self.layout03)
            self.layout02.addLayout(self.layout021)
            #self.layout02.addLayout(self.layout022)
            self.layout02.addLayout(self.layout023)


            self.text=QTextEdit()
            self.image01=QLabel()
            self.screenStr="Use \"Sreenshoot\" to capture"+"\n"+"the pathological images you want"
            self.fillLabel01=QLabel(self.screenStr)
            self.fillLabel01.setAlignment(Qt.AlignCenter)
            #self.fillLabel01.setFrameShape(QFrame.Box)
            self.image01.setFrameShape(QFrame.Box)
            self.image01.setGeometry(500,400,480,480)
            self.fillLabel02=QLabel(self.screenStr)
            self.fillLabel02.setAlignment(Qt.AlignCenter)
            self.PDFButton=QPushButton("PDF Converter")
            self.PDFButton.clicked.connect(self.PDFConvert)
            self.cursor=self.text.textCursor()
            self.layout01.addWidget(self.text)
            self.layout021.addWidget(self.fillLabel01)
            # self.layout022.addWidget(self.image01)
            # self.layout022.addWidget(self.scroll)
            self.layout023.addWidget(self.fillLabel02)
            self.layout03.addWidget(self.PDFButton)
        

            self.text.setText(self.content.expandtabs(tabsize=8))
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        #定义主文本框
        else:
            self.mainLayout = QVBoxLayout()
            self.mainlayout_widget = QWidget()
            self.mainlayout_widget.setLayout(self.mainLayout)
            self.setCentralWidget(self.mainlayout_widget)

            self.layout01=QHBoxLayout()
            self.layout02=QHBoxLayout()
            self.layout021=QHBoxLayout()
            self.layout022=QHBoxLayout()
            self.layout023=QHBoxLayout()
            self.layout04=QHBoxLayout()
            self.layout041=QHBoxLayout()
            self.layout042=QHBoxLayout()
            self.layout043=QHBoxLayout()
            self.layout03=QHBoxLayout()
            # self.layout04=QHBoxLayout()

            self.mainLayout.addLayout(self.layout01)
            self.mainLayout.addLayout(self.layout02)
            self.mainLayout.addLayout(self.layout04)
            self.mainLayout.addLayout(self.layout03)
            self.layout02.addLayout(self.layout021)
            self.layout02.addLayout(self.layout022)
            self.layout02.addLayout(self.layout023)
            self.layout04.addLayout(self.layout041)
            self.layout04.addLayout(self.layout042)
            self.layout04.addLayout(self.layout043)

            self.text=QTextEdit()
            self.image01=QLabel()
            self.screenStr="Use \"Sreenshoot\" to capture"+"\n"+"the pathological images you want"
            self.fillLabel01=QLabel(self.screenStr)
            self.fillLabel01.setAlignment(Qt.AlignCenter)
            #self.fillLabel01.setFrameShape(QFrame.Box)
            self.image01.setFrameShape(QFrame.Box)
            self.image01.setGeometry(500,400,480,480)
            self.fillLabel02=QLabel(self.screenStr)
            self.fillLabel02.setAlignment(Qt.AlignCenter)
            #self.fillLabel02.setFrameShape(QFrame.Box)
            self.scroll=NewQslider.MyQSlider()
            self.scroll.setOrientation(Qt.Vertical)
            self.scroll.setSingleStep(1)
            self.scroll.setMinimum(1)
            self.scroll.setValue(1)
            self.scroll.setMaximum(len(self.clotResult))
            self.scroll.valueChanged.connect(self.sliderMoved_01)
            self.layerNumber01=QLabel()
            #self.layerNumber01.setFrameShape(QFrame.Box)
            self.layerNumber=QLabel()
            self.layerNumber.setAlignment(Qt.AlignCenter)
            #self.layerNumber.setFrameShape(QFrame.Box)
            self.layerNumber02=QLabel()
            #self.layerNumber02.setFrameShape(QFrame.Box)
            self.PDFButton=QPushButton("PDF Converter")
            self.PDFButton.clicked.connect(self.PDFConvert)
            self.pixmap = self.setImage01(self.scroll.value()-1)
            # self.screenShot=QPushButton("Screen Shot")
            # self.screenShot.clicked.connect(self.screenShotFun)
            self.cursor=self.text.textCursor()
            self.layout01.addWidget(self.text)
            self.layout021.addWidget(self.fillLabel01)
            self.layout022.addWidget(self.image01)
            self.layout022.addWidget(self.scroll)
            self.layout023.addWidget(self.fillLabel02)
            # self.layout03.addWidget(self.image02)
            # self.layout03.addWidget(self.image03)
            self.layout041.addWidget(self.layerNumber01)
            self.layout042.addWidget(self.layerNumber)
            self.layout043.addWidget(self.layerNumber02)
            self.layout03.addWidget(self.PDFButton)
        

            self.text.setText(self.content.expandtabs(tabsize=8))

        
            #self. _useableSignal01.emit("Useable")
    
    def setImage01(self,num):
  
        self.number=array(self.clotResult)[num]
        #self.number=self.clotResult[num]

        img=self.slices[self.number-1, :, :]
        img = img.astype(uint8)  # 转换为0--255的灰度uint8类型
        try:
            img = resize(src=img, dsize=None, fx=1, fy=1)
        except:
            print("IndexError")
        # print(img.shape)
        #print(len(img[img == 253]))
        img2 = cvtColor(img, COLOR_BGR2RGB)
        img2[where((img2 == [255, 255, 255]).all(axis=2))] = [255, 0, 0]
        img2[where((img2 == [254, 254, 254]).all(axis=2))] = [0, 255, 0]
        img2[where((img2 == [253, 253, 253]).all(axis=2))] = [152, 245, 255]
        # 将nparray转化成QImage对象显示在QLabel中
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        pixmap_imgSrc_1 = QPixmap.fromImage(image).scaled(self.image01.width()/2, self.image01.height()/2)
        self.layerNumber.setText(str(self.number))
        self.image01.setPixmap(pixmap_imgSrc_1)
        self.image01.setAlignment(Qt.AlignCenter)
        self.image01.setScaledContents(True)

    def sliderMoved_01(self):

        try:
            self.setImage01(self.scroll.value()-1)
        except:
            pass


    def PDFConvert(self):
        #打开需要保存的文件
        if(self.name.find(".gz")!=-1):
            self.name=self.name[:-3]
        name = QFileDialog.getSaveFileName(None, "Save File",self.name, "*.pdf")
        pdfFile = QFile(name[0])
     
        #打开要写入的pdf文件
        pdfFile.open(QIODevice.WriteOnly)
        #创建pdf写入器
        pPdfWriter = QPdfWriter(pdfFile)
        #设置纸张为A4
        pPdfWriter.setPageSize(QPagedPaintDevice.A4)
        #设置纸张的分辨率为300,因此其像素为3508X2479
        pPdfWriter.setResolution(300)
        pPdfWriter.setPageMargins(QMarginsF(60, 60, 60, 60))
        pPdfPainter = QPainter(pPdfWriter)
        # 标题上边留白
        iTop = 100
        #文本宽度2100
        iContentWidth = 2200
        str01=self.text.toPlainText()
        #str.expandtabs(tabsize = 8)
        # print(self.text.toPlainText())
        # print(type(str))
        strResult=str01.split('\n')
        strResult=str01.split('\n')
        content=""
        textCounter=0
        # print("This is PDF")
        for i in range(0,len(strResult)):
            # content+=strResult[i].expandtabs(tabsize=8)
            # print("This is strResult",strResult[i])
            # content+="\n"
            content=strResult[i].expandtabs(tabsize=8)
            # print("Print Content",content)
            pPdfPainter.drawText(QRect(0, iTop+textCounter*50, iContentWidth, 100), Qt.TextWordWrap,content)
            self.rect=QRect(0, iTop+textCounter*50, iContentWidth, 100)
            if i%50==0:
                if i!=0:
                    pPdfWriter.newPage()
                    textCounter=0
            else:
                textCounter+=1

        # #option=QTextOption(Qt.AlignLeft | Qt.AlignVCenter)
        # #option.setWrapMode(QTextOption.WordWrap)
        # #str.expandtabs(tabsize = 8)
        # pPdfPainter.drawText(QRect(0, iTop, iContentWidth, 3000), Qt.TextWordWrap,content)
        # pPdfWriter.newPage() 

        if self.getScreenShotFlag==True:
            # pPdfWriter.newPage()
            if self.i==1:
                print(self.i)
                pPdfPainter.drawImage(QRect(0,self.rect.y()+100,self.image01.width()/2+300,self.image01.height()/2+300),self.fillLabel01.pixmap().toImage())
            if self.i==2:
                print(self.i)
                pPdfPainter.drawImage(QRect(0,self.rect.y()+100,self.image01.width()/2+300,self.image01.height()/2+300),self.fillLabel01.pixmap().toImage())
                pPdfPainter.drawImage(QRect(self.image01.width()/2+500,self.rect.y()+100,self.image01.width()/2+300,self.image01.height()/2+300),self.fillLabel02.pixmap().toImage())

        # for i in range(0, len(self.clotResult)):
        #     print(self.clotResult[i])
        pPdfWriter.newPage()
        i=0
        factor=0
        pageNumber=1
        finalX=0
        finalY=200
        count=0
        changePage=False
        while i<len(self.clotResult):
            clotLayerNumber=i
            # print("clotLayerNumber",clotLayerNumber)
            for j in range(0,3):
                if (clotLayerNumber+j)>len(self.clotResult):
                    break
                
                pPdfPainter.drawImage(QRect(finalX+j*(self.image01.width()/2+500),finalY+(((int)(factor/3))*(self.image01.height()/2+500)),self.image01.width()/2+300,self.image01.height()/2+300),self.convertImage(i))
                rect=QRect(finalX+j*(self.image01.width()/2+500),finalY+(((int)(factor/3))*(self.image01.height()/2+500)),self.image01.width()/2+300,self.image01.height()/2+300)
                #print((self.image01.height()/2+500)*((int)(i/3)))
                
                # if i==len(self.clotResult)-1:
                #     self.finalX=rect.x()
                #     self.finalY=rect.y()
                i+=1
                factor+=1
                if i==len(self.clotResult):
                    break
                # if i%3==0:
                #     factor+=1
                if rect.y()>=2219:
                    if i%3==0:
                
                        changePage=True
                        
                        self.clotLayerNumResult="Slices:"+"\t\t\t\t\t\t\t\t\t"+(str)(self.clotResult[clotLayerNumber])+"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"+(str)(self.clotResult[clotLayerNumber+1])+"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"+(str)(self.clotResult[clotLayerNumber+2])+"\n"
                        pPdfPainter.drawText(QRect(0, 700+count*(self.image01.height()/2+500), 2000,300), Qt.TextWordWrap,self.clotLayerNumResult)
                        pPdfWriter.newPage()
                        pageNumber+=1
                        finalX=0
                        finalY=200
                        factor=0
                        count=0
            if changePage==False:
                if i%3==1:
   
                    self.clotLayerNumResult="Slices:"+"\t\t\t\t\t\t\t\t\t"+(str)(self.clotResult[clotLayerNumber])
                    pPdfPainter.drawText(QRect(0, 700+count*(self.image01.height()/2+500), 2000,300), Qt.TextWordWrap,self.clotLayerNumResult)
                elif i%3==2:
      
                    self.clotLayerNumResult="Slices:"+"\t\t\t\t\t\t\t\t\t"+(str)(self.clotResult[clotLayerNumber])+"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"+(str)(self.clotResult[clotLayerNumber+1])+"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"
                    pPdfPainter.drawText(QRect(0, 700+count*(self.image01.height()/2+500), 2000,300), Qt.TextWordWrap,self.clotLayerNumResult)
                else:
              
                    self.clotLayerNumResult="Slices:"+"\t\t\t\t\t\t\t\t\t"+(str)(self.clotResult[clotLayerNumber])+"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"+(str)(self.clotResult[clotLayerNumber+1])+"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"+(str)(self.clotResult[clotLayerNumber+2])+"\n"
                    pPdfPainter.drawText(QRect(0, 700+count*(self.image01.height()/2+500), 2000,300), Qt.TextWordWrap,self.clotLayerNumResult)
                count+=1
            else:
                changePage=False
    
        # if factor%3==0:
        # if self.getScreenShotFlag==True:
        #     pPdfWriter.newPage()
        #     pPdfPainter.drawImage(QRect(0,200,self.image01.width()/2+300,self.image01.height()/2+300),self.fillLabel01.pixmap().toImage())
        #     pPdfPainter.drawImage(QRect(self.image01.width()/2+500,200,self.image01.width()/2+300,self.image01.height()/2+300),self.fillLabel02.pixmap().toImage())
        # else:
        #     pPdfPainter.drawImage(QRect(0,self.finalY+self.image01.height()/2+500,self.image01.width()/2+300,self.image01.height()/2+300),self.fillLabel01.pixmap().toImage())
        #     pPdfPainter.drawImage(QRect(self.image01.width()/2+500,self.finalY+self.image01.height()/2+500,self.image01.width()/2+300,self.image01.height()/2+300),self.fillLabel02.pixmap().toImage())
        # pPdfPainter.drawImage(QRect(0,1000,self.image01.width()/2+100,self.image01.height()/2+100),self.fillLabel01.pixmap().toImage())
        # pPdfPainter.drawImage(QRect(self.image01.width(),1000,self.image01.width()/2+100,self.image01.height()/2+100),self.fillLabel02.pixmap().toImage())
        #pPdfPainter.drawImage(QRect(self.image01.width()+self.image02.width(),1000,self.image03.width()/2+100,self.image03.height()/2+100),self.image03.pixmap().toImage())
        # #for i in range(0,len(strResult)):
        #     #pPdfPainter.drawText(QRect(0, iTop, iContentWidth, 1000), Qt.TextWordWrap,strResult[i])
        # #pPdfPainter.drawText(QRect(0, iTop, iContentWidth, 90), Qt.AlignHCenter,self.text.toPlainText())
        del pPdfPainter


    
    def getImage(self,image):
        self.getScreenShotFlag=True
        image=image.scaled(self.image01.width(), self.image01.height())
        #记录截屏的个数
   
        if self.i==0:
            self.fillLabel01.setPixmap(image)
            self.fillLabel01.setAlignment(Qt.AlignCenter)
            #self._resultSignal01.emit("First")
            self.i+=1
            return
        if self.i==1:
        
            self.fillLabel02.setPixmap(image)
            self.fillLabel02.setAlignment(Qt.AlignCenter)
            self.i+=1
            return
            #self._resultSignal02.emit("Second")
    
    def getClotResult(self,clot):
        self.clotResult=clot

    def convertImage(self,num):
        #将图片从np.array转化成QImage类型
        #print("Number",num)
        #self.number=np.array(self.clotResult)[num]
        self.number=self.clotResult[num]
        #print("self.number",self.number)
        img=self.slices[self.number-1, :, :]
        img = img.astype(uint8)  # 转换为0--255的灰度uint8类型
        try:
            img = resize(src=img, dsize=None, fx=1, fy=1)
        except:
            print("IndexError")
        # print(img.shape)
        #print(len(img[img == 253]))
        img2 = cvtColor(img, COLOR_BGR2RGB)
        img2[where((img2 == [255, 255, 255]).all(axis=2))] = [255, 0, 0]
        img2[where((img2 == [254, 254, 254]).all(axis=2))] = [0, 255, 0]
        img2[where((img2 == [253, 253, 253]).all(axis=2))] = [152, 245, 255]
        # 将nparray转化成QImage对象显示在QLabel中
        image = QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QImage.Format_RGB888)
        # pixmap_imgSrc_1 = QPixmap.fromImage(image).scaled(self.image01.width()/2, self.image01.height()/2)
        return image

    def closeEvent(self,event):
        self._closeSignal01.emit("Close")
        self.close()
        

