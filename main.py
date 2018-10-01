#!/usr/bin/python
from Bpm import getBpm
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
 
class App(QWidget):
 
    AudioPath = ""

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        button = QPushButton('Select audio', self)
        button.setToolTip('select audio file to use')
        button.move(100,140) 
        button.clicked.connect(self.openFileNameDialog)
        
        button = QPushButton('Generate Bpm', self)
        button.setToolTip('genereates bpm for selected audio')
        button.move(100,70) 
        button.clicked.connect(self.on_click)

        self.show()
 
    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            global AudioPath
            AudioPath = fileName
 
    def on_click(self):
        #audioPath = 'test.mp3'
        global AudioPath
        print (getBpm(AudioPath))
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())



