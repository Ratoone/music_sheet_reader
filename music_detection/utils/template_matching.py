from enum import Enum

import cv2
import numpy as np
from typing import List, Tuple, Optional

from music_detection.utils.template import Template

# TODO: move this to some configuration file
MIN_SCALE = 0.3
MAX_SCALE = 1.5
SCALE_INCREMENT = 0.05


def match(template: np.array, image: np.array) -> Tuple[float, Tuple]:
    """
    Looks for the template in image and returns the correlation score and position using multi-scale search.
    This assumes the image is rectified beforehand.
    :param template: the template to be found
    :param image: original image
    :return: tuple representing the correlation value and the position in image of the template found
    """
    found = None

    # scale the template at multiple values
    for scale in np.linspace(MIN_SCALE, MAX_SCALE, int((MAX_SCALE - MIN_SCALE) / SCALE_INCREMENT)):
        resized_template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        if resized_template.shape[0] > image.shape[0] or resized_template.shape[1] > image.shape[1]:
            break

        # perform template matching and pick the best result
        result = cv2.matchTemplate(image, resized_template, cv2.TM_CCOEFF_NORMED)
        (_, correlation, _, max_position) = cv2.minMaxLoc(result)
        # compare with old best result and update scale
        if found is None or correlation > found[0]:
            found = (correlation, max_position, scale)

    (correlation, position, scale) = found
    return correlation, position


def pick_template(template_list: List[Template], image: np.array, threshold=0.7) -> Optional[Enum]:
    """
    Pick the best matching template from the list.
    :param template_list: the list of templates to pick from
    :param image: the original image
    :param threshold: the correlation threshold below which the template will be considered to not be found
    :return: the enum type of the best template, or None if no template score exceeds the threshold value
    """
    max_score = 0
    enum_type = 0

    for template in template_list:
        score, _ = match(template.template, image)
        if score > max_score:
            enum_type = template.type
            max_score = score

    # if the score is lower than the threshold, no template was actually found
    if max_score < threshold:
        return None
    return enum_type
