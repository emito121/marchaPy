from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import sys
from PyQt5.QtWidgets import QApplication

class Rodilla(QDialog):
    def __init__(self, imagen):
        QDialog.__init__(self)
        uic.loadUi("rodilla.ui", self)
        self.video.setScene(imagen)
    
    def angulo(self, angulo):
        self.labelAngulo.setText(f'Ángulo de la rodilla: {angulo}')

# #app = QApplication(sys.argv)
# _ventana = Rodilla()
# _ventana.show()
# app.exec_()