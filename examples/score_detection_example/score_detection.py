import os
import cv2
from music_detection.utils.music_score_detector import *

path  = os.path.join(os.path.dirname(__file__), "paper_test.jpg")

image = cv2.imread(path)
paper = find_music_score(image)

cv2.imshow("result", scale_image(paper))
cv2.waitKey(0)
