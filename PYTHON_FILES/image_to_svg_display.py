import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QSlider, QFileDialog)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        super().__init__()
        self.fig, self.ax = plt.subplots()
        self.setParent(parent)

    def plot_image(self, image, title):
        self.ax.clear()  # Clear the current axes
        self.ax.imshow(image, cmap='gray')
        self.ax.set_title(title)
        self.ax.axis('off')  # Hide axes
        self.draw()  # Update the canvas

class UI_image_to_svg_display(QWidget):
    def __init__(self, image_to_svg_widget):
        super().__init__()
        self.DaddyWidget = image_to_svg_widget
        self.VBL = QVBoxLayout()  # Instantiate the QVBoxLayout

        self.canvas = MplCanvas(self)
        self.VBL.addWidget(self.canvas) 
        self.DaddyWidget.select_file_b.clicked.connect(self.open_file)  # Connect the button click to open file
        self.DaddyWidget.threshold_slider.setValue(127)
        self.DaddyWidget.threshold_slider.valueChanged.connect(self.update_image)  # Corrected signal name

        self.setLayout(self.VBL)
        self.image = None  # Initialize the image attribute
        self.thresholded_image = None  # Initialize the thresholded image attribute

    def update_image(self, val):
        if self.image is not None:  # Ensure the image has been loaded
            blurred = cv2.GaussianBlur(self.image, (5, 5), 0)
            _, self.thresholded_image = cv2.threshold(blurred, val, 255, cv2.THRESH_BINARY)
            self.canvas.plot_image(self.thresholded_image, "Thresholded Image")
            self.canvas.draw()

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Image Files (*.png *.xpm *.jpg *.bmp);;All Files (*)")
        if path:
            self.image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)  # Load as grayscale
            self.update_image(self.DaddyWidget.threshold_slider.value())  # Update image with the default threshold value

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Assuming image_to_svg_widget is defined and initialized here
    # This is a placeholder, replace it with your actual widget instance
    image_to_svg_widget = QWidget()  # Placeholder; replace with your actual widget
    image_to_svg_widget.select_file_b = QPushButton("Select File")  # Placeholder button
    image_to_svg_widget.threshold_slider = QSlider(Qt.Horizontal)  # Placeholder slider
    image_to_svg_widget.threshold_slider.setRange(0, 255)

    # Create an instance of the UI_image_to_svg_display
    widget = UI_image_to_svg_display(image_to_svg_widget)
    widget.show()
    
    sys.exit(app.exec_())
