import cv2
import os
import pytest
from music_detection.staff import Staff


@pytest.fixture(scope="session", autouse=True)

def test_bar_lines():
    file_name = "twinkle_test_11.png"
    path=os.path.join(os.path.dirname(__file__), "measure_splitting\\pictures\\"+file_name)

    im = cv2.imread(path)
    staff = Staff(im)
    staff.line_gap = 11
    staff.identify_measures()
    
    assert len(staff.measure_list)==4
