

from PyQt5 import QtCore, QtGui, QtWidgets 
from edge_detection_widget import Ui_edge_detection_widget
from edge_tracing_widget import Ui_edge_tracing_widget
from image_to_svg_widget import Ui_image_to_svg_widget
from ascii_art_widget import Ui_ascii_art_widget

from edge_tracing_display import UI_edge_tracing_display
from edge_detection_display import UI_edge_detection_display
from image_to_svg_display import UI_image_to_svg_display

from mpl_canvas import MplCanvas

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1265, 850)
        MainWindow.setAutoFillBackground(False) 

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setHorizontalSpacing(7)
        self.gridLayout.setObjectName("gridLayout")
        self.OPTIONS_FRAME = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OPTIONS_FRAME.sizePolicy().hasHeightForWidth())
        self.OPTIONS_FRAME.setSizePolicy(sizePolicy)
        self.OPTIONS_FRAME.setMaximumSize(QtCore.QSize(500, 16777215))

        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiCondensed")
        font.setPointSize(13)

        ###############################################################
        #OPTIONS FRAME

        self.OPTIONS_FRAME.setFont(font)
        self.OPTIONS_FRAME.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.OPTIONS_FRAME.setFrameShadow(QtWidgets.QFrame.Raised) 
        self.OPTIONS_FRAME.setObjectName("OPTIONS_FRAME")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.OPTIONS_FRAME)
        self.verticalLayout.setObjectName("verticalLayout")

        self.stackedWidget = QtWidgets.QStackedWidget(self.OPTIONS_FRAME)
        self.stackedWidget.setObjectName("stackedWidget")

        self.EDGE_DETECTION_WIDGET = Ui_edge_detection_widget()
        self.edge_detection_container = QtWidgets.QWidget()
        self.EDGE_DETECTION_WIDGET.setupUi(self.edge_detection_container)
        # self.EDGE_DETECTION_WIDGET.setObjectName("EDGE_DETECTION_WIDGET")
        self.stackedWidget.addWidget(self.edge_detection_container)




        self.EDGE_TRACING_WIDGET = Ui_edge_tracing_widget()
        self.edge_tracing_container = QtWidgets.QWidget()
        self.EDGE_TRACING_WIDGET.setupUi(self.edge_tracing_container)
        # self.EDGE_TRACING_WIDGET.setObjectName("EDGE_TRACING_WIDGET")
        self.stackedWidget.addWidget(self.edge_tracing_container)


        self.IMAGE_TO_SVG_WIDGET = Ui_image_to_svg_widget()
        self.image_to_svg_container=QtWidgets.QWidget()
        self.IMAGE_TO_SVG_WIDGET.setupUi(self.image_to_svg_container)
        # self.IMAGE_TO_SVG_WIDGET.setObjectName("IMAGE_TO_SVG_WIDGET")
        self.stackedWidget.addWidget(self.image_to_svg_container)

        self.ASCII_ART_WIDGET = Ui_ascii_art_widget()
        self.ascii_art_container=QtWidgets.QWidget()
        self.ASCII_ART_WIDGET.setupUi(self.ascii_art_container)
        # self.ASCII_ART_WIDGET.setObjectName("ASCII_ART_WIDGET")
        self.stackedWidget.addWidget(self.ascii_art_container)

        self.verticalLayout.addWidget(self.stackedWidget)
        self.gridLayout.addWidget(self.OPTIONS_FRAME, 1, 1, 1, 1)


        ##########################################################################
        #APP NAME FRAME


        self.APP_NAME_FRAME = QtWidgets.QFrame(self.centralwidget)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.APP_NAME_FRAME.sizePolicy().hasHeightForWidth())

        self.APP_NAME_FRAME.setSizePolicy(sizePolicy)
        self.APP_NAME_FRAME.setMinimumSize(QtCore.QSize(500, 100))
        self.APP_NAME_FRAME.setMaximumSize(QtCore.QSize(500, 100))

        font = QtGui.QFont()
        font.setPointSize(10)
        self.APP_NAME_FRAME.setFont(font)
        self.APP_NAME_FRAME.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.APP_NAME_FRAME.setFrameShadow(QtWidgets.QFrame.Raised)
        self.APP_NAME_FRAME.setObjectName("APP_NAME_FRAME")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.APP_NAME_FRAME)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.APP_TITLE = QtWidgets.QLabel(self.APP_NAME_FRAME)
        font = QtGui.QFont()
        font.setFamily("Freestyle Script")
        font.setPointSize(28)
        self.APP_TITLE.setFont(font)
        self.APP_TITLE.setAlignment(QtCore.Qt.AlignCenter)
        self.APP_TITLE.setObjectName("APP_TITLE")
        self.verticalLayout_2.addWidget(self.APP_TITLE)
        self.APP_CREDITS = QtWidgets.QLabel(self.APP_NAME_FRAME)
        self.APP_CREDITS.setObjectName("APP_CREDITS")
        self.verticalLayout_2.addWidget(self.APP_CREDITS)
        self.gridLayout.addWidget(self.APP_NAME_FRAME, 0, 1, 1, 1)
        self.DISPLAY_FRAME = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DISPLAY_FRAME.sizePolicy().hasHeightForWidth())


        ###################################################################################################
        #DISPLAY_FRAME

        self.DISPLAY_FRAME.setSizePolicy(sizePolicy)
        self.DISPLAY_FRAME.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.DISPLAY_FRAME.setFrameShadow(QtWidgets.QFrame.Raised)
        self.DISPLAY_FRAME.setObjectName("DISPLAY_FRAME")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.DISPLAY_FRAME)
        self.horizontalLayout.setObjectName("horizontalLayout")


        self.stackedWidget_2 = QtWidgets.QStackedWidget(self.DISPLAY_FRAME)
        self.stackedWidget_2.setObjectName("stackedWidget_2")

        self.EDGE_DETECTION_DISPLAY = UI_edge_detection_display(self.EDGE_DETECTION_WIDGET)
        self.EDGE_DETECTION_DISPLAY_CONTAINER = QtWidgets.QWidget()
        self.layout_for_edge_detection = QtWidgets.QVBoxLayout(self.EDGE_DETECTION_DISPLAY_CONTAINER)
        self.layout_for_edge_detection.addWidget(self.EDGE_DETECTION_DISPLAY)
        self.stackedWidget_2.addWidget(self.EDGE_DETECTION_DISPLAY_CONTAINER)

        self.EDGE_TRACING_DISPLAY = UI_edge_tracing_display(self.EDGE_TRACING_WIDGET)
        self.EDGE_TRACING_DISPLAY_CONTAINER=QtWidgets.QWidget()
        self.layout_for_edge_tracing = QtWidgets.QVBoxLayout(self.EDGE_TRACING_DISPLAY_CONTAINER)
        self.layout_for_edge_tracing.addWidget(self.EDGE_TRACING_DISPLAY)
        self.stackedWidget_2.addWidget(self.EDGE_TRACING_DISPLAY_CONTAINER)

        # self.IMAGE_TO_SVG_DISPLAY = UI_image_to_svg_display(self.IMAGE_TO_SVG_WIDGET)
        # self.IMAGE_TO_SVG_DISPLAY_CONTAINER=QtWidgets.QWidget()
        # self.layout_for_image_to_svg = QtWidgets.QVBoxLayout(self.IMAGE_TO_SVG_DISPLAY_CONTAINER)
        # self.layout_for_image_to_svg.addWidget(self.IMAGE_TO_SVG_DISPLAY)
        # self.stackedWidget_2.addWidget(self.IMAGE_TO_SVG_DISPLAY_CONTAINER)



        # self.ASCII_ART_DISPLAY_CONTAINER = QtWidgets.QWidget()
        # self.stackedWidget_2.addWidget(self.ASCII_ART_DISPLAY_CONTAINER)

        self.horizontalLayout.addWidget(self.stackedWidget_2)
        self.gridLayout.addWidget(self.DISPLAY_FRAME, 1, 0, 1, 1)

        ####################################################################################
        #MENU FRAME



        self.MENU_FRAME = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MENU_FRAME.sizePolicy().hasHeightForWidth())
        self.MENU_FRAME.setSizePolicy(sizePolicy)
        self.MENU_FRAME.setMinimumSize(QtCore.QSize(600, 100))
        self.MENU_FRAME.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.MENU_FRAME.setFrameShadow(QtWidgets.QFrame.Raised)
        self.MENU_FRAME.setObjectName("MENU_FRAME")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.MENU_FRAME)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")




        self.menu_button_1 = QtWidgets.QPushButton(self.MENU_FRAME)
        self.menu_button_1.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold Condensed")
        font.setPointSize(12)
        self.menu_button_1.setFont(font)
        self.menu_button_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.menu_button_1.setObjectName("menu_button_1")
        self.horizontalLayout_2.addWidget(self.menu_button_1)
        self.menu_button_1.clicked.connect(self.menu_button_1_clicked)


        self.menu_button_2 = QtWidgets.QPushButton(self.MENU_FRAME)
        self.menu_button_2.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold Condensed")
        font.setPointSize(12)
        self.menu_button_2.setFont(font)
        self.menu_button_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.menu_button_2.setObjectName("menu_button_2")
        self.horizontalLayout_2.addWidget(self.menu_button_2)
        self.menu_button_2.clicked.connect(self.menu_button_2_clicked)



        self.menu_button_3 = QtWidgets.QPushButton(self.MENU_FRAME)
        self.menu_button_3.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold Condensed")
        font.setPointSize(12)
        self.menu_button_3.setFont(font)
        self.menu_button_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.menu_button_3.setObjectName("menu_button_3")
        self.horizontalLayout_2.addWidget(self.menu_button_3)
        self.menu_button_3.clicked.connect(self.menu_button_3_clicked)


        self.menu_button_4 = QtWidgets.QPushButton(self.MENU_FRAME)
        self.menu_button_4.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiBold Condensed")
        font.setPointSize(12)
        self.menu_button_4.setFont(font)
        self.menu_button_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.menu_button_4.setObjectName("menu_button_4")
        self.horizontalLayout_2.addWidget(self.menu_button_4)
        self.menu_button_4.clicked.connect(self.menu_button_4_clicked)


        self.gridLayout.addWidget(self.MENU_FRAME, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        
        
        MainWindow.setCentralWidget(self.centralwidget)



        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.APP_TITLE.setText(_translate("MainWindow", "MY PYTHON PROJECT"))
        self.APP_CREDITS.setText(_translate("MainWindow", "By UTKARSH PRABHAT , 23EEB0B56"))
        self.menu_button_1.setText(_translate("MainWindow", "EGDE \n""DETCTION"))
        self.menu_button_2.setText(_translate("MainWindow", "EDGE\n""TRACING"))
        self.menu_button_3.setText(_translate("MainWindow", "IMAGE TO\n""SVG"))
        self.menu_button_4.setText(_translate("MainWindow", "ASCII \n""ART"))
    
    def menu_button_1_clicked(self):
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)
    
    def menu_button_2_clicked(self):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_2.setCurrentIndex(1)
    
    def menu_button_3_clicked(self):
        self.stackedWidget.setCurrentIndex(2)
        self.stackedWidget_2.setCurrentIndex(2)
    
    def menu_button_4_clicked(self):
        self.stackedWidget.setCurrentIndex(3)
        self.stackedWidget_2.setCurrentIndex(3)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
