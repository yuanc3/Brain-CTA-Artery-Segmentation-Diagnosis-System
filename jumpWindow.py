from PyQt5.QtWidgets import QMainWindow,QLabel,QWidget,QHBoxLayout
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QIcon
import base64
import os
from seg_ico import imglogo

class Process(QMainWindow):
    _processSignal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setFixedSize(700,120)
        #self.setGeometry(200, 300, 800, 600)
        tmp = open('in.ico', 'wb')
        tmp.write(base64.b64decode(imglogo))
        tmp.close()
        self.setWindowIcon(QIcon("in.ico"))
        os.remove('in.ico')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Help")
        self.setGeometry(600, 500, 500, 120)
        self.show()

        self.mainLayout=QHBoxLayout()
        self.mainlayout_widget = QWidget()
        self.mainlayout_widget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainlayout_widget)
        self.warningLabel=QLabel()
        self.warningLabel.setText("Unable to connect to the server, please contact the relevant personnel")
        self.mainLayout.addWidget(self.warningLabel)
        

