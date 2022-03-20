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

class MainWindow(QDialog):
    
    def __init__(self):
        super().__init__()
        uic.loadUi("rodilla.ui", self)
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.Graph = False
        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.Worker1.labelRodillaUpdate.connect(self.labelRodillaUpdate)
        self.Worker1.labelCaderaUpdate.connect(self.labelCaderaUpdate)
        #self.Worker1.plot2d.connect(self.plot2d)
        self.Worker1.muestreoRodilla.connect(self.graphRodilla)
        self.Worker1.muestreoCadera.connect(self.graphCadera)
        self.btnStart.clicked.connect(self.comenzarAnalisis)
        self.btnStop.clicked.connect(self.detenerAnalisis)
        self.traces = dict()
        pg.setConfigOptions(antialias=True)

        #self.canvas = self.graphicsView

    # def trace(self,name,dataset_x,dataset_y):
    #     if name in self.traces:
    #         self.traces[name].setData(dataset_x,dataset_y)
    #     else:
    #         self.traces[name] = self.canvas.plot(pen='y')

    def comenzarAnalisis(self):
        self.Graph = True
        self.Worker1.graficar = True
    
    # def plot2d(self, landmarks, conections):
    #     mp.solutions.drawing_utils.plot_landmarks(landmarks, conections)
    
    def detenerAnalisis(self):
        self.Graph = False
    
    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def labelRodillaUpdate(self, Label):
        self.labelAnguloRodilla.setText(f'Ángulo de la rodilla: {Label}°')
    
    def labelCaderaUpdate(self, Label):
        self.labelAnguloCadera.setText(f'Ángulo de la cadera: {Label}°')

    def CancelFeed(self):
        self.close()
    
    def graphRodilla(self, name, dataset_x, dataset_y):
        if self.Graph:
            # print(tiempo)
            # print(Angle)
            try:
                #self.graphicsView.plot(tiempo, Angle, pen = 'r')
                self.graphicsView.upgrade(dataset_x, dataset_y, pen = 'y')
            except:
                self.graphicsView.plot(dataset_x, dataset_y, pen = 'y')
            # if name in self.traces:
            #     self.traces[name].setData(dataset_x,dataset_y)
            # else:
            #     try:
            #         self.traces[name] = self.graphicsView.upgrade(pen = 'y')
            #     except:
            #         self.traces[name] = self.graphicsView.plot(pen='y')
    
    def graphCadera(self, name, dataset_x, dataset_y):
        if self.Graph:
            # print(tiempo)
            # print(Angle)
            # try:
            #     #self.graphicsView.plot(dataset_x dataset_y, pen = 'r')
            #     self.graphicsCadera.upgrade(dataset_x, dataset_y, pen = 'r')
            # except:
            #     self.graphicsCadera.plot(dataset_x, dataset_y, pen = 'r')
            if name in self.traces:
                self.traces[name].setData(dataset_x,dataset_y)
            else:
                # try:
                #     self.traces[name] = self.graphicsCadera.upgrade(pen = 'r')
                # except:
                self.traces[name] = self.graphicsCadera.plot(pen='r')


# class Plot2D():
#     def __init__(self):
#         self.traces = dict()

#         #QtGui.QApplication.setGraphicsSystem('raster')
#         #self.app = QtGui.QApplication([])
#         #mw = QtGui.QMainWindow()
#         #mw.resize(800,800)

#         #self.win = pg.GraphicsWindow(title="Basic plotting examples")
#         #self.win.resize(1000,600)
#         #self.win.setWindowTitle('pyqtgraph example: Plotting')

#         # Enable antialiasing for prettier plots
#         pg.setConfigOptions(antialias=True)

#         self.canvas = self.win.addPlot(title="Pytelemetry")
        

#     # def start(self):
#     #     if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#     #         QtGui.QApplication.instance().exec_()

#     def trace(self,name,dataset_x,dataset_y):
#         if name in self.traces:
#             self.traces[name].setData(dataset_x,dataset_y)
#         else:
#             self.traces[name] = self.canvas.plot(pen='y')

class Worker1(QThread):
    
    ImageUpdate = pyqtSignal(QImage)
    #plot2d = pyqtSignal(LandmarkList,list)
    labelRodillaUpdate = pyqtSignal(str)
    labelCaderaUpdate = pyqtSignal(str)
    muestreoRodilla = pyqtSignal(str, list, list)
    muestreoCadera = pyqtSignal(str, list, list)
    # tiempo = []
    # angulosRodilla = []
    # angulosCadera = []
    # contadorTiempo = 0
    
    def __init__(self):
        super().__init__()
        self.tiempos = []
        self.tiempo = 0
        self.angulosRodilla = []
        self.angulosCadera = []
        self.anguloRodilla = 0
        self.anguloCadera = 0
        self.contadorTiempo = []
        self.graficar = False
    
    def update(self):
        #print(self.tiempo, self.angulosCadera, self.angulosRodilla)
        self.muestreoRodilla.emit('rodilla',self.tiempos,self.angulosRodilla)
        self.muestreoCadera.emit('cadera',self.tiempos, self.angulosCadera)
        #self.tiempo = self.tiempo + 0.05
        # self.angulosRodilla = []
        # self.angulosCadera = []
        # self.timePlot1 = timePlot2        
    
    def run(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose
        cap = cv2.VideoCapture(1)
        self.ThreadActive = True
        timeSample1 = time.time()
        timePlot1 = time.time()
        # tiempo = []
        # angulosRodilla = []
        # angulosCadera = []
        # contadorTiempo = 0
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                angleRodilla = 0
                angleCadera = 0
                ret, frame = cap.read()
            
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
                    print(landmarks)
                
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
                #self.plot2d.emit(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
                self.labelCaderaUpdate.emit(str(self.anguloCadera))
                #print(self.graficar)
                # if self.graficar:
                #     timer = QtCore.QTimer()
                #     timer.timeout.connect(self.update)
                #     timer.start(50)
                #     self.graficar = False
                #if Graph:
                timeSample2 = time.time()
                if ((timeSample2 - timeSample1) > 0.04):
                    #self.update()
                    self.tiempos.append(self.tiempo)
                    self.angulosRodilla.append(self.anguloRodilla)
                    self.angulosCadera.append(self.anguloCadera)
                    self.tiempo = self.tiempo+0.04
                    timeSample1 = timeSample2
                
                timePlot2 = time.time()
                if ((timePlot2 - timePlot1) > 1):
                    # self.muestreoRodilla.emit('rodilla',self.tiempos, self.angulosRodilla)
                    # self.muestreoCadera.emit('cadera',self.tiempos, self.angulosCadera)
                    self.update()
                    self.tiempos = []
                    self.angulosRodilla = []
                    self.angulosCadera = []
                    timePlot1 = timePlot2

                # p = Plot2D()
                # i = 0

                # def update():
                #     global p, i
                #     t = np.arange(0,3.0,0.01)
                #     s = sin(2 * pi * t + i)
                #     c = cos(2 * pi * t + i)
                #     p.trace("sin",t,s)
                #     p.trace("cos",t,c)
                #     i += 0.1

                
                
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

App = QApplication(sys.argv)
Root = MainWindow()
Root.show()
App.exec_()