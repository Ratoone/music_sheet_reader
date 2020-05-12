import os

import cv2
import matplotlib.pyplot as plt
import numpy as np


staff_info = {"twinkle":{"name":"no_key_twinkle_42_11.jpg", "x_coord_upper_line": 42, "line_gap":11, "nb_bar_lines" : 3},
              "mario" : {"name":"no_key_mario_23_7.png", "x_coord_upper_line": 23, "line_gap":7, "nb_bar_lines" : 8},
              "repeat": {"name":"no_key_repeat_bar_12_20.png", "x_coord_upper_line": 12, "line_gap":20, "nb_bar_lines" : 5}}


score = staff_info['twinkle']
file_name = score['name']
file_name = 'twinkle_test_11.png'
x_coord_upper_line = score['x_coord_upper_line']
line_gap = score['line_gap']
nb_bar_lines = score['nb_bar_lines']
vote_threshold = int(3.25*line_gap)

path = os.path.join(os.path.dirname(__file__), "pictures\\"+file_name)
im = cv2.imread(path)
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im_blur = cv2.GaussianBlur(im_gray, (3, 3), 0)
#_,imthres =cv2.threshold(im_blur, 127, 255, cv2.THRESH_BINARY_INV)
im_adapt_thresh = cv2.adaptiveThreshold(im_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                    cv2.THRESH_BINARY_INV, 11, 2)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
im_morph = cv2.morphologyEx(im_adapt_thresh, cv2.MORPH_CLOSE, kernel)

im_skel = np.zeros(im_morph.shape, np.uint8)
element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
while cv2.countNonZero(im_morph) != 0:
    im_open = cv2.morphologyEx(im_morph, cv2.MORPH_OPEN, element)
    temp = cv2.subtract(im_morph, im_open)
    eroded = cv2.erode(im_morph, element)
    im_skel = cv2.bitwise_or(im_skel, temp)
    im_morph = eroded.copy()

lines = cv2.HoughLines(im_skel,1,np.pi/180,vote_threshold)
bar_lines_loc = list()
for rho, theta in lines[:, 0] :
    if theta==0 :
        bar_lines_loc.append(int(round(rho)))

#That part is just here to display the bar lines
#
#         y1 = x_coord_upper_line
#         x1 = int(rho)
#         x2 = int(rho)
#         y2 = x_coord_upper_line+5*line_gap
#         cv2.line(im,(x1,y1),(x2,y2),(0,0,255),2)
# plt.subplot(211)
# plt.imshow(im)
# plt.title("Vote threshold={}".format(vote_threshold))
# plt.subplot(212)
# plt.imshow(imskel)
# plt.show()

bar_lines_loc.sort()
prev_boundary = 0
measure_list = list()
for next_boundary in bar_lines_loc :
    if next_boundary-prev_boundary > 2*line_gap :
        measure_list.append(im[:, prev_boundary+1:next_boundary])
    else:
        measure_list.append(measure_list[-1])
    prev_boundary = next_boundary

for measure in measure_list :
    cv2.imshow('measure', measure)
    cv2.waitKey(0)

