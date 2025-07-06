from svg.path import parse_path
import matplotlib.pyplot as plt
import numpy as np
from svgpathtools import svg2paths


paths,attributes = svg2paths(r"C:\personal folder\workspace\projects\python project\edges.svg")

for path in paths:
    print(path)
    print()

    for segment in path :
        print(len(segment))
        print()
# # Iterate through segments
# for segment in path:
#     print(segment)

# steps =100
# fig,ax = plt.subplots()
# t=np.linspace(0,1,steps+1)
print(len(paths))
# for segment in path:
#     points=segment.point(t)
#     if type(points) == complex :
#         continue
#     ax.plot([p.real for p in points],[p.imag for p in points],color="black")




# ax.set_aspect("equal")
# plt.show()