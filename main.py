import cv2
import logging

from music_detection.key_enum import KeyEnum
from music_detection.staff import Staff
from music_detection.utils.StaffRemover import staffDetection
from music_detection.utils.midi_writer import MIDIWriter
from music_detection.utils.music_score_detector import find_music_score

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - [%(name)s] %(levelname)s: %(message)s")
    image = cv2.imread("resources/test_images/twinkle.jpg")
    # music_score = find_music_score(image)
    _, staves_binary, line_gap = staffDetection(image, True)
    midi_writer = MIDIWriter(1)
    previous_staff = None

    for staff_image in staves_binary:
        staff = Staff(staff_image, line_gap)
        if previous_staff is not None and staff.key in [KeyEnum.UNDEFINED, previous_staff.key]:
            staff.time_signature = previous_staff.time_signature

        previous_staff = staff
        midi_writer.addStaff(0, staff)

    midi_writer.writeToFile("output.mid")
