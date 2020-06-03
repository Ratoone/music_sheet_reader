import cv2
import numpy as np

def elementSegmentation(im):
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    gray = cv2.normalize(gray, None, 0, 0.53, cv2.NORM_MINMAX)
    verticalProj = np.sum(gray, 0)
    mean = np.mean(verticalProj)
    elementLoc = []
    for i in range(len(verticalProj)):
        if i == len(verticalProj) - 1:
            break
        if verticalProj[i] > mean:
            elementLoc.append(i)

    bounding = []
    for i in range(len(elementLoc) - 1):
        if elementLoc[i + 1] - elementLoc[i] > 1:
            bounding.append((elementLoc[i],elementLoc[i+1]))

    crop_img = []
    for i in range(len(bounding) - 1):
        x = bounding[i][1] - bounding[i][0]
        crop_img.append(im[:, bounding[i][0]:bounding[i][0]+x])

    return crop_img

