#!/usr/bin/python
from Bpm import getBpm
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QComboBox, QLabel
import PyQt5.QtGui
from PyQt5.QtCore import pyqtSlot
 
class App(QWidget):
 
    Bpm = 0
    AudioPath = ""
    Key = ""
    Tonality = ""

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
 
        self.lbl1 = QLabel("select audio file", self)
        self.lbl1.move(150, 30)
        button = QPushButton('Select audio', self)
        button.setToolTip('select audio file to use')
        button.move(20,30) 
        button.clicked.connect(self.openFileNameDialog)
        
        self.lbl2 = QLabel("Generate Bpm", self)
        self.lbl2.move(150, 60)
        button = QPushButton('Generate Bpm', self)
        button.setToolTip('genereates bpm for selected audio')
        button.move(20,60) 
        button.clicked.connect(self.on_click)

        self.lbl3 = QLabel("Key", self)

        comboKey = QComboBox(self)
        comboKey.addItem("A")
        comboKey.addItem("A#")
        comboKey.addItem("B")
        comboKey.addItem("C")
        comboKey.addItem("C#")
        comboKey.addItem("D")
        comboKey.addItem("D#")
        comboKey.addItem("E")
        comboKey.addItem("F")
        comboKey.addItem("F#")
        comboKey.addItem("G")
        comboKey.addItem("G#")

        comboKey.move(20, 90)
        self.lbl3.move(150, 90)
        comboKey.activated[str].connect(self.setKey) 

        self.lbl4 = QLabel("Tonality", self)

        comboT = QComboBox(self)
        comboT.addItem("Major")
        comboT.addItem("Minor")

        comboT.move(20, 120)
        self.lbl4.move(150, 120)
        comboT.activated[str].connect(self.setTone) 

        #ToDo add play button that will simply play the scale selected for now
         

        self.show()
 

    def setKey(self, text):
        self.lbl3.setText(text)
        self.lbl3.adjustSize() 
        global Key
        Key = text

    def setTone(self, text):
        self.lbl4.setText(text)
        self.lbl4.adjustSize() 
        global Tonality
        Tonality=text

    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            global AudioPath
            self.lbl1.setText(fileName)
            self.lbl3.adjustSize() 
            AudioPath = fileName
 
    def on_click(self):
        global AudioPath
        global Bpm 
        Bpm = getBpm(AudioPath)
        self.lbl2.setText(str(Bpm))
        self.lbl2.adjustSize() 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())



