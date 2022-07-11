from PyQt5.QtWidgets import QApplication, QFileDialog, QStyleFactory, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

form_inforwindow = uic.loadUiType("infor.ui")[0]  # 두 번


class informationwindow(QDialog, QWidget, form_inforwindow):
    def __init__(self):
        super(informationwindow, self).__init__()
        self.initUI()
        self.show()  # 두번째창 실행

    def initUI(self):
        self.setupUi(self)
        self.backpage.clicked.connect(self.Home)

    def Home(self):
        self.close()
