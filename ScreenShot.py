from PyQt5.QtWidgets import QWidget,QDesktopWidget,QApplication
from PyQt5.QtGui import QPixmap,QPainter,QBitmap,QPen,QBrush
from PyQt5.QtCore import Qt,pyqtSignal,QPoint,QRect
 
'''
# Qt 中无法导入 QScreen 类
try:
    from PySide2.QtGui import QScreen
except:
    from PyQt5.QtGui import QScreen
'''

class WScreenShot(QWidget):
    pixmapSignal = pyqtSignal(QPixmap)
    def __init__(self, parent=None):
        super(WScreenShot, self).__init__(parent)
        self.flag=False
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet('''background-color:black; ''')
        self.setWindowOpacity(0.6)
        # desktop = QApplication.desktop()
        # rect = desktop.availableGeometry()
        desktopRect = QDesktopWidget().screenGeometry()
        self.setGeometry(desktopRect)
        self.setCursor(Qt.CrossCursor)
        self.blackMask = QBitmap(desktopRect.size())
        self.blackMask.fill(Qt.black)
        self.mask = self.blackMask.copy()
        self.isDrawing = False
        self.startPoint = QPoint()
        self.endPoint = QPoint()
        self.show()
 
    def paintEvent(self, event):
        if self.isDrawing:
            self.mask = self.blackMask.copy()
            pp = QPainter(self.mask)
            pen = QPen()
            pen.setStyle(Qt.NoPen)
            pp.setPen(pen)
            brush = QBrush(Qt.white)
            pp.setBrush(brush)
            pp.drawRect(QRect(self.startPoint, self.endPoint))
            self.setMask(QBitmap(self.mask))

 
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPoint = event.pos()
            self.endPoint = self.startPoint
            self.isDrawing = True
 
    def mouseMoveEvent(self, event):
        if self.isDrawing:
            self.endPoint = event.pos()
            self.update()
 
    def mouseReleaseEvent(self, event):
        #if event.button() == Qt.LeftButton:
        self.endPoint = event.pos()
            # PySide2
            # screenshot = QPixmap.grabWindow(QApplication.desktop().winId())
            # PyQt5
            # screenshot = QApplication.primaryScreen().grabWindow(0)
            # 通用
        screenshot = QApplication.primaryScreen().grabWindow(QApplication.desktop().winId())
        rect = QRect(self.startPoint, self.endPoint)
            #获得截取的图片
        self.outputRegion = screenshot.copy(rect)
            #转化成QImage对象
        #self.image=QImage(self.outputRegion)
        self.pixmapSignal.emit(self.outputRegion)
        #self.getImage(self.outputRegion)
        self.close()

 
 
# if __name__ == '__main__':
#     # app = QApplication.instance() or QApplication(sys.argv)
#     # WScreenShot.run()
#     # app.exec_()
 
#     app = QApplication(sys.argv)
#     win = WScreenShot()
#     win.show()
#     app.exec_()
 
    # app = QApplication(sys.argv)
    # win = DesktopChosenBox(700, 500, 30)
    # win.show()
    # app.exec_()