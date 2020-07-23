import cv2
import os, sys

sys.path.append(os.getcwd())

from music_detection.utils.StaffRemover import *
from music_detection.staff import Staff
from music_detection.measure import Measure

def draw_elements(measure:Measure) -> np.ndarray :
    """Small function that draws rectangles over the different elements in the measure image"""
    measure_img = measure.image.copy()
    for element in measure.elements_info :
        xstart, ystart, width, height,_=element
        cv2.rectangle(measure_img, (xstart-2, ystart-2), (xstart+width+2, ystart+height+2), (0,0,255),2)
    return measure_img

img = cv2.imread("resources/test_images/music_score.jpeg")
if img.shape[0] == 0 :
        raise FileNotFoundError("can't open file")

staves, staves_bin,_ = staffDetection(img)

staff =Staff(staves[0], None)
staff.segment_and_divide_staff(staves_bin[0])

for i,measure in enumerate(staff.measure_list) :
    cv2.imshow(str(i), draw_elements(measure))
cv2.waitKey()


