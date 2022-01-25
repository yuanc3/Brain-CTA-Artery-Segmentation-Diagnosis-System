import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
class MyLabel(QLabel):

    def __init__(self, text, connect=0,number=0):
        super().__init__(text)
        self.x = 0
        self.y= 0
        self.xPosition=0
        self.yPosition=0
        self.connect=connect
        self.number=number

    def mousePressEvent(self, e):
        self.x=e.x()
        self.y=e.y()
        if self.connect:
            self.xPosition = round(self.x * (512.0 / self.width()))
            self.yPosition = round(self.y * (512.0 / self.height()))
            self.connect[0].setText("X: "+str(self.xPosition))
            self.connect[1].setText("Y: " + str(self.yPosition))
        e.ignore()
    def mouseMoveEvent(self, e):
        self.x=e.x()
        self.y=e.y()
        if self.connect:
            self.xPosition = round(self.x * (512.0 / self.width()))
            self.yPosition = round(self.y * (512.0 / self.height()))
            self.connect[0].setText("X: "+str(self.xPosition))
            self.connect[1].setText("Y: " + str(self.yPosition))
        e.ignore()


