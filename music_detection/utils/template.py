from enum import Enum

import cv2

from music_detection.utils.preprocessing_functions import generate_thresholded_image


class Template:
    """
    Holds the image template and the type of template. Should probably better be a generic type
    with the enum type.
    """
    def __init__(self, path: str, enum_type: Enum):
        self.template = generate_thresholded_image(cv2.imread(path), True)
        self.type = enum_type
