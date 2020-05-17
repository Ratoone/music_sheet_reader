import cv2
import numpy as np


def findLines(img):
    # remove noise
    kernel = np.ones((3, 3), np.float32) / 9
    dst = cv2.filter2D(img, -1, kernel)
    # convert the image to gray scale if the image is bgr
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
    linesSorted, _ = findLines(img)
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
    return distance, lineGap


def cropImage(distance, img):
    numberOfStave = int(distance.shape[0])
    crop_img = []
    for i in range(numberOfStave - 1):
        y = int(distance[i][0])
        h = int(distance[i + 1][0] - distance[i][0])
        crop_img.append(img[y:y + h, :, :])
    return crop_img


def removeStaff(edges, staffLines):
    # staffRemoval
    for i in range(staffLines.shape[0]):
        x = int(staffLines[i, 0][0])
        edges[x, :] = 0
    # do closing operation
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    # complement of the image
    imageComp = cv2.bitwise_not(closing)
    return imageComp
