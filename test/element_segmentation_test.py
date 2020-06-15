import os

import cv2

from music_detection.NoteDetection import elementSegmentation

def test_count_elements_successfully():
    path = os.path.dirname(os.path.abspath(__file__))
    image = cv2.imread(os.path.join(path, "../resources/test_images/twinkle_test_11.png"))
    crop_image = elementSegmentation(image)
    assert len(crop_image)==19



