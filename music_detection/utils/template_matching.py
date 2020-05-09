from enum import Enum

import cv2
import numpy as np
from typing import List, Tuple

from music_detection.utils.template import Template


def match(template: np.array, image: np.array) -> Tuple[float, Tuple]:
    """
    Looks for the template in image and returns the correlation score and position using multi-scale search
    :param template: the template to be found
    :param image: original image
    :return: tuple representing the correlation value and the position in image of the template found
    """
    found = None

    for scale in np.linspace(0.5, 1.5, 20):
        resized_template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        if resized_template.shape[0] > image.shape[0] or resized_template.shape[1] > image.shape[1]:
            break

        result = cv2.matchTemplate(image, resized_template, cv2.TM_CCOEFF_NORMED)
        (_, confidence, _, max_position) = cv2.minMaxLoc(result)
        if found is None or confidence > found[0]:
            found = (confidence, max_position, scale)

    (score, position, scale) = found
    return score, position


def pick_template(template_list: List[Template], image: np.array) -> Enum:
    max_score = 0
    enum_type = 0

    for template in template_list:
        score, _ = match(template.template, image)
        if score > max_score:
            enum_type = template.type
            max_score = score

    return enum_type
