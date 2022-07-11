import sys
import cv2 as cv
import mediapipe as mp
from PyQt5.QtWidgets import QApplication, QFileDialog, QStyleFactory, QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication, QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5 import QtGui
from PyQt5 import QtCore
import push_up
import squat
import information_

form_class = uic.loadUiType("main.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.push_up.clicked.connect(self.push_upFunction)
        self.squat.clicked.connect(self.squatFunction)
        self.exit.clicked.connect(self.exitFunction)
        self.information.clicked.connect(self.infor)

    def exitFunction(self):
        exit.clicked.connect(QCoreApplication.instance().quit)

    def push_upFunction(self):
        self.hide()  # 메인 윈도우 숨김
        self.second = push_up.secondwindow()
        self.second.exec()  # 두번째창 닫을때까지 기다림
        self.show()  # 두번째창 닫으면 다시 첫 번째 창 보여 짐

    def squatFunction(self):
        self.hide()  # 메인 윈도우 숨김
        self.second = squat.thirdwindow()
        self.second.exec()  # 두번째창 닫을때까지 기다림
        self.show()  # 두번째창 닫으면 다시 첫 번째 창 보여 짐

    def infor(self):
        self.hide()  # 메인 윈도우 숨김
        self.second = information_.informationwindow()
        self.second.exec()  # 두번째창 닫을때까지 기다림
        self.show()  # 두번째창 닫으면 다


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
