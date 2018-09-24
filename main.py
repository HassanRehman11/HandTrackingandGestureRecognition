import sys
from PyQt5.QtWidgets import QDialog ,QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np
import pixMap, Morph, Trained,db
import time
import keyboard
import subprocess
class mouse(QMainWindow):
    def __init__(self):
        super(mouse,self).__init__()
        loadUi('recog.ui',self)
        self.roi=None
        self.thresh = None
        self.startCam.clicked.connect(self.start_webcam)
        self.stopCam.clicked.connect(self.stop_webcam)
        self.minhv.setNum(self.minH.value())
        self.minsv.setNum(self.minS.value())
        self.minvv.setNum(self.minV.value())
        self.maxhv.setNum(self.maxH.value())
        self.maxsv.setNum(self.maxS.value())
        self.maxvv.setNum(self.maxV.value())
        self.picO = pixMap.Pix()
        self.pic1 = pixMap.Pix()
        self.morph = Morph.Morph()
        self.data = Trained.Recog()
        self.db = db.sqlDB()
          
    @pyqtSlot()
    def start_webcam(self):
        self.capture=cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,381)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,351)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(0)
    @pyqtSlot()
    def stop_webcam(self):
        self.timer.stop()


    """@pyqtSlot()
    def start_Create(self):
        self.capture=cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,381)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,351)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.cap)
        self.timer.start(0)
    @pyqtSlot()
    def stop_Create(self):
        self.timer.stop()"""
    
    @pyqtSlot()
    def update(self):
        ret,img=self.capture.read()
        
        self.thresh= self.morph.ImgMorph(img,(self.minH.value(),self.minS.value(),self.minV.value()),(self.maxH.value(),self.maxS.value(),self.maxV.value()))
        im2, cont, her = cv2.findContours(self.thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        try:
            lala = self.morph.contour(self.thresh,cont)
            self.roi = cv2.resize(lala,(24,24))
            gesture, value = self.data.recognize(self.roi)
            output = self.db.search(gesture)
            perc = (int(value)/500)*100
            self.gestName.setText(output)
            self.gestPerc.setText(str(perc)+"%")
            if (output=="Leo"):
                subprocess.call('xdg-open MyScreenshot.png', shell=True)
                stop_webcam()
            if (output=="Hello World"):
                subprocess.call('scrot MyScreenshot.png', shell=True)
                stop_webcam()

        except:
            pass
        self.picO.display(self.thresh,self.imgRec)
    
        



        
app = QApplication(sys.argv)
window=mouse()
window.show()
sys.exit(app.exec_())
