import cv2
import os
from music_detection.staff import Staff

file_name = "twinkle_test_11.png"
path=os.path.join(os.path.dirname(__file__), "measure_splitting\\pictures\\"+file_name)

im = cv2.imread(path)
staff = Staff(im)

cv2.imshow("Uncropped staff", staff.image)
cv2.waitKey(0)

staff.line_gap = 11
staff.identify_measures()
for measure in staff.measure_list:
    cv2.imshow("Measure", measure.image)
    cv2.waitKey(0)