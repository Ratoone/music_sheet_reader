import os

import cv2

from music_detection.staff import Staff
from music_detection.utils.StaffRemover import generate_thresholded_image

path = os.path.dirname(os.path.abspath(__file__))


def scale_test():
    image = cv2.imread(os.path.join(path, "../resources/test_images/scale_test.jpg"))
    image = generate_thresholded_image(image, True)
    staff = Staff(image, 0)
    staff.segment_and_divide_staff(image)
    assert staff.scale == 2


if __name__ == '__main__':
    scale_test()