import cv2
import numpy as np
from matplotlib import pyplot as plt

img_rgb = cv2.imread('fire.jpg')
img_rgb = cv2.resize(img_rgb, (0,0), fx=0.5, fy=0.5)
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

template = cv2.imread('flat-space.png', 0)
template = cv2.resize(template, (0,0), fx=0.5, fy=0.5)
# for sharp-line threshold=0.7
# for flat threshold=0.7
threshold=0.7

template_1=cv2.imread('flat-line.png',0)
template_1 = cv2.resize(template_1, (0,0), fx=0.5, fy=0.5)

w, h = template.shape[::-1]
w, h = template_1.shape[::-1]



res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.7
if res is not None:
    loc = np.where(res >= threshold)
    #print(res)
    # print(loc)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 1)

else:

    res = cv2.matchTemplate(img_gray, template_1, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (255, 255, 0), 2)

""""
res = cv2.matchTemplate(img_gray, template_1, cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (255,255,0), 2)
"""
#cv2.imshow('match', img_rgb)
cv2.imwrite('output.png', img_rgb)

cv2.waitKey(0)
cv2.destroyAllWindows()