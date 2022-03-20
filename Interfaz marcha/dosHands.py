import cv2
import mediapipe as mp
import sys
from pyqtgraph.Qt import QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
from PyQt5 import uic
import time
import pyqtgraph as pg

class MainWindowHands2(QDialog):
    
    def __init__(self, camara2use = [0,1]):
        super().__init__()
        uic.loadUi("doscamarasHands.ui", self)
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.Worker1 = Worker1(camara2use)
        self.Worker1.start()
        self.Worker1.ImageUpdate1.connect(self.ImageUpdateSlot1)
        self.Worker1.ImageUpdate2.connect(self.ImageUpdateSlot2)
    
    def ImageUpdateSlot1(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))
    
    def ImageUpdateSlot2(self, Image):
        self.FeedLabel_2.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.Worker1.cap1.release()
        self.Worker1.cap2.release()
        self.close()

class Worker1(QThread):
    
    ImageUpdate1 = pyqtSignal(QImage)
    ImageUpdate2 = pyqtSignal(QImage)
    
    def __init__(self, camara2use):
        super().__init__()
        self.cap1 = cv2.VideoCapture(camara2use[0])
        self.cap2 = cv2.VideoCapture(camara2use[1])

    def run(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands

        with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands1:
            with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands2:
                while self.cap1.isOpened():
                    success1, image1 = self.cap1.read()
                    success2, image2 = self.cap2.read()

                    image1.flags.writeable = False
                    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
                    results1 = hands1.process(image1)
                    image1.flags.writeable = True

                    if results1.multi_hand_landmarks:
                        for hand_landmarks in results1.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                image1,
                                hand_landmarks,
                                mp_hands.HAND_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(255,255,0), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=2))
 
                    ConvertToQtFormat = QImage(image1.data, image1.shape[1], image1.shape[0], QImage.Format_RGB888)
                    Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    self.ImageUpdate1.emit(Pic)

                    image2.flags.writeable = False
                    image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
                    results2 = hands2.process(image2)
                    image2.flags.writeable = True

                    if results2.multi_hand_landmarks:
                        for hand_landmarks in results2.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(
                                image2,
                                hand_landmarks,
                                mp_hands.HAND_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(255,255,0), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=2))
 
                    ConvertToQtFormat = QImage(image2.data, image2.shape[1], image2.shape[0], QImage.Format_RGB888)
                    Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    self.ImageUpdate2.emit(Pic)

# App = QApplication(sys.argv)
# Root = MainWindowHands()
# Root.show()
# App.exec_()