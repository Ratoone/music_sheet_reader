import os

import cv2
import matplotlib.pyplot as plt
import numpy as np


staff_info = {"twinkle":{"name":"no_key_twinkle_42_11.jpg", "x_coord_upper_line": 42, "line_gap":11, "nb_bar_lines" : 3},
              "mario" : {"name":"no_key_mario_23_7.png", "x_coord_upper_line": 23, "line_gap":7, "nb_bar_lines" : 8},
              "repeat": {"name":"no_key_repeat_bar_12_20.png", "x_coord_upper_line":12, "line_gap":20, "nb_bar_lines" : 5}}

for key in staff_info:
    score = staff_info[key]
    file_name = score['name']
    x_coord_upper_line = score['x_coord_upper_line']
    line_gap = score['line_gap']
    nb_bar_lines = score['nb_bar_lines']
    path = os.path.join(os.path.dirname(__file__), "pictures\\"+file_name)
    im = cv2.imread(path)
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im_blur = cv2.GaussianBlur(im_gray, (3, 3), 0)
    #_,imthres =cv2.threshold(im_blur, 127, 255, cv2.THRESH_BINARY_INV)
    im_adapt_thresh = cv2.adaptiveThreshold(im_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY_INV, 11, 2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    im_morph = cv2.morphologyEx(im_adapt_thresh, cv2.MORPH_CLOSE, kernel)


    im_skel = np.zeros(im_adapt_thresh.shape, np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

    while cv2.countNonZero(im_adapt_thresh) != 0:
        im_open = cv2.morphologyEx(im_adapt_thresh, cv2.MORPH_OPEN, element)
        temp = cv2.subtract(im_adapt_thresh, im_open)
        eroded = cv2.erode(im_adapt_thresh, element)
        im_skel = cv2.bitwise_or(im_skel, temp)
        im_adapt_thresh = eroded.copy()


    line_gap_coeffs = np.arange(1, 4.5, 0.01)
    to_int = np.vectorize(lambda x: int(x))
    vote_thres = to_int(line_gap_coeffs*line_gap)
    nb_lines_obtained = list()

    for threshold in vote_thres:
        lines = cv2.HoughLines(im_skel, 1, np.pi/180, threshold)
        nb_vert_lines = 0
        for rho, theta in lines[:,0]:
            if (theta==0) :
                nb_vert_lines+=1
        nb_lines_obtained.append(nb_vert_lines)
    
    plt.plot(line_gap_coeffs,nb_lines_obtained, "ro")
    xmin, xmax = plt.xlim()
    plt.hlines(nb_bar_lines, xmin, xmax)
    plt.xlim(xmin, xmax)
    plt.legend(["nb of vertical lines found", "expected number"], loc='best')
    plt.title("Score : "+file_name)
    plt.show()


# for rho, theta in lines[:,0]:
#     if (theta<2*np.pi/180) :
#         a = np.cos(theta)
#         b = np.sin(theta)
#         x0 = a*rho
#         y0 = b*rho
#         x1 = int(x0+1600*(-b))
#         y1 = int(y0+1600*a)
#         x2 = int(x0-1600*(-b))
#         y2 = int(y0-1600*a)
#         cv2.line(im,(x1,y1),(x2,y2),(0,0,255),2)

# plt.subplot(211)
# plt.imshow(im)
# plt.subplot(212)
# plt.imshow(im_skel)
# plt.show()

# # Displaying the final skeleton
# cv2.imshow("Skeleton",im_skel)
# cv2.waitKey(0)

