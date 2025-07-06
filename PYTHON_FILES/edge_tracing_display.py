from PyQt5.QtWidgets import QWidget,QSlider,QFileDialog
from file_select_dialog import get_file_path
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from svgpathtools import Line ,Path,svg2paths
from svgpathtools import parse_path
import numpy as np 
from numba import njit


class UI_edge_tracing_display(FigureCanvasQTAgg):
    def  __init__(self,edge_tracing_widget,parent=None):

        # self.fig = Figure(figsize=(5, 10), dpi=100)
        # super(UI_edge_tracing_display, self).__init__(self.fig,parent)
        # self.axes = self.fig.add_subplot(111)

        # Correct order: Initialize superclass first
        self.fig = Figure(figsize=(5, 9), dpi=100)  # Create figure
        super(UI_edge_tracing_display,self).__init__(self.fig)  # Call super first
        self.setParent(parent)  # Set parent explicitly if needed
        self.axes = self.fig.add_subplot(111)  # Now you can safely add axes
        self.axes.invert_yaxis()
        self.axes.set_aspect("equal",adjustable='box')


        self.EDGE_TRACING_WIDGET=edge_tracing_widget


        self.EDGE_TRACING_WIDGET.select_file_b.clicked.connect( self.set_file_path)
        self.EDGE_TRACING_WIDGET.show_original_path_cb.clicked.connect( self.set_visibility)
        self.EDGE_TRACING_WIDGET.show_traced_path_cb.clicked.connect( self.set_visibility)
        self.EDGE_TRACING_WIDGET.show_vectors_cb.clicked.connect( self.set_visibility)
        self.EDGE_TRACING_WIDGET.show_circles_cb.clicked.connect( self.set_visibility)


        ##########################
        #Initial setup of data 
        self.steps=1000
        self.n_vectors=51

        self.EDGE_TRACING_WIDGET.vector_count_sb.setRange(21,201)
        self.EDGE_TRACING_WIDGET.vector_count_sb.setSingleStep(2)
        self.EDGE_TRACING_WIDGET.vector_count_sb.setValue(self.n_vectors)



        self.EDGE_TRACING_WIDGET.steps_sb.setRange(500,100000)
        self.EDGE_TRACING_WIDGET.steps_sb.setSingleStep(1)
        self.EDGE_TRACING_WIDGET.steps_sb.setValue(self.steps)


        self.EDGE_TRACING_WIDGET.vector_count_sb.valueChanged.connect(self.set_freq_arr)
        self.EDGE_TRACING_WIDGET.steps_sb.valueChanged.connect(self.set_steps)
        self.EDGE_TRACING_WIDGET.calculate_b.clicked.connect(self.calculate)

        
        self.EDGE_TRACING_WIDGET.t_parameter_slider.valueChanged.connect( self.update_plot)

        self.original_path,=self.axes.plot([0],[0])
        self.curve_plot,= self.axes.plot([0],[0])
        self.points_plot,=self.axes.plot([0],[0])


    
    def reset_all_plots(self):
        self.axes.cla()
        
        self.draw()

    def set_visibility(self):
        self.original_path.set_visibility(self.EDGE_TRACING_WIDGET.show_original_path_cb.isChecked())
        self.curve_plot.set_visibility(self.EDGE_TRACING_WIDGET.show_traced_path_cb.isChecked())
        self.points_plot.set_visibility(self.EDGE_TRACING_WIDGET.show_vectors_cb.isChecked())
        
        self.draw()

    def set_file_path(self):
        print("reached function")
        self.file_path, _ = QFileDialog.getOpenFileName(None, "Open SVG File", "", "SVG Files (*.svg);;All Files (*)")
    def set_freq_arr(self,n=51):
        self.n_vectors=n
        

    def set_steps(self,n=1000):
        self.steps=n
        

    def calculate(self):
        from svgpathtools import Line ,Path,svg2paths
        from svgpathtools import parse_path
        
        self.EDGE_TRACING_WIDGET.t_parameter_slider.setRange(0,self.steps)
        self.reset_all_plots()
        N_l=[0]
        for i in range(1,self.n_vectors+1) :
            N_l=N_l+[i]+[-i]
        self.freq_arr=np.array(N_l)
        print(self.freq_arr)
        self.t_arr=np.linspace(0,1,self.steps+1)
        print(self.t_arr)
        self.t_step=1/self.steps


        self.paths,attributes=svg2paths(self.file_path)
        self.combined_path = Path()

        for path in self.paths:
            self.combined_path+=path
        print(self.combined_path)
        ##PATH COORDINATES
        self.path_coordinates = np.array([self.combined_path.point(t) for t in self.t_arr])
        print(self.path_coordinates)
 

        # df = small element across f  
        def get_df(t,f):
            return self.path_coordinates[int(t*self.steps)]*self.t_step*np.exp(2j*(np.pi)*f*t)
        vectorized_df = np.vectorize(get_df)

        print("got_df")
        # integration , COMPLEX AMPLITUDES OF VECTORs OBTAINED
        self.C= np.array([np.sum(vectorized_df(self.t_arr,f))  for f in self.freq_arr])
        self.MyGraph = self.TimeVar(self.C,self.freq_arr)
        print("COMplex array")
        print(self.C)
        self.set_initial_plot()

    def update_plot(self,value=1):

        self.t = (value/self.steps)
        self.MyGraph.V(self.t)
        self.curve_plot.set_data(self.curve_data[0,0:int((self.t*self.steps) + 1)],self.curve_data[1,0:int((self.t*self.steps)+1)])
        self.points_plot.set_data(*self.MyGraph.point_data())
        self.draw()


    def set_initial_plot(self):

        self.curve_data = np.array(([np.sum(self.MyGraph.V(t)).real for t in self.t_arr],[np.sum(self.MyGraph.V(t)).imag for t in self.t_arr]),dtype=np.complex128)
        self.MyGraph.V(1)
        self.original_path,=self.axes.plot([point.real for point in self.path_coordinates],[point.imag for point in self.path_coordinates])
        self.curve_plot,= self.axes.plot(self.curve_data[0,0:len(self.t_arr)-1],self.curve_data[1,0:len(self.t_arr)-1],linewidth=1,color="black")
        self.points_plot,=self.axes.plot(*self.MyGraph.point_data(),linewidth=1,color="darkgreen")
        
        self.draw()

    
    







    ############################################################################################
    class TimeVar:
        def __init__(self, C, N, t=1, start=(0, 0), steps=100):
            self.t = t
            self.C = np.array(C, dtype=np.complex128)
            self.N = np.array(N, dtype=np.float64)
            self.steps = steps
            self.n = len(N)  # number of frequencies
            self.start = complex(start[0], start[1])
            self.p_data = np.zeros((2, self.n), dtype=np.float64)
            self.c_data = np.zeros((self.n - 1, 2, self.steps), dtype=np.float64)
            self.v_data = np.zeros(self.n, dtype=np.complex128)

            # Initialize first point of p_data
            self.p_data[0, 0] = self.C[0].real
            self.p_data[1, 0] = self.C[0].imag

        @staticmethod
        @njit
        def get_exp(t, f):
            return np.exp(-2j * np.pi * f * t)

        @staticmethod
        @njit
        def calculate_v_data(C, E, v_data):
            for i in range(len(C)):
                v_data[i] = C[i] * E[i]
            return v_data

        def E(self, t):
            # Generate the exponential values for each frequency in N
            return np.array([self.get_exp(t, f) for f in self.N])

        def V(self, t):
            # Calculate V using the numba-optimized function
            self.v_data = self.calculate_v_data(self.C, self.E(t), self.v_data)
            self.t = t
            return self.v_data

        @staticmethod
        @njit
        def calculate_point_data(v_data, p_data):
            for i in range(1, len(v_data)):
                p_data[0, i] = v_data[i].real + p_data[0, i - 1]
                p_data[1, i] = v_data[i].imag + p_data[1, i - 1]
            return p_data

        def point_data(self):
            # Use numba to calculate the point data for faster performance
            self.p_data = self.calculate_point_data(self.v_data, self.p_data)
            return self.p_data

        @staticmethod
        @njit
        def calculate_circle_data(v_data, p_data, c_data, steps):
            angles = np.linspace(0, 2 * np.pi, steps)
            for i in range(len(v_data) - 1):
                radius = abs(v_data[i + 1])
                for j in range(steps):
                    c_data[i, 0, j] = p_data[0, i] + radius * np.cos(angles[j])
                    c_data[i, 1, j] = p_data[1, i] + radius * np.sin(angles[j])
            return c_data

        def circle_data(self):
            # Use numba-optimized function for circle data calculation
            self.c_data = self.calculate_circle_data(self.v_data, self.p_data, self.c_data, self.steps)
            return self.c_data
        
    #################################################################################