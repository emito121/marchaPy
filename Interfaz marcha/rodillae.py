import cv2
import mediapipe as mp
import numpy as np
import time
from interfaz import Rodilla
import sys
from PyQt5.QtWidgets import QApplication

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return abs(angle-180) 

def main(angulos, x):
    cap = cv2.VideoCapture(0)
    ## Setup mediapipe instance
    tiempo2 = time.time()
    # angulos = []
    # x = []
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinatesRIGHT_HIP, RIGHT_KNEE, RIGHT_ANKLE
                cadera = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                rodilla = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                tobillo = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                
                # Calculate angle
                angle = calculate_angle(cadera, rodilla, tobillo)
                # tiempo1 = time.time()

                # if (tiempo2 - tiempo1) > 0.001:
                #     tiempo2 = tiempo1   
                #     x.append(contador)
                #     angulos.append(angle)
                #     contador = contador + 0.001
                #     print(angle)

                # Visualize angle
                # cv2.putText(image, str(angle), 
                #             tuple(np.multiply(rodilla, [640, 480]).astype(int)), 
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                #                     )
                
                cv2.putText(image, str(angle), 
                            tuple([50, 50]), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                        
            except:
                pass
            
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(0,255,255), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
                                    )               

            #cv2.imshow('Mediapipe Feed', image)

            app = QApplication(sys.argv)
            _ventana = Rodilla(image)
            _ventana.angulo(angle)
            _ventana.show()
            app.exec_()

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    
    return angulos, x