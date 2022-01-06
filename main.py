from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
import cv2 as cv
import sys
import time


class Streamer(QObject):
    frameSig= pyqtSignal()
    def run(self):
        capture= cv.VideoCapture(0)
        while True:
            _, self.frame= capture.read()
            self.frameSig.emit()
            time.sleep(1/30)


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.streaming= False
        self.frameText= ''
        self.initUI()

    def initUI(self):
        
        self.imageFrame= QtWidgets.QLabel(self)

        self.thr= QThread()
        self.stream= Streamer()
        self.stream.moveToThread(self.thr)

        self.thr.started.connect(self.stream.run)
        self.thr.finished.connect(self.thr.deleteLater)
        self.stream.frameSig.connect(self.updateFrame)

        self.thr.start()

        self.startBtn= QtWidgets.QPushButton(self)
        self.stopBtn= QtWidgets.QPushButton(self)
        self.writeBtn= QtWidgets.QPushButton(self)
        self.startBtn.setText('start')
        self.stopBtn.setText('stop')
        self.writeBtn.setText('write')
        self.startBtn.clicked.connect(self.startStream)
        self.stopBtn.clicked.connect(self.stopStream)
        self.writeBtn.clicked.connect(self.addText)

        self.textInput= QtWidgets.QLineEdit(self)

    def updateFrame(self):
        frame= self.stream.frame
        height, width= frame.shape[0], frame.shape[1]

        self.setFixedSize(width+20, height+20)
        self.imageFrame.setGeometry(10,10, width,height)
        
        if self.streaming:
            image= QImage(frame.data, width, height, QImage.Format.Format_RGB888).rgbSwapped()
            self.imageFrame.setPixmap(QPixmap.fromImage(image))

    def startStream(self):
        self.streaming= True
    
    def stopStream(self):
        self.streaming= False

    def addText(self):
        self.frameText= self.textInput.text() 


app= QApplication(sys.argv)
win= Window()
win.show()
sys.exit(app.exec_())