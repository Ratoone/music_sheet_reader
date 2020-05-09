import cv2
import pytest

from music_detection.key_enum import KeyEnum
from music_detection.time_enum import TimeSignatureEnum
from music_detection.utils.template_manager import TemplateManager
from music_detection.utils.template_matching import pick_template


@pytest.fixture(scope="session", autouse=True)
def template_manager():
    return TemplateManager("../resources/templates")


def test_key(template_manager):
    image = cv2.imread("../resources/test_images/twinkle.jpg")
    assert KeyEnum.SOL == pick_template(template_manager.clef, image)


def test_time(template_manager):
    image = cv2.imread("../resources/test_images/twinkle.jpg")
    assert TimeSignatureEnum.COMMON == pick_template(template_manager.time_signature, image)
