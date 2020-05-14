# Python program to read image using OpenCV
# importing OpenCV(cv2) module
import PIL
import cv2
import numpy as np
from PIL import Image


# Read the image
img = cv2.imread('twinkle.jpeg')


def PreProccesing(img):
    # remove noise
    kernel = np.ones((3, 3), np.float32) / 9
    dst = cv2.filter2D(img, -1, kernel)
    # convert the image to gray scale if the image is bgr
    if len(dst.shape) == 3:
        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    # Otsu's thresholding
    # ret2,th2 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # canny_edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    # find the lines using Hough Transform
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 450)
    # sort the lines based on their distance from the origin (top left)
    linesSorted = np.sort(lines, axis=0)
    return linesSorted, edges


def staffDetection(img):
    linesSorted, edges = PreProccesing(img)
    # find number of all the staff lines
    numberOfLines = int(linesSorted.shape[0] / 2)
    # find number of staves (in twinkle case it is 3)
    numberOfStave = int(numberOfLines / 5)
    # find line Gap
    lineGap = linesSorted[3, 0][0] - linesSorted[2, 0][0]
    # make an empty matrix
    distance = np.zeros((numberOfStave, 2))
    # put all the half distances in the d matrix
    distance[0][0] = linesSorted[0, 0][0] - round((linesSorted[10, 0][0] - linesSorted[9, 0][0]) / 2)
    distance[0][1] = linesSorted[0, 0][1]
    for i in range(numberOfStave - 1):
        if i == (numberOfStave - 1):
            break
        s = int((numberOfLines * 2 / numberOfStave) * (i + 1))
        distance[i + 1][0] = linesSorted[s - 1, 0][0] + round((linesSorted[s, 0][0] - linesSorted[s - 1, 0][0]) / 2)
        distance[i + 1][1] = linesSorted[s - 1, 0][1]
    return distance


distance = staffDetection(img)


def CropImage(distance):
    numberOfStave = int(distance.shape[0])
    crop_img = []
    for i in range(numberOfStave - 1):
        y = int(distance[i][0])
        h = int(distance[i + 1][0] - distance[i][0])
        crop_img.append(img[y:y + h, :, :])
    return crop_img


linesSorted, edges = PreProccesing(img)


def StaffRemoval(img):
    # staffRemoval
    for i in range(linesSorted.shape[0]):
        x = int(linesSorted[i, 0][0])
        edges[x, :] = 0
    # do closing operation
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    # complement of the image
    imageComp = cv2.bitwise_not(closing)
    return imageComp


imageComp = StaffRemoval(img)
cv2.imshow('r', imageComp)
cv2.waitKey(0)
'''
# this is to test how the lines are found
for rho, theta in linesSorted[:, 0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 2000 * (-b))
    y1 = int(y0 + 2000 * (a))
    x2 = int(x0 - 2000 * (-b))
    y2 = int(y0 - 2000 * (a))
    cv2.imshow('img',img)
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)
    cv2.waitKey(0)
cv2.imwrite('houghlines3.jpg', img)
'''
