from typing import Tuple, List

import cv2
import numpy as np


def findLines(img: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Finds the staff lines in the image
    :param img: original image
    :return: a tuple consisting of the staff lines and the edge map
    """
    # remove noise
    kernel = np.ones((3, 3), np.float32) / 9
    dst = cv2.filter2D(img, -1, kernel)
    # convert the image to gray scale if the image is bgr
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    # canny_edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    # find the lines using Hough Transform
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 450)
    # sort the lines based on their distance from the origin (top left)
    linesSorted = np.sort(lines, axis=0)
    return linesSorted, edges


def cropImage(img: np.ndarray, splits: np.ndarray) -> List[np.ndarray]:
    """
    Splits the image using the splitting vector
    :param img: the image to be split
    :param splits: list containing splitting lines
    :return: a list of the resulting image crops
    """
    numberOfSplits = int(splits.shape[0])
    crop_img = []
    for i in range(numberOfSplits - 1):
        y = int(splits[i][0])
        h = int(splits[i + 1][0] - splits[i][0])
        crop_img.append(img[y:y + h, :])
    # add the last crop as well
    crop_img.append(img[int(splits[-1, 0]):, :])
    return crop_img


def removeStaff(edges: np.ndarray, staffLines: np.ndarray) -> np.ndarray:
    """
    Removes the staff lines from the edge map and performs a closing operation afterwards
    :param edges: the edge map image
    :param staffLines: the staff lines that will be removed
    :return: the edge map after removing the lines
    """
    # staffRemoval
    for i in range(staffLines.shape[0]):
        x = int(staffLines[i, 0][0])
        edges[x, :] = 0
    # do closing operation
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    return closing


def staffDetection(img: np.ndarray, removeLines: bool = True) -> Tuple[List[np.ndarray], int]:
    """
    Recognizes the staff lines from the image and crops each individual staff. May also remove the staff lines
    if requested.
    :param img: the rectified image of the music sheet
    :param removeLines: if True, the final image will not contain the staff lines
    :return: a list of images, each one corresponding to one staff, as well as the line gap in pixels
    """
    staffLines, edges = findLines(img)
    # find number of all the staff lines
    numberOfLines = int(staffLines.shape[0] / 2)
    # find number of staves (in twinkle case it is 3)
    numberOfStave = int(numberOfLines / 5)
    # find line Gap
    lineGap = staffLines[3, 0][0] - staffLines[2, 0][0]
    # make an empty matrix
    splittingLines = np.zeros((numberOfStave, 2))
    # split the title
    splittingLines[0][0] = staffLines[0, 0][0] - round((staffLines[10, 0][0] - staffLines[9, 0][0]) / 2)
    splittingLines[0][1] = staffLines[0, 0][1]
    for i in range(numberOfStave - 1):
        if i == (numberOfStave - 1):
            break
        s = 10 * (i + 1)
        splittingLines[i + 1][0] = staffLines[s - 1, 0][0] + round((staffLines[s, 0][0] - staffLines[s - 1, 0][0]) / 2)
        splittingLines[i + 1][1] = staffLines[s - 1, 0][1]

    if removeLines:
        edges = removeStaff(edges, staffLines)

    staffCrop = cropImage(edges, splittingLines)
    return staffCrop, lineGap
