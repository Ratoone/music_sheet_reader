from typing import Tuple, List
from enum import Enum
import cv2
import numpy as np
from music_detection.utils.preprocessing_functions import *

def findLines(edges: np.ndarray) -> np.ndarray:
    """
    Finds the staff lines in the edge map
    :param edges: original binary edge map (edges are expected to be in white)
    :return: np.ndarray, array containing the staff lines information
    """
    # find the lines using Hough Transform
    threshold = int(edges.shape[1]/2)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold)
    # sort the lines based on their distance from the origin (top left)
    linesSorted = np.sort(lines, axis=0)
    return linesSorted


def cropImage(img: np.ndarray, splits: np.ndarray) -> List[np.ndarray]:
    """
    Splits the image using the splitting vector
    :param img: the image to be split
    :param splits: list containing splitting lines
    :return: a list of the resulting image crops
    """
    numberOfSplits = int(splits.shape[0])
    crop_img = []
    h = 0
    for i in range(numberOfSplits - 1):
        y = int(splits[i][0])
        h = int(splits[i + 1][0] - splits[i][0])
        crop_img.append(img[y:y + h, :])

    # add the last crop as well - make sure it has the same size as the rest
    last_crop = img[int(splits[-1, 0]):, :]
    if last_crop.shape[0] < h:
        background_color = last_crop[-1, -1]
        for i in range(h - last_crop.shape[0]):
            last_crop = np.append(last_crop, [last_crop.shape[1] * list([background_color])], axis=0)
    else:
        last_crop = last_crop[:h, :]
    crop_img.append(last_crop)
    return crop_img


def removeStaff(binarized_music_score: np.ndarray, staff_lines:np.ndarray, number_of_staves:int) -> np.ndarray :
    """
    Removes the staff lines from a binarized music score \n
     :param binarized_music_score: np.ndarray, binary image of a music score
     :param staff_lines: np.ndarray, staff lines edges obtained with the Hough transform
     :param number_of_staves: int, number of staves in the image
     :return : np.ndarray, music score without its staff lines
    """
    _,width=binarized_music_score.shape
    staff_lines_erased = binarized_music_score.copy()
    for staff_number in range(number_of_staves) : 
        for i in range(0,10,2) :# It is assumed that a staff = 5 staff lines
            lower_lim=int(staff_lines[staff_number*10+i,0,0])
            upper_lim=int(staff_lines[staff_number*10+i+1,0,0]+1)
            for col in range(width) :
                if (binarized_music_score[lower_lim-1, col]==0) and (binarized_music_score[upper_lim+1,col]==0) :
                    staff_lines_erased[lower_lim:upper_lim, col]=0

    #Closing operation
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    staff_lines_erased = cv2.morphologyEx(staff_lines_erased, cv2.MORPH_CLOSE, kernel)  
    return staff_lines_erased


def staffDetection(img: np.ndarray, removeLines: bool = True) -> Tuple[List[np.ndarray],List[np.ndarray], int]:
    """
    Recognizes the staff lines from the image and crops each individual staff. May also remove the staff lines
    if requested.
    :param img: the rectified image of the music sheet
    :param removeLines: if True, the final image will not contain the staff lines
    :return: a list of staff images, a list of binarized staff images where staff lines have been removed, and the line gap in pixels
    """
    edge_map =generate_edge_map(img)
    im_morph = generate_thresholded_image(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = 255 - img

    staffLines = findLines(edge_map)
    # find number of all the staff lines
    numberOfLines = int(staffLines.shape[0] / 2)
    # find number of staves (in twinkle case it is 3)
    numberOfStave = int(numberOfLines / 5)
    # find line Gap
    lineGap = staffLines[3, 0][0] - staffLines[1, 0][0]
    # make an empty matrix
    splittingLines = np.zeros((numberOfStave, 2))
    # split the title
    splittingLines[0,0] = staffLines[0, 0][0] - round((staffLines[10, 0][0] - staffLines[9, 0][0]) / 2)
    splittingLines[0,1] = staffLines[0, 0][1]
    for i in range(numberOfStave -1):
        s = 10 * (i + 1)
        splittingLines[i + 1][0] = staffLines[s - 1, 0][0] + round((staffLines[s, 0][0] - staffLines[s - 1, 0][0]) / 2)
        splittingLines[i + 1][1] = staffLines[s - 1, 0][1]

    if removeLines:
        im_morph = removeStaff(im_morph, staffLines, numberOfStave)
    staff_crop = cropImage(img, splittingLines)
    staff_bin_crop = cropImage(im_morph, splittingLines)

    return staff_crop, staff_bin_crop, int(lineGap)
