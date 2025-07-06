from svg.path import parse_path
import numpy as np
import matplotlib.pyplot as plt

from svgpathtools import svg2paths


paths_list,attributes = svg2paths(r"C:\personal folder\workspace\projects\python project\edges.svg")
steps=1000

for segment in paths_list:
    print(segment)


# paths_coordinates = np.array([[path.point(i) for i in t] for path in paths])
segment_coordinates = np.array([[[segment.point(i) for i in t] for segment in path ] for path in paths_list ])
fig,ax = plt.subplots()

for path_coordinate in paths_coordinates:
    ax.plot([point.real for point in path_coordinate],[point.imag for point in path_coordinate])

for a in segment_coordinates:
    for points in a :
        ax.plot([point.real for point in points],[point.imag for point in points])


ax.set_aspect("equal")
ax.grid()
plt.show()