import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from svgpathtools import Line ,Path,svg2paths
from svgpathtools import parse_path
import numpy as np
from matplotlib.widgets import Slider 
from numba import njit

#lets say i have a path p 
# path p has segments s 

path1,attributes = svg2paths(r"C:\personal folder\workspace\projects\python project\svg_images\untitled.svg")
path=path1[1]

#SETTING UP PLOTS
fig,ax=plt.subplots()
plt.subplots_adjust(bottom=0.2)
# fig.patch.set_facecolor("black")
# ax.set_facecolor("black")


#STEP,FREQ,TIME_ARR
steps=100000 
t_step = 1/steps
n=125
N_l=[0]
for i in range(1,n+1) :
    N_l=N_l+[i]+[-i]
N=np.array(N_l)
print(N)
t_arr=np.linspace(0,1,steps+1)
print("t_arr obtained")



#SETTING UP PATH CORDINATES
path_coordinates = np.array([path.point(i) for i in t_arr])
print("path_cordinates obtained")
print(path_coordinates)

# F(t) main function (path function )
@njit
def F(t):
    return path_coordinates[int(t*steps)]

# df = small element across f
@njit
def get_df(t,f):
    return path_coordinates[int(t*steps)]*t_step*np.exp(2j*(np.pi)*f*t)
vectorized_df = np.vectorize(get_df)

# integration , COMPLEX AMPLITUDES OF VECTORs OBTAINED
C= np.array([np.sum(vectorized_df(t_arr,f))  for f in N])
print("C array formed")
print(C)

ax.plot([point.real for point in path_coordinates],[point.imag for point in path_coordinates])
point,=ax.plot([F(1).real],[F(1).imag],marker="o")



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









MyGraph = TimeVar(C,N)




curve_data = np.array(([np.sum(MyGraph.V(t)).real for t in t_arr],[np.sum(MyGraph.V(t)).imag for t in t_arr]))
MyGraph.V(1)
curve,=ax.plot(curve_data[0,0:len(t_arr)-1],curve_data[1,0:len(t_arr)-1],linewidth=1,color="black")
points,=ax.plot(*MyGraph.point_data(),linewidth=1,color="darkgreen")




# circle_plot=np.zeros(2*n,dtype=Line)
# for i in np.arange(2*n):
#     circle_plot[i],=ax.plot(*MyGraph.circle_data()[i],linewidth=0.2,color="orange")


def zoom(event):
    # Get the current x and y limits
    cur_xlim = ax.get_xlim()
    cur_ylim = ax.get_ylim()
    
    # Set the zoom factor
    zoom_factor = 0.9 if event.button == 'up' else 1.1
    zoom_x=curve_data[0,int(S_t.val*steps)]
    zoom_y=curve_data[1,int(S_t.val*steps)]
    # Calculate the new limits based on the zoom factor using zoom_x and zoom_y
    new_xlim = [zoom_x - (zoom_x - cur_xlim[0]) * zoom_factor,
                zoom_x + (cur_xlim[1] - zoom_x) * zoom_factor]
    new_ylim = [zoom_y - (zoom_y - cur_ylim[0]) * zoom_factor,
                zoom_y + (cur_ylim[1] - zoom_y) * zoom_factor]
    
    ax.set_xlim(new_xlim)
    ax.set_ylim(new_ylim)



t_slider=plt.axes([0.1,0.1,0.8,0.05])
S_t=Slider(t_slider,"t",0,1,valinit=1)
def update(val):
    MyGraph.V(S_t.val)
    curve.set_data(curve_data[0,0:int(S_t.val*steps)],curve_data[1,0:int(S_t.val*steps)])
    points.set_data(*MyGraph.point_data())
    # for i in np.arange(2*n):
    #     circle_plot[i].set_data(*MyGraph.circle_data()[i])
    
    ax.figure.canvas.draw()


S_t.on_changed(update)
# fig.canvas.mpl_connect('scroll_event', zoom)
T_total=40
fps=25
F_total=fps*T_total
t_perframe=1/F_total
interval=1/fps


# def animate(frame):
#     MyGraph.V(frame*t_perframe)
#     curve.set_data(curve_data[0,0:int(frame*t_perframe*steps)],curve_data[1,0:int(frame*t_perframe*steps)])
#     points.set_data(*MyGraph.point_data())
#     for i in np.arange(2*n):
#         circle_plot[i].set_data(*MyGraph.circle_data()[i])

# ani = animation.FuncAnimation(fig, animate, frames=F_total, interval=interval)

ax.set_aspect("equal")
ax.grid()
ax.invert_yaxis()
plt.show()





