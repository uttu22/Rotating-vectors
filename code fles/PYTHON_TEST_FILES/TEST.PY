# from svg.path import parse_path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider 

from svgpathtools import svg2paths,parse_path
from svgpathtools import Line ,Path



paths_list,attributes = svg2paths(r"C:\personal folder\workspace\projects\python project\svg_images\singlepath.svg")

path=paths_list[0]
steps=1000

corrected_path=Path(*[segment for segment in path if not isinstance(segment,Line) ])
for segment in corrected_path :
    print(segment)


t=np.linspace(0,1,10001)
path_coordinates = np.array([corrected_path.point(i) for i in t] )
print(path_coordinates)
# # segment_coordinates = np.array([[[segment.point(i) for i in t] for segment in path ] for path in paths ])
fig,ax = plt.subplots()



line,=ax.plot([point.real for point in path_coordinates],[point.imag for point in path_coordinates])

# # for a in segment_coordinates:
# #     for points in a :
# #         ax.plot([point.real for point in points],[point.imag for point in points])

t_slider=plt.axes([0.1,0.1,1,0.05])
S_t=Slider(t_slider,"t",0,1,valinit=0)

def update(val):
    line.set_data([point.real for point in path_coordinates[0:int(S_t.val*10000)]],[point.imag for point in path_coordinates[0:int(S_t.val*10000)]])
    fig.canvas.draw_idle()

S_t.on_changed(update)
ax.set_aspect("equal")
ax.grid()
plt.show()

#N = number of epicycles 

