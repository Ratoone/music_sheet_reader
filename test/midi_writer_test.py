import pytest

from music_detection.staff import Staff
from music_detection.utils.midi_writer import *

@pytest.fixture(scope="session", autouse=True)

def test_track_creation():
    mw = MIDIWriter(4)
    assert (len(mw.track_list)==4 and type(mw.track_list[0])==Track)

def test_staff_appen():
    mw = MIDIWriter(3)
    for i in range(4) :
        staff = Staff(None,0)
        mw.addStaff(1,staff)
    assert (len(mw.track_list[1].staff_list)==4 and type(mw.track_list[1].staff_list[0])== Staff)
