from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import cv2


from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
import cv2
import numpy as np

class VideoFeed(QThread):
    ImageUpdate = pyqtSignal(np.ndarray)
    ThreadActive =True

    def run(self):
        self.ThreadActive = True 
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        while self.ThreadActive:
            ret, frame = self.cap.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(image, 1)
                self.ImageUpdate.emit(FlippedImage)

    def stop(self):
        self.ThreadActive = False
        self.cap.release()
        self.quit()
