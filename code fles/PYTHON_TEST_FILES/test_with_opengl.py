import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QWidget
from PyQt5.QtOpenGL import QGLWidget
from OpenGL.GL import *

class CircleWidget(QGLWidget):
    def __init__(self):
        super().__init__()
        self.radius = 0.5  # Default radius

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Set background color to black

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        
        # Draw the circle
        self.draw_circle(self.radius)

        self.swapBuffers()

    def draw_circle(self, radius):
        num_segments = 100  # Number of segments to approximate the circle
        glBegin(GL_LINE_LOOP)  # Draw a line loop for the circle
        for i in range(num_segments):
            angle = 2 * np.pi * i / num_segments
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            glVertex2f(x, y)
        glEnd()

    def set_radius(self, radius):
        self.radius = radius
        self.update()  # Trigger a repaint

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenGL Circle with Adjustable Radius")
        self.setGeometry(100, 100, 800, 600)

        self.circle_widget = CircleWidget()

        # Create a slider to adjust the radius
        self.slider = QSlider()
        self.slider.setOrientation(1)  # Horizontal slider
        self.slider.setRange(1, 100)  # Range from 1 to 100
        self.slider.setValue(50)  # Set initial value
        self.slider.valueChanged.connect(self.update_radius)

        layout = QVBoxLayout()
        layout.addWidget(self.circle_widget)
        layout.addWidget(self.slider)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_radius(self, value):
        radius = value / 100.0  # Scale to 0.01 to 1.0
        self.circle_widget.set_radius(radius)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
