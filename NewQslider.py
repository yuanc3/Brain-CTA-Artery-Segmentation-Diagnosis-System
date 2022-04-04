from PyQt5.QtWidgets import QLabel,QSlider

class MyQSlider(QSlider):
    def __init__(self,parent=None,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        label = QLabel(self)
        self.label = label
        #label.setText('200')
        label.setStyleSheet('background-color:cyan;color:red')
        label.hide()

    def mousePressEvent(self, evt):
        try:
            super().mousePressEvent(evt)
            y = (1-((self.value()-self.minimum())/(self.maximum()-self.minimum())))*(self.height()-self.label.height())
            x =  (self.width()-self.label.width())/2
            self.label.move(x,y)
            self.label.show()
            #print("Slider value", self.value())
            self.label.setText(str(self.value()))
        except:
            pass

    def mouseMoveEvent(self, evt):
        try:
            super().mouseMoveEvent(evt)
            y = (1-((self.value()-self.minimum())/(self.maximum()-self.minimum())))*(self.height()-self.label.height())
            x =  (self.width()-self.label.width())/2
            self.label.move(x,y)
            #print("makabakamakabaka:",self.value())
            # print("Slider value", self.value())
            self.label.setText(str(self.value()))
            self.label.adjustSize()
        except:
            pass

    def mouseReleaseEvent(self, evt):
        try:
            super().mouseReleaseEvent(evt)
            self.label.show()
        except:
            pass

    def getSlicesNumber(self):
        try:
            return self.value()
        except:
            pass
    