from PyQt5.QtWidgets import QSlider,QLabel

class ConstratQSlider(QSlider):
    def __init__(self,parent=None,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        label = QLabel(self)
        self.label = label
        #label.setText('200')
        label.setStyleSheet('background-color:cyan;color:red')
        label.hide()

    def mousePressEvent(self, evt):
        super().mousePressEvent(evt)
        x = (((self.value()-self.minimum())/(self.maximum()-self.minimum())))*(self.width()-self.label.width())
        y =  (self.height()-self.label.height())/2
        self.label.move(x,y)
        self.label.show()
        # print("Slider value", self.value())
        self.label.setText(str(self.value()))

    def mouseMoveEvent(self, evt):
        super().mouseMoveEvent(evt)
        x = (((self.value()-self.minimum())/(self.maximum()-self.minimum())))*(self.width()-self.label.width())
        y =  (self.height()-self.label.height())/2
        self.label.move(x,y)
        #print("makabakamakabaka:",self.value())
        #print("Slider value", self.value())
        self.label.setText(str(self.value()))
        self.label.adjustSize()

    def mouseReleaseEvent(self, evt):
        super().mouseReleaseEvent(evt)
        self.label.show()
