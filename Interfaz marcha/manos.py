# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'manos.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(541, 255)
        Dialog.setToolTipDuration(0)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.FeedLabel = QtWidgets.QLabel(Dialog)
        self.FeedLabel.setText("")
        self.FeedLabel.setObjectName("FeedLabel")
        self.verticalLayout.addWidget(self.FeedLabel)
        self.CancelBTN = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.CancelBTN.setFont(font)
        self.CancelBTN.setStyleSheet("QPushButton{background-color:skyblue;}\n"
"QPushButton:hover{background-color:orange;}")
        self.CancelBTN.setObjectName("CancelBTN")
        self.verticalLayout.addWidget(self.CancelBTN)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Marcha4Cam - Una Cámara Manos"))
        self.label.setText(_translate("Dialog", "Interfaz Manos"))
        self.CancelBTN.setText(_translate("Dialog", "Cerrar"))
