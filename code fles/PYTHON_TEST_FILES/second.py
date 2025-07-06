import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider 
import cv2 

# n=7
# R = np.random.uniform(size=n)*5
# W = np.random.uniform(size=n)*5
# # R=np.array([1,2,3,4])
# # W=np.array([0.2,0.4,0.6,0.8])


import cv2
image = cv2.imread(r'C:\personal folder\workspace\projects\python project\sample_images\IMG20240930004701.jpg', 0)




cv2.namedWindow("Original image")
cv2.imshow("Original image",cv2.resize(image,(600,800)))

def on_trackbar(val):
    pass
# cv2.namedWindow("Canny")
# cv2.createTrackbar('low_threshold', 'Canny', 0, 255, on_trackbar)
# cv2.createTrackbar('high_threshold', 'Canny', 0, 255, on_trackbar)

# cv2.createTrackbar('sigma', 'Canny', 0, 1000, on_trackbar)
cv2.namedWindow("thresholded image")
cv2.createTrackbar('Threshold', 'thresholded image', 0, 255, on_trackbar)
while True:
    # sigma=cv2.getTrackbarPos('sigma', 'Canny')
    # low_threshold=cv2.getTrackbarPos('low_threshold', 'Canny')
    # high_threshold=cv2.getTrackbarPos('high_threshold', 'Canny')
    threshold_value=cv2.getTrackbarPos("Threshold","thresholded image")

    # blurred_image = cv2.GaussianBlur(image, (9,9), sigma/100)

    # edges = cv2.Canny(blurred_image, low_threshold, high_threshold)
    _, thresholded_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    # cv2.imshow('Canny', edges)
    cv2.imshow('thresholded image', thresholded_image)

    # Find contours from the thresholded image
    # contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # image_with_contours = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)
    # cv2.imshow('Contours', cv2.resize(image_with_contours, (800, 600)))
    if cv2.waitKey(1) & 0xFF == 27:
        cv2.imwrite("edges.png",thresholded_image)
        cv2.destroyAllWindows()
        break
# # Display the results

# blurred_image = cv2.GaussianBlur(image, (9,9),0)
 
# edges = cv2.Canny(blurred_image,0, 50)
# _, thresholded_image = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY)
# cv2.imshow('Canny', edges)
# cv2.imshow('thresholded image', cv2.resize(thresholded_image, (800, 600)))

#     # Find contours from the thresholded image
# contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# image_with_contours = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
# cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)
# cv2.imshow('Contours', cv2.resize(image_with_contours, (800, 600)))
# cv2.waitKey(0)
# cv2.destroyAllWindows()





print(len(contours))
class My_plot :
    def __init__(self,R,W,t=1,start=(0,0),steps=100):       
        self.R=R
        self.W=W
        self.t=t
        self.steps=steps
        self.p_data=np.zeros((len(R)+1,2))
        self.l_data=np.zeros((len(R),2,steps))
        self.c_data=np.zeros((len(R),2,steps))
        self.p_data[0]=np.array(start)
        self.point_data(t)
        self.line_data(t)
        self.circle_data(t)
    def point_data(self,t):
        self.t=t
        for i in np.arange(1,len(self.R)+1):
            self.p_data[i][0]=self.p_data[i-1][0]+self.R[i-1]*np.cos(self.W[i-1]*t)
            self.p_data[i][1]=self.p_data[i-1][1]+self.R[i-1]*np.sin(self.W[i-1]*t)
        return self.p_data
    def line_data(self,t):
        self.t=t
        for i in np.arange(0,len(self.R),1):
            self.l_data[i][0]=np.linspace(self.p_data[i][0],self.p_data[i+1][0],self.steps)
            self.l_data[i][1]=np.linspace(self.p_data[i][1],self.p_data[i+1][1],self.steps)
        return self.l_data
    def circle_data(self,t):
        self.t=t
        angles=np.linspace(0,2*np.pi,self.steps)
        for i in np.arange(0,len(R),1):
            self.c_data[i][0]=self.p_data[i][0]+np.cos(angles)*R[i]
            self.c_data[i][1]=self.p_data[i][1]+np.sin(angles)*R[i]
        return self.c_data 


# t=1
# T_max=20
# steps_persec=200
fig,ax=plt.subplots()
# plt.subplots_adjust(bottom=0.25)
# graph= My_plot(R,W,t,(1,1),steps=50)
# points,=ax.plot(graph.point_data(t)[:,0],graph.point_data(t)[:,1],"o",markersize=3)
# circles=[ax.plot(*graph.circle_data(t)[i])[0] for i in range(len(R))]
# line,=ax.plot(np.ravel(graph.line_data(t)[:,0,:]),np.ravel(graph.line_data(t)[:,1,:]),linewidth=0.5)
# end_point_trace = np.zeros((steps_persec*T_max+1,2))
# for i in np.arange(0,steps_persec*T_max+1):
#     end_point_trace[i]=graph.point_data((i)/steps_persec)[n]
# end_point_curve_plot, = ax.plot(end_point_trace[0:int((steps_persec*t)),0],end_point_trace[0:int((steps_persec*t)),1])
# for contour in contours:
#     # Extract x and y coordinates
#     x = contour[:, 0, 0]  # x-coordinates
#     y = contour[:, 0, 1]  # y-coordinates
#     ax.plot(x, y,linewidth=1) 


# t_slider=plt.axes([0.1,0.1,0.5,0.05])
# S_t=Slider(t_slider,"t",0,T_max,valinit=1)

# def update(val):
#     points.set_data(graph.point_data(S_t.val)[:,0],graph.point_data(S_t.val)[:,1])
#     line.set_data(np.ravel(graph.line_data(S_t.val)[:,0,:]),np.ravel(graph.line_data(S_t.val)[:,1,:]))
#     for i in range(len(circles)):
#         circles[i].set_data(*graph.circle_data(t)[i])
#     fig.canvas.draw_idle()
#     end_point_curve_plot.set_data(end_point_trace[0:int((steps_persec*(S_t.val))),0],end_point_trace[0:int((steps_persec*(S_t.val))),1])

# S_t.on_changed(update)
# sum_r = np.sum(R)

# ax.set_xlim((sum_r*(-2),sum_r*2))
# ax.set_ylim(-sum_r,sum_r)
# ax.set_aspect("equal")
# ax.grid()
# plt.show()



