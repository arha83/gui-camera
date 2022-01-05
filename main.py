from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
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

    def updateFrame(self):
        frame= self.stream.frame
        height, width= frame.shape[0], frame.shape[1]

        self.setFixedSize(width+20, height+20)
        self.imageFrame.setGeometry(10,10, width,height)
        
        image= QImage(frame.data, width, height, QImage.Format.Format_RGB888).rgbSwapped()
        self.imageFrame.setPixmap(QPixmap.fromImage(image))




app= QApplication(sys.argv)
win= Window()
win.show()
sys.exit(app.exec_())