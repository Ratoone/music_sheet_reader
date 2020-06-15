import cv2
import numpy as np

from music_detection.key_enum import KeyEnum
from music_detection.note import Note


class ShapeManager:
    @staticmethod
    def identify_shape(image: np.ndarray, key: KeyEnum, line_gap: int):
        # TODO: implement template matching to identify what kind of element is the current one
        pass

    @staticmethod
    def handle_note(image: np.ndarray, key: KeyEnum, line_gap: int, note_center_position: int) -> Note:
        """
        If the identified object is a note, find its pitch by checking the vertical position in the staff
        :param note_center_position: the position of the center of the note
        :param image: the object's cropped image from the music score
        :param key: the key of the staff - used to map the height to the pitch
        :param line_gap: the line gap, in pixels
        :return: a note object corresponding to the identified note
        """
        # TODO: include the possibility of being in a different scale - assuming Do Major
        # TODO: consider the 1/16th note as well
        note_duration = 0
        height, width = image.shape
        # no line => full note
        lines = cv2.HoughLinesP(image, 1, np.pi / 180, int(line_gap * 2.5))
        if lines is None:
            note_duration = 4
        else:
            # center is empty => half note
            if image[note_center_position, width // 2] == 0:
                note_duration = 2
            else:
                # width is no bigger than 2 line gaps (implying the existence of the little flags)
                if width < 2 * line_gap:
                    note_duration = 1
                else:
                    note_duration = 0.5

        # the default note will be the Si4 - third line, Sol clef - as it is in the center of the image
        default_note_pitch = 7 * 4 + 6
        # count the increments of half line gap between the note and the third line
        note_pitch = default_note_pitch + (height//2 - note_center_position) / (line_gap // 2)
        # adapt the note to the key
        if key == KeyEnum.FA:
            note_pitch -= 12
        if key == KeyEnum.DO:
            note_pitch -= 6
        return Note.from_pitch_duration(note_pitch, note_duration)


if __name__ == '__main__':
    image = cv2.imread("../../resources/test_images/sol_quarter.png")
    im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    im_blur = cv2.GaussianBlur(im_gray, (3, 3), 0)
    _, im_adapt_thresh = cv2.threshold(im_blur, 127, 255, cv2.THRESH_BINARY_INV)
    ShapeManager.handle_note(im_adapt_thresh, KeyEnum.UNDEFINED, 12, 3, 3)
