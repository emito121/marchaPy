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
#from controlPrincipal import mainWindow

class MainWindow2(QDialog):
    
    def __init__(self, camara2use = [0,1]):
        super().__init__()
        uic.loadUi("interfazdoscamaras.ui", self)
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.Graph = False
        self.Worker1 = Worker1(camara2use)
        self.Worker1.start()
        self.Worker1.ImageUpdate1.connect(self.ImageUpdateSlot1)
        self.Worker1.ImageUpdate2.connect(self.ImageUpdateSlot2)
        self.Worker1.labelRodillaUpdate.connect(self.labelRodillaUpdate)
        self.Worker1.labelCaderaUpdate.connect(self.labelCaderaUpdate)
        self.Worker1.muestreoRodilla.connect(self.graphRodilla)
        self.Worker1.muestreoCadera.connect(self.graphCadera)
        self.btnStart.clicked.connect(self.comenzarAnalisis)
        self.btnStop.clicked.connect(self.detenerAnalisis)
        self.traces = dict()
        pg.setConfigOptions(antialias=True)
        self.camara2use = camara2use

    def comenzarAnalisis(self):
        self.Graph = True
        self.Worker1.graficar = True
    
    def detenerAnalisis(self):
        self.Graph = False
    
    def ImageUpdateSlot1(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))
    
    def ImageUpdateSlot2(self, Image):
        self.FeedLabel_2.setPixmap(QPixmap.fromImage(Image))

    def labelRodillaUpdate(self, Label):
        self.labelAnguloRodilla.setText(f'Ángulo de la rodilla: {Label}°')
    
    def labelCaderaUpdate(self, Label):
        self.labelAnguloCadera.setText(f'Ángulo de la cadera: {Label}°')

    def CancelFeed(self):
        self.Worker1.cap1.release()
        self.Worker1.cap2.release()
        self.close()
        #mainWindow().exec_
    
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
    
    ImageUpdate1 = pyqtSignal(QImage)
    ImageUpdate2 = pyqtSignal(QImage)
    labelRodillaUpdate = pyqtSignal(str)
    labelCaderaUpdate = pyqtSignal(str)
    muestreoRodilla = pyqtSignal(str, list, list)
    muestreoCadera = pyqtSignal(str, list, list)
    
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
        self.cap1 = cv2.VideoCapture(camara2use[0])
        self.cap2 = cv2.VideoCapture(camara2use[1])
    
    def update(self):
        self.muestreoRodilla.emit('rodilla',self.tiempos,self.angulosRodilla)
        self.muestreoCadera.emit('cadera',self.tiempos, self.angulosCadera)
    
    def run(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose
        # cap1 = cv2.VideoCapture(self.camara2use[0])
        # cap2 = cv2.VideoCapture(self.camara2use[1])
        self.ThreadActive = True
        timeSample1 = time.time()
        timePlot1 = time.time()
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5, model_complexity = 0) as pose1:
            with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5, model_complexity = 0) as pose2:
                while self.cap1.isOpened():
                    ret1, frame1 = self.cap1.read()
                    ret2, frame2 = self.cap2.read()
                
                    # Recolor image to RGB
                    image1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
                    image1.flags.writeable = False
                    
                    results1 = pose1.process(image1)

                    image1.flags.writeable = True

                    image2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
                    image2.flags.writeable = False
                    
                    results2 = pose2.process(image2)

                    image2.flags.writeable = True

                    try:
                        landmarks = results1.pose_landmarks.landmark
                        
                        # Get coordinatesRIGHT_HIP, RIGHT_KNEE, RIGHT_ANKLE
                        cadera = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                        rodilla = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                        tobillo = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                        
                        hombro = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                        cadera = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                        rodilla = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                        
                        # Calculate angle
                        self.anguloRodilla1 = self.calculate_angle(cadera, rodilla, tobillo)
                        self.anguloCadera1 = self.calculate_angle(hombro, cadera, rodilla)
                    
                    except:
                        pass
                    
                    # Render detections
                    mp_drawing.draw_landmarks(image1, results1.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                            mp_drawing.DrawingSpec(color=(255,255,0), thickness=2, circle_radius=2), 
                                            mp_drawing.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=2)
                                            )

                    try:
                        landmarks = results2.pose_landmarks.landmark
                        
                        # Get coordinatesRIGHT_HIP, RIGHT_KNEE, RIGHT_ANKLE
                        cadera = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                        rodilla = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                        tobillo = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                        
                        hombro = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                        cadera = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                        rodilla = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                        
                        # Calculate angle
                        self.anguloRodilla2 = self.calculate_angle(cadera, rodilla, tobillo)
                        self.anguloCadera2 = self.calculate_angle(hombro, cadera, rodilla)
                    
                    except:
                        pass
                    
                    # Render detections
                    mp_drawing.draw_landmarks(image2, results2.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                            mp_drawing.DrawingSpec(color=(255,255,0), thickness=2, circle_radius=2), 
                                            mp_drawing.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=2)
                                            )  

                    #FlippedImage = cv2.flip(image, 1)
                    FlippedImage1 = image1
                    ConvertToQtFormat = QImage(FlippedImage1.data, FlippedImage1.shape[1], FlippedImage1.shape[0], QImage.Format_RGB888)
                    Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    self.ImageUpdate1.emit(Pic)
                    self.labelRodillaUpdate.emit(str(self.anguloRodilla))
                    self.labelCaderaUpdate.emit(str(self.anguloCadera))
                    FlippedImage2 = image2
                    ConvertToQtFormat = QImage(FlippedImage2.data, FlippedImage2.shape[1], FlippedImage2.shape[0], QImage.Format_RGB888)
                    Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    self.ImageUpdate2.emit(Pic)

                    timeSample2 = time.time()
                    if ((timeSample2 - timeSample1) > 1):
                        
                        self.tiempos.append(self.tiempo)
                        self.angulosRodilla.append(self.anguloRodilla)
                        self.angulosCadera.append(self.anguloCadera)
                        self.muestreoRodilla.emit('rodilla',self.tiempos, self.angulosRodilla)
                        self.muestreoCadera.emit('cadera',self.tiempos, self.angulosCadera)
                        self.tiempo = self.tiempo+1
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
# Root = MainWindow2()
# Root.show()
# App.exec_()