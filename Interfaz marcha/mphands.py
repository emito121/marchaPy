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

class MainWindowHands(QDialog):
    
    def __init__(self, camara2use = 0):
        super().__init__()
        uic.loadUi("manos.ui", self)
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.Graph = False
        self.Worker1 = Worker1(camara2use)
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        pg.setConfigOptions(antialias=True)
    
    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.Worker1.cap.release()
        self.close()

class Worker1(QThread):
    
    ImageUpdate = pyqtSignal(QImage)
    
    def __init__(self, camara2use):
        super().__init__()
        self.cap = cv2.VideoCapture(camara2use[0])

    def run(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands

        # cap = cv2.VideoCapture(self.camara2use[0])
        with mp_hands.Hands(
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
            while self.cap.isOpened():
                success, image = self.cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)

                # Draw the hand annotations on the image.
                image.flags.writeable = True
                # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(255,255,0), thickness=2, circle_radius=2), 
                            mp_drawing.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=2))

                ConvertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)

# App = QApplication(sys.argv)
# Root = MainWindowHands()
# Root.show()
# App.exec_()