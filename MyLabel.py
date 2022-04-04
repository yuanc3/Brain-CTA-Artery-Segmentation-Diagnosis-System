from PyQt5.QtWidgets import QLabel
class MyLabel(QLabel):

    def __init__(self, text, connect=0,IsClicked=True):
        super().__init__(text)
        self.x = 0
        self.y= 0
        self.xPosition=0
        self.yPosition=0
        self.connect=connect
        self.IsClicked=IsClicked

    def setIsClicked(self, judge):
        self.IsClicked = judge

    def getIsClicked(self):
        return self.IsClicked

    def mousePressEvent(self, e):
        self.x=e.x()
        self.y=e.y()
        if self.connect:
            self.xPosition = round(self.x * (512.0 / self.width()))
            self.yPosition = round(self.y * (512.0 / self.height()))
            self.connect[0].setText("X: "+str(self.xPosition))
            self.connect[1].setText("Y: " + str(self.yPosition))
            if(self.xPosition<0):
                self.xPosition=0
            if(self.yPosition<0):
                self.yPosition=0
            if(self.xPosition>511):
                self.xPosition=511
            if(self.yPosition>511):
                self.yPosition=511
            self.setIsClicked(True)
        e.ignore()
    def mouseMoveEvent(self, e):
        # print("Internal")
        self.x=e.x()
        self.y=e.y()
        if self.connect:
            self.xPosition = round(self.x * (512.0 / self.width()))
            self.yPosition = round(self.y * (512.0 / self.height()))
            self.connect[0].setText("X: "+str(self.xPosition))
            self.connect[1].setText("Y: " + str(self.yPosition))
            if(self.xPosition<0):
                self.xPosition=0
            if(self.yPosition<0):
                self.yPosition=0
            if(self.xPosition>511):
                self.xPosition=511
            if(self.yPosition>511):
                self.yPosition=511
            self.setIsClicked(True)
        e.ignore()




