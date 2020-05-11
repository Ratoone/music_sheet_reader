from enum import Enum

import cv2


class Template:
    """
    Holds the image template and the type of template. Should probably better be a generic type
    with the enum type.
    """
    def __init__(self, path: str, enum_type: Enum):
        self.template = cv2.imread(path)
        self.type = enum_type
