import sys
from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import mediapipe as mp
import numpy as np
from PyQt5 import uic
import time
import pyqtgraph as pg
from interfazdoscam import MainWindow2
from interfazv2 import MainWindow1
from mphands import MainWindowHands
from dosHands import MainWindowHands2

class mainWindow(QDialog):    
    def __init__(self):
        super().__init__()
        uic.loadUi("mainWindow.ui", self)
        self.btnStart.clicked.connect(self.start)
        self.btnClose.clicked.connect(self.stop)
        self.Worker1 = Worker()
        self.Worker1.start()
        self.Worker1.ImageUpdate0.connect(self.ImageUpdateSlot0)
        self.Worker1.ImageUpdate1.connect(self.ImageUpdateSlot1)
        self.Worker1.ImageUpdate2.connect(self.ImageUpdateSlot2)
        self.Worker1.ImageUpdate3.connect(self.ImageUpdateSlot3)
    
    def ImageUpdateSlot0(self, Image):
        self.FeedLabel0.setPixmap(QPixmap.fromImage(Image))

    def ImageUpdateSlot1(self, Image):
        self.FeedLabel1.setPixmap(QPixmap.fromImage(Image))
    
    def ImageUpdateSlot2(self, Image):
        self.FeedLabel2.setPixmap(QPixmap.fromImage(Image))

    def ImageUpdateSlot3(self, Image):
        self.FeedLabel3.setPixmap(QPixmap.fromImage(Image))


    def start(self):
        camaras = []
        if self.checkBox0.isChecked():
            camaras.append(0)
        if self.checkBox1.isChecked():
            camaras.append(1)
        if self.checkBox2.isChecked():
            camaras.append(2)
        if self.checkBox3.isChecked():
            camaras.append(3)
        
        if self.comboBox.currentText() == 'Marcha':
            if len(camaras) > 2:
                self.labelError.setText('No debe seleccionar más de dos cámaras')
            if len(camaras) == 0:
                self.labelError.setText('Debe seleccionar al menos una cámara')
            if len(camaras) == 1:
                self.Worker1.cap0.release()
                self.Worker1.cap1.release()
                self.Worker1.cap2.release()
                self.Worker1.cap3.release()
                self.close()
                MainWindow1(camaras).exec_()
            if len(camaras) == 2:
                self.Worker1.cap0.release()
                self.Worker1.cap1.release()
                self.Worker1.cap2.release()
                self.Worker1.cap3.release()
                self.close()
                MainWindow2(camaras).exec_()
        
        if self.comboBox.currentText() == 'Manos':
            if len(camaras) > 2:
                self.labelError.setText('No debe seleccionar más de dos cámaras')
            if len(camaras) == 0:
                self.labelError.setText('Debe seleccionar al menos una cámara')
            if len(camaras) == 1:
                self.Worker1.cap0.release()
                self.Worker1.cap1.release()
                self.Worker1.cap2.release()
                self.Worker1.cap3.release()
                self.close()
                MainWindowHands(camaras).exec_()
            if len(camaras) == 2:
                self.Worker1.cap0.release()
                self.Worker1.cap1.release()
                self.Worker1.cap2.release()
                self.Worker1.cap3.release()
                self.close()
                MainWindowHands2(camaras).exec_()

    def stop(self):
        self.Worker1.cap0.release()
        self.Worker1.cap1.release()
        self.Worker1.cap2.release()
        self.Worker1.cap3.release()
        self.close()

class Worker(QThread):
    
    ImageUpdate0 = pyqtSignal(QImage)
    ImageUpdate1 = pyqtSignal(QImage)
    ImageUpdate2 = pyqtSignal(QImage)
    ImageUpdate3 = pyqtSignal(QImage)
    
    def __init__(self):
        super().__init__()
        self.cap0 = cv2.VideoCapture(0)
        self.cap1 = cv2.VideoCapture(1)
        self.cap2 = cv2.VideoCapture(2)
        self.cap3 = cv2.VideoCapture(3)
    
    def run(self):
        self.ThreadActive = True

        while self.cap1.isOpened():
            ret0, frame0 = self.cap0.read()
            ret1, frame1 = self.cap1.read()
            ret2, frame2 = self.cap2.read()
            ret3, frame3 = self.cap3.read()
        
            # Recolor image to RGB
            image0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2RGB)            
            image1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            image2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)            
            image3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2RGB)             

            ConvertToQtFormat = QImage(image0.data, image0.shape[1], image0.shape[0], QImage.Format_RGB888)
            Pic = ConvertToQtFormat.scaled(320, 220, Qt.KeepAspectRatio)
            self.ImageUpdate0.emit(Pic)
            ConvertToQtFormat = QImage(image1.data, image1.shape[1], image1.shape[0], QImage.Format_RGB888)
            Pic = ConvertToQtFormat.scaled(320, 220, Qt.KeepAspectRatio)
            self.ImageUpdate1.emit(Pic)
            ConvertToQtFormat = QImage(image2.data, image2.shape[1], image2.shape[0], QImage.Format_RGB888)
            Pic = ConvertToQtFormat.scaled(320, 220, Qt.KeepAspectRatio)
            self.ImageUpdate2.emit(Pic)
            ConvertToQtFormat = QImage(image3.data, image3.shape[1], image3.shape[0], QImage.Format_RGB888)
            Pic = ConvertToQtFormat.scaled(320, 220, Qt.KeepAspectRatio)
            self.ImageUpdate3.emit(Pic)

App = QApplication(sys.argv)
Root = mainWindow()
Root.show()
App.exec_()