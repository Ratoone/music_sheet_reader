from enum import Enum

import cv2


class Template:
    def __init__(self, path: str, enum_type: Enum):
        self.template = cv2.imread(path)
        self.type = enum_type
