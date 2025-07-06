
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from camera_feed import VideoFeed
from edge_detection_widget import Ui_edge_detection_widget
import cv2
import numpy as np

class UI_edge_detection_display(QWidget):
    def __init__(self,edge_detection_widget):
        super().__init__()

        self.DaddyWidget = edge_detection_widget
        self.VBL = QVBoxLayout()
        
        self.feedlabel = QLabel()
        self.feedlabel.setAlignment(Qt.AlignCenter)
        self.feedlabel.setScaledContents(True)
        self.VBL.addWidget(self.feedlabel)
        self.current_edge_algorithm=self.canny

        self.DaddyWidget.camera_radiobutton.setChecked(True)
        self.ShowVideo()

        self.minThreshold=50
        self.maxThreshold=200
        self.DaddyWidget.lcdNumber_1.setDigitCount(3)
        self.DaddyWidget.lcdNumber_1.display(self.minThreshold)
        self.DaddyWidget.lcdNumber_2.setDigitCount(3)
        self.DaddyWidget.lcdNumber_1.display(self.maxThreshold)
        self.DaddyWidget.lcdNumber_3.setDigitCount(3)
        self.DaddyWidget.horizontalSlider_1.setRange(0,255)
        self.DaddyWidget.horizontalSlider_1.setValue(self.minThreshold)
        self.DaddyWidget.horizontalSlider_2.setRange(0,255)
        self.DaddyWidget.horizontalSlider_2.setValue(self.maxThreshold)
        self.DaddyWidget.slider_label_1.setText("Min Threshold")
        self.DaddyWidget.slider_label_2.setText("Max Threshold")


        self.DaddyWidget.camera_radiobutton.toggled.connect(self.ShowVideo)
        self.DaddyWidget.systemfile_radiobutton.toggled.connect(self.ShowFileImage)
        self.DaddyWidget.edge_detection_algorithm_combobox.addItems(["CANNY","SOBEL_X","SOBEL_Y","SOBEL","SCHARR",'LAPLACIAN',"PREWITTS","ROBERT'S CROSSING"])
        self.DaddyWidget.edge_detection_algorithm_combobox.currentIndexChanged.connect(self.set_current_algorithm)
        self.DaddyWidget.select_file_button.clicked.connect(self.ShowFileImage)
        self.edge_algorithms=[self.canny,self.sobel_x,self.sobel_y,self.sobel,self.scharr,self.laplacian,self.prewitt,self.roberts]
        self.DaddyWidget.horizontalSlider_1.valueChanged.connect(self.update_slider_1_val)
        self.DaddyWidget.horizontalSlider_2.valueChanged.connect(self.update_slider_2_val)
        self.DaddyWidget.save_file_button.clicked.connect(self.save_img)
        self.DaddyWidget.click_image_button.clicked.connect(self.clicked_image)
        self.DaddyWidget.restore_button.clicked.connect(self.ShowVideo)
        

        # Set the layout
        self.setLayout(self.VBL)

    def clicked_image(self):
        if self.DaddyWidget.camera_radiobutton.isChecked():
            self.cancel_feed()

    def save_img(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "JPEG Files (*.jpg);;PNG Files (*.png);;All Files (*)")
    
        # Check if a valid file path was chosen
        if file_path:
            # Save the current image as PNG or JPEG using OpenCV
            cv2.imwrite(file_path, self.current_image)
            print(f"Image saved to {file_path}")
        

    def update_slider_1_val(self,value):
        self.minThreshold=value
        self.DaddyWidget.lcdNumber_1.display(value)
        if self.DaddyWidget.systemfile_radiobutton.isChecked():
            self.current_edge_algorithm(self.file_image)
    
    def update_slider_2_val(self,value):
        self.maxThreshold=value
        self.DaddyWidget.lcdNumber_2.display(value)
        if self.DaddyWidget.systemfile_radiobutton.isChecked():
            self.current_edge_algorithm(self.file_image)


    def set_current_algorithm(self,index):
        self.current_edge_algorithm=self.edge_algorithms[index]
        if index != 0:
            self.DaddyWidget.horizontalSlider_1.setEnabled(False)
            self.DaddyWidget.horizontalSlider_2.setEnabled(False)
        else:
            self.DaddyWidget.horizontalSlider_1.setEnabled(True)
            self.DaddyWidget.horizontalSlider_2.setEnabled(True)

        if self.DaddyWidget.systemfile_radiobutton.isChecked():
            self.current_edge_algorithm(self.file_image)


    
    def update_label(self,processed_image,technique):
        h, w = processed_image.shape 
        bytes_per_line = w  
        qt_image = QImage(processed_image.data, w, h, bytes_per_line, QImage.Format_Grayscale8)

        self.feedlabel.setPixmap(QPixmap.fromImage(qt_image).scaled(
            self.feedlabel.size(), Qt.IgnoreAspectRatio, technique))

    def update_label_smooth(self,processed_image):

        h, w = processed_image.shape 
        bytes_per_line = w  
        qt_image = QImage(processed_image.data, w, h, bytes_per_line, QImage.Format_Grayscale8)

        self.feedlabel.setPixmap(QPixmap.fromImage(qt_image).scaled(
            self.feedlabel.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))



    def canny(self, cv_image):
        edges = cv2.Canny(cv_image, self.minThreshold, self.maxThreshold)
        self.current_image=edges
        self.update_label(edges,Qt.SmoothTransformation)
    
    def sobel_x(self, cv_image):
        # Check if the input image is grayscale; if not, convert it to grayscale.
        if len(cv_image.shape) == 3:
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Apply Sobel operator in the x direction
        sobelx = cv2.Sobel(cv_image, cv2.CV_64F, 1, 0, ksize=3)
        
        # Convert to uint8 for display compatibility directly
        sobelx = cv2.convertScaleAbs(sobelx)
        self.current_image=sobelx

        self.update_label(sobelx,Qt.SmoothTransformation)
        



    def sobel_y(self, cv_image):
        # Check if the input image is grayscale; if not, convert it to grayscale.
        if len(cv_image.shape) == 3:
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Apply Sobel operator in the y direction
        sobely = cv2.Sobel(cv_image, cv2.CV_64F, 0, 1, ksize=3)
        
        # Convert to uint8 for display compatibility directly
        sobely = cv2.convertScaleAbs(sobely)
        self.current_image=sobely

        self.update_label(sobely,Qt.SmoothTransformation)




    

    def sobel(self, cv_image):
        # Check if the input image is grayscale; if not, convert it to grayscale.
        if len(cv_image.shape) == 3:
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Apply Sobel operator in both x and y directions
        sobelx = cv2.Sobel(cv_image, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(cv_image, cv2.CV_64F, 0, 1, ksize=3)

        # Compute the magnitude of gradients
        edges = cv2.magnitude(sobelx, sobely)
        edges = cv2.convertScaleAbs(edges)  # Convert to uint8 for display compatibility
        self.current_image=edges

        self.update_label(edges,Qt.SmoothTransformation)



    def scharr(self, cv_image):
        # Check if the input image is grayscale; if not, convert it to grayscale.
        if len(cv_image.shape) == 3:
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Apply Scharr operator in both x and y directions
        scharrx = cv2.Scharr(cv_image, cv2.CV_64F, 1, 0)
        scharry = cv2.Scharr(cv_image, cv2.CV_64F, 0, 1)

        # Compute the magnitude of gradients
        edges = cv2.magnitude(scharrx, scharry)
        edges = cv2.convertScaleAbs(edges)  # Convert to uint8 for display compatibility
        self.current_image=edges

        self.update_label(edges,Qt.FastTransformation)

    def laplacian(self, cv_image):
        # Check if the input image is grayscale; if not, convert it to grayscale.
        if len(cv_image.shape) == 3:
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Apply Laplacian operator
        edges = cv2.Laplacian(cv_image, cv2.CV_64F)
        edges = cv2.convertScaleAbs(edges)  # Convert to uint8 for display compatibility
        self.current_image=edges

        self.update_label(edges,Qt.FastTransformation)


    def prewitt(self, cv_image):
        # Check if the input image is grayscale; if not, convert it to grayscale.
        if len(cv_image.shape) == 3:
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Define Prewitt kernels
        kernelx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
        kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)

        # Apply Prewitt filters
        prewittx = cv2.filter2D(cv_image, cv2.CV_64F, kernelx)
        prewitty = cv2.filter2D(cv_image, cv2.CV_64F, kernely)

        # Compute the magnitude of gradients
        edges = cv2.magnitude(prewittx, prewitty)
        edges = cv2.convertScaleAbs(edges)  # Convert to uint8 for display compatibility

        self.update_label(edges,Qt.FastTransformation)

    
    def roberts(self, cv_image):
        # Check if the input image is grayscale; if not, convert it to grayscale.
        if len(cv_image.shape) == 3:
            cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Define Roberts kernels
        kernelx = np.array([[1, 0], [0, -1]], dtype=np.float32)
        kernely = np.array([[0, 1], [-1, 0]], dtype=np.float32)

        # Apply Roberts filters
        robertsx = cv2.filter2D(cv_image, cv2.CV_64F, kernelx)
        robertsy = cv2.filter2D(cv_image, cv2.CV_64F, kernely)

        # Compute the magnitude of gradients
        edges = cv2.magnitude(robertsx, robertsy)
        edges = cv2.convertScaleAbs(edges)  # Convert to uint8 for display compatibility

        self.update_label(edges,Qt.FastTransformation)




    def update_display(self, cv_image):
        self.current_edge_algorithm(cv_image)

    def cancel_feed(self):
        self.imagefeed.stop()

    def resizeEvent(self, event):
        self.feedlabel.update()
        super().resizeEvent(event)

    def ShowVideo(self):
        if self.DaddyWidget.camera_radiobutton.isChecked():


            self.imagefeed = VideoFeed()
            self.imagefeed.ImageUpdate.connect(self.update_display)
            self.imagefeed.start()
    
    def ShowFileImage(self):
        if self.DaddyWidget.systemfile_radiobutton.isChecked():
            if self.imagefeed.ThreadActive:
                self.cancel_feed()
            self.file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "All Files (*)")
            if self.file_path == '':
                return 
            self.file_image = cv2.imread(self.file_path)
            self.update_display(self.file_image)

    




        


    




