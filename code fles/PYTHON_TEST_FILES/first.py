import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np 
import math

def plot_vector(ax,vec,start,step=1,**kwargs):
    return ax.plot(np.linspace(start[0],start[0]+vec[0],step),np.linspace(start[1],start[1]+vec[1],step),**kwargs)
def rot_vec(w,r,t):
    return np.array((r*np.cos(w*t),r*np.sin(w*t)))
fig,ax=plt.subplots()
plt.subplots_adjust(bottom=0.25)

ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_title('Rotating Vectors with Sliders')
ax.axhline(0, color='black', lw=0.5, ls='--')  # Optional: Add x-axis
ax.axvline(0, color='black', lw=0.5, ls='--') 

r1=1
r1_slider=plt.axes([0.1,0.05,0.1,0.05])
S_r1=Slider(r1_slider,"R1",0,3,valinit=0)

r2=1
r2_slider=plt.axes([0.1,0,0.1,0.05])
S_r2=Slider(r2_slider,"R2",0,3,valinit=0)

w1=1
w1_slider=plt.axes([0.3,0.05,0.1,0.05])
S_w1=Slider(w1_slider,"W1",0,1,valinit=0)

w2=1
w2_slider=plt.axes([0.3,0,0.1,0.05])
S_w2=Slider(w2_slider,"W2",0,1,valinit=0)

t=0
t_slider=plt.axes([0.1,0.1,0.5,0.05])
S_t=Slider(t_slider,"t",0,20,valinit=0)


line1,=plot_vector(ax,rot_vec(w1,r1,t),(0,0),step=100)
line2,=plot_vector(ax,rot_vec(w2,r2,t),rot_vec(w1,r1,t),step=100)

def update(val):
    vec1=rot_vec(S_w1.val,S_r1.val,S_t.val)
    vec2=rot_vec(S_w2.val,S_r2.val,S_t.val)
    line1.set_data(np.linspace(0, vec1[0], 100), np.linspace(0, vec1[1], 100))
    line2.set_data(np.linspace(vec1[0], vec1[0] + vec2[0], 100),np.linspace(vec1[1], vec1[1] + vec2[1], 100))
    fig.canvas.draw_idle()

S_r1.on_changed(update)
S_r2.on_changed(update)
S_w1.on_changed(update)
S_w1.on_changed(update)
S_t.on_changed(update)


plt.show()