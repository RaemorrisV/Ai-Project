from PyQt5.QtWidgets import QApplication, QFileDialog, QStyleFactory, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5 import uic
import cv2 as cv
import numpy as np
import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import mediapipe as mp
from PyQt5.QtCore import QCoreApplication, QThread, Qt, pyqtSignal, pyqtSlot

form_thirdwindow = uic.loadUiType("squat.ui")[0]  # 두 번째창 ui


class squat_thread(QThread):
    mp_pose = mp.solutions.pose
    consum_calorie = 0  # 70kg 남성을 기준으로 하여 계산할 예정입니다
    count = 0
    status = '일어섰음'
    updateText = pyqtSignal(str)
    updateText_status = pyqtSignal(str)
    updateText_consume = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.updateText.connect(self.parent.count1.setText)
        self.updateText_status.connect(self.parent.status1.setText)
        self.updateText_consume.connect(self.parent.conume1.setText)

    def run(self):
        mp_drawing = mp.solutions.drawing_utils
        mp_styles = mp.solutions.drawing_styles
        pose = self.mp_pose.Pose(
            min_detection_confidence=0.5, min_tracking_confidence=0.5)
        cap = cv.VideoCapture(0, cv.CAP_DSHOW)
        width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.parent.label.resize(width, height)
        while cap.isOpened():
            ret, img = cap.read()
            img = cv.flip(img, 1)
            if ret:
                res = pose.process(cv.cvtColor(img, cv.COLOR_BGR2RGB))
                try:
                    landmarks = res.pose_landmarks.landmark
                    self.count, self.status, self.consum_calorie = self.squat1(
                        self.count, self.status, self.consum_calorie, landmarks)
                    self.updateText.emit(str(self.count))
                    self.updateText_status.emit(str(self.status))
                    self.updateText_consume.emit(
                        str(format(self.consum_calorie, ".1f")))
                    text = "{}:{}".format("SQUATs", self.count)
                    cv.putText(img, text, (10, 40),
                               cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                except:
                    pass

                mp_drawing.draw_landmarks(img, res.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                          landmark_drawing_spec=mp_styles.get_default_pose_landmarks_style())
                img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
                h, w, c = img.shape
                qImg = QtGui.QImage(
                    img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImg)
                self.parent.label.setPixmap(pixmap)

            else:
                QtWidgets.QMessageBox.about(
                    self.parent.win, "Error", "Cannot read frame.")
                print("cannot read frame.")
                break
        cap.release()
        print("Thread end.")

    def read_body_partX_Y(self, landmarks, body_part_name):
        return [
            landmarks[self.mp_pose.PoseLandmark[body_part_name].value].x,
            landmarks[self.mp_pose.PoseLandmark[body_part_name].value].y,
            landmarks[self.mp_pose.PoseLandmark[body_part_name].value].visibility
        ]

    def calculate_angle(self, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - \
            np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle

    def angle_of_the_left_leg(self, landmarks):
        l_hip = self.read_body_partX_Y(landmarks, "LEFT_HIP")
        l_knee = self.read_body_partX_Y(landmarks, "LEFT_KNEE")
        l_ankle = self.read_body_partX_Y(landmarks, "LEFT_ANKLE")
        return self.calculate_angle(l_hip, l_knee, l_ankle)

    def angle_of_the_right_leg(self, landmarks):
        r_hip = self.read_body_partX_Y(landmarks, "RIGHT_HIP")
        r_knee = self.read_body_partX_Y(landmarks, "RIGHT_KNEE")
        r_ankle = self.read_body_partX_Y(landmarks, "RIGHT_ANKLE")
        return self.calculate_angle(r_hip, r_knee, r_ankle)

    def squat1(self, counter, status, consum, landmarks):
        left1 = self.angle_of_the_right_leg(landmarks)
        right1 = self.angle_of_the_left_leg(landmarks)
        avg_leg_angle = (left1 + right1) // 2

        if status == '일어섰음':
            if avg_leg_angle < 100:
                counter += 1
                consum += 0.4
                status = '앉았음'
        else:
            if avg_leg_angle > 160:
                status = '일어섰음'

        return [counter, status, consum]


class thirdwindow(QDialog, QWidget, form_thirdwindow):
    def __init__(self):
        super(thirdwindow, self).__init__()
        self.initUI()
        self.show()  # 두번째창 실행

    def initUI(self):
        self.setupUi(self)
        self.backhome1.clicked.connect(self.Home)
        self.on1.clicked.connect(self.start)
        self.count1.setFontPointSize(25)
        self.status1.setFontPointSize(22)
        self.conume1.setFontPointSize(25)

    def Home(self):
        self.close()

    def start(self):
        h2 = squat_thread(self)
        h2.start()
        print("started..")
