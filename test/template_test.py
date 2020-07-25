import os

import cv2
import pytest

from music_detection.key_enum import KeyEnum
from music_detection.time_enum import TimeSignatureEnum
from music_detection.utils.preprocessing_functions import generate_thresholded_image
from music_detection.utils.template_manager import TemplateManager
from music_detection.utils.template_matching import pick_template


path = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="session", autouse=True)
def template_manager():
    print(os.path.join(path, "../resources/templates"))
    return TemplateManager(os.path.join(path, "../resources/templates"))


def test_key(template_manager):
    image = cv2.imread(os.path.join(path, "../resources/test_images/template_test.jpg"))
    image = generate_thresholded_image(image, True)
    assert KeyEnum.SOL == pick_template(template_manager.clef, image)


def test_time(template_manager):
    image = cv2.imread(os.path.join(path, "../resources/test_images/template_test.jpg"))
    image = generate_thresholded_image(image, True)
    assert TimeSignatureEnum.COMMON == pick_template(template_manager.time_signature, image)
