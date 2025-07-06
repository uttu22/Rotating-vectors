import matplotlib.pyplot as plt 
from svgpathtools import Line ,Path,svg2paths
from svgpathtools import parse_path
import numpy as np
from matplotlib.widgets import Slider 
from numba import njit
#lets say i have a path p 
# path p has segments s 

path1,attributes = svg2paths(r"C:\personal folder\workspace\projects\python project\untitled.svg")

path=path1[1]

fig,ax=plt.subplots()
plt.subplots_adjust(bottom=0.2)

steps=100000


t_step = 1/steps
n=50

N_l=[0]
for i in range(1,n+1) :
    N_l=N_l+[i]+[-i]
N=np.array(N_l)
print(N)

t_arr=np.linspace(0,1,steps+1)
print("t_arr obtained")


path_coordinates = np.array([path.point(i) for i in t_arr])
print("path_cordinates obtained")

ax.plot([point.real for point in path_coordinates],[point.imag for point in path_coordinates])
fig.patch.set_facecolor("black")
ax.set_facecolor("black")
print(path_coordinates)


def F(t):
    return path_coordinates[int(t*steps)]

point,=ax.plot([F(1).real],[F(1).imag],marker="o")

@njit
def get_df(t,f):
    return path_coordinates[int(t*steps)]*t_step*np.exp(2j*(np.pi)*f*t)

vectorized_df = np.vectorize(get_df)
print(vectorized_df(t_arr,2))


C= np.array([np.sum(vectorized_df(t_arr,f))  for f in N])
print("C array formed")
print(C)

class time_var:
    def __init__(self,C,N,t=1,start=(0,0),steps=100):
        self.t=t
        self.C=C
        self.N=N
        self.steps=steps
        self.n=len(N) #n number of freq = number of vector = number of points other than start 
        self.start=complex(start[0],start[1])
        self.p_data= np.zeros((2,self.n))
        # self.l_data= np.zeros((n,2,self.steps+1))
        self.p_data[0,0]=C[0].real
        self.p_data[1,0]=C[0].imag
        self.vectorized_exp=np.vectorize(self.get_exp)
        self.c_data=np.zeros((self.n-1,2,self.steps))
        self.v_data=np.zeros(self.n)

    
    def get_exp(self,t,f):
        return np.exp(-2j*np.pi*f*t)


    

    def E(self,t):
        return self.vectorized_exp(t,self.N)

    def V(self,t):
        self.v_data=(self.C)*(self.E(t))
        self.t=t
        return self.v_data
 
    def point_data(self):
        for i in np.arange(1,(self.n)):
            self.p_data[0,i]=self.v_data[i].real + self.p_data[0,i-1] 
            self.p_data[1,i]=self.v_data[i].imag + self.p_data[1,i-1] 
        return self.p_data
    
    
    def circle_data(self):
        angles=np.linspace(0,2*np.pi,self.steps)
        for i in range(0,self.n-1):
            self.c_data[i,0]=self.p_data[0,i] + abs(self.v_data[i+1])*np.cos(angles)
            self.c_data[i,1]=self.p_data[1,i] + abs(self.v_data[i+1])*np.sin(angles)
        return self.c_data








MyGraph = time_var(C,N)



t_slider=plt.axes([0.1,0.1,0.8,0.05])
S_t=Slider(t_slider,"t",0,1,valinit=1)

curve_data = np.array(([np.sum(MyGraph.V(t)).real for t in t_arr],[np.sum(MyGraph.V(t)).imag for t in t_arr]))
MyGraph.V(1)
curve,=ax.plot(curve_data[0,0:len(t_arr)-1],curve_data[1,0:len(t_arr)-1])
points,=ax.plot(*MyGraph.point_data(),marker="o",markersize=0.5)



circle_plot=np.zeros(n,dtype=Line)
for i in np.arange(n):
    circle_plot[i],=ax.plot(*MyGraph.circle_data()[i],linewidth=0.2)


def update(val):
    MyGraph.V(S_t.val)
    curve.set_data(curve_data[0,0:int(S_t.val*steps)],curve_data[1,0:int(S_t.val*steps)])
    points.set_data(*MyGraph.point_data())
    for i in np.arange(n):
        circle_plot[i].set_data(*MyGraph.circle_data()[i])


S_t.on_changed(update)

ax.set_aspect("equal")
ax.grid()
plt.show()





