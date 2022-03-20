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
import pickle
import io
import os
from datetime import date
from os import listdir, path, startfile, stat

class MainWindow1(QDialog):
    
    def __init__(self, camara2use = 0):
        super().__init__()
        uic.loadUi("rodilla.ui", self)
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.Graph = False
        self.Worker1 = Worker1(camara2use)
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.Worker1.labelRodillaUpdate.connect(self.labelRodillaUpdate)
        self.Worker1.labelCaderaUpdate.connect(self.labelCaderaUpdate)
        self.Worker1.muestreoRodilla.connect(self.graphRodilla)
        self.Worker1.muestreoCadera.connect(self.graphCadera)
        self.Worker1.saveData.connect(self.saveData)
        self.btnStart.clicked.connect(self.comenzarAnalisis)
        self.btnStop.clicked.connect(self.detenerAnalisis)
        self.traces = dict()
        pg.setConfigOptions(antialias=True)

    def comenzarAnalisis(self):
        self.Graph = True
        self.Worker1.graficar = True
    
    def detenerAnalisis(self):
        self.Graph = False
    
    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def labelRodillaUpdate(self, Label):
        self.labelAnguloRodilla.setText(f'Ángulo de la rodilla: {Label}°')
    
    def labelCaderaUpdate(self, Label):
        self.labelAnguloCadera.setText(f'Ángulo de la cadera: {Label}°')

    def CancelFeed(self):
        self.Worker1.cap.release()
        self.close()
    
    def saveData(self, datos, conexiones, tiempo):
        if self.Graph:
            if (f'{date.today()}' in listdir(f'{path.abspath(os.getcwd())}/resultados1Chands')):
                fichero = open(f'resultados1CHands/{date.today()}', 'ab')
                pickle.dump([datos, conexiones, tiempo],fichero)
                fichero.close()
            else:   
                fichero = open(f'resultados1CHands/{date.today()}', 'wb')
                pickle.dump([datos, conexiones, tiempo],fichero)
                fichero.close()

    def graphRodilla(self, name, dataset_x, dataset_y):
        if self.Graph:
            if name in self.traces:
                self.traces[name].setData(dataset_x,dataset_y)
            else:
                self.traces[name] = self.graphicsView.plot(pen='y')
    
    def graphCadera(self, name, dataset_x, dataset_y):
        if self.Graph:
            if name in self.traces:
                self.traces[name].setData(dataset_x,dataset_y)
            else:
                self.traces[name] = self.graphicsCadera.plot(pen='r')

class Worker1(QThread):
    
    ImageUpdate = pyqtSignal(QImage)
    labelRodillaUpdate = pyqtSignal(str)
    labelCaderaUpdate = pyqtSignal(str)
    muestreoRodilla = pyqtSignal(str, list, list)
    muestreoCadera = pyqtSignal(str, list, list)
    saveData = pyqtSignal(object, object, float)
    
    def __init__(self, camara2use):
        super().__init__()
        self.tiempos = []
        self.tiempo = 0
        self.angulosRodilla = []
        self.angulosCadera = []
        self.anguloRodilla = 0
        self.anguloCadera = 0
        self.contadorTiempo = []
        self.graficar = False
        self.cap = cv2.VideoCapture(camara2use[0])
    
    def update(self):
        self.muestreoRodilla.emit('rodilla',self.tiempos,self.angulosRodilla)
        self.muestreoCadera.emit('cadera',self.tiempos, self.angulosCadera)  
    
    def run(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose
        # cap = cv2.VideoCapture(self.camara2use[0])
        self.ThreadActive = True
        timeSample1 = time.time()
        timePlot1 = time.time()
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5,model_complexity = 0) as pose:
            while self.cap.isOpened():
                angleRodilla = 0
                angleCadera = 0
                ret, frame = self.cap.read()
            
                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                
                results = pose.process(image)

                image.flags.writeable = True

                try:
                    landmarks = results.pose_landmarks.landmark
                    
                    # Get coordinatesRIGHT_HIP, RIGHT_KNEE, RIGHT_ANKLE
                    cadera = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    rodilla = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    tobillo = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                    
                    hombro = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    cadera = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    rodilla = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    
                    # Calculate angle
                    self.anguloRodilla = self.calculate_angle(cadera, rodilla, tobillo)
                    self.anguloCadera = self.calculate_angle(hombro, cadera, rodilla)
                
                except:
                    pass
                
                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(255,255,0), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=2)
                                        )

                #FlippedImage = cv2.flip(image, 1)
                #mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
                FlippedImage = image
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
                self.labelRodillaUpdate.emit(str(self.anguloRodilla))
                self.labelCaderaUpdate.emit(str(self.anguloCadera))
                
                timeSample2 = time.time()
                if ((timeSample2 - timeSample1) > 0.1):
                    
                    self.tiempos.append(self.tiempo)
                    self.angulosRodilla.append(self.anguloRodilla)
                    self.angulosCadera.append(self.anguloCadera)
                    self.muestreoRodilla.emit('rodilla',self.tiempos, self.angulosRodilla)
                    self.muestreoCadera.emit('cadera',self.tiempos, self.angulosCadera)
                    self.saveData.emit(results.pose_landmarks, mp_pose.POSE_CONNECTIONS, self.tiempo)
                    self.tiempo = self.tiempo+0.1
                    timeSample1 = timeSample2
                
    def stop(self):
        self.ThreadActive = False
        self.quit()

    def calculate_angle(self,a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle >180.0:
            angle = 360-angle
            
        return abs(angle-180)

# App = QApplication(sys.argv)
# Root = MainWindow1()
# Root.show()
# App.exec_()