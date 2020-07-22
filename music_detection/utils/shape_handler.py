import os
from typing import Tuple

import cv2
import numpy as np

from music_detection.key_enum import KeyEnum
from music_detection.note import Note
from music_detection.utils.template_manager import TemplateManager
from music_detection.utils.template_matching import pick_template

# TODO: open it from the configuration file
path = os.path.dirname(os.path.abspath(__file__))
template_manager = TemplateManager(os.path.join(path, "../../resources/templates"))

# the default note will be the Si4 - third line, Sol clef - as it is in the center of the image
DEFAULT_NOTE_PITCH = 7 * 4 + 6
MAXIMUM_PITCH_DIFFERENCE = 4


def get_adjusted_line_gap(line_gap: int) -> int:
    return int(line_gap * 0.8)


class ShapeHandler:
    @staticmethod
    def identify_shape(image: np.ndarray, upper_limit: int, element_height: int, key: KeyEnum, line_gap: int) -> Tuple[str, object]:
        """
        Identify the current shape using various methods: template matching, hough transform, etc.
        :param upper_limit: the upper bound of the identified element
        :param element_height: the height of the element in the image
        :param image: the element to be identified
        :param key: the key of the staff. Useful for identifying the right pitch of the note
        :param line_gap: the line gap in pixels between two staff lines. Useful for notes
        :return: a string denoting the type of element found and an object relevant to that type.
        For instance, a note will return a Note, a clef will return an Enum, etc.
        """
        clef = pick_template(template_manager.clef, image)
        if clef is not None:
            return "clef", clef

        time = pick_template(template_manager.time_signature, image)
        if time is not None:
            return "time", time

        # filter out the non-template elements that are far from the staff
        height, _ = image.shape
        theoretical_pitch_distance = (height - 2 * upper_limit - element_height) / line_gap
        if abs(theoretical_pitch_distance) > MAXIMUM_PITCH_DIFFERENCE:
            return "invalid", None

        line_empty_gap = get_adjusted_line_gap(line_gap)
        note_heads = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1.2, line_empty_gap, minRadius=int(0.7*line_empty_gap), maxRadius=line_empty_gap, param1=50, param2=5)
        if note_heads is not None:
            # TODO: assuming single note, fix for 2 eights
            return "note", ShapeHandler.handle_note(image, key, line_gap, int(note_heads[0][0][0]), int(note_heads[0][0][1]))

        return "invalid", None

    @staticmethod
    def handle_note(image: np.ndarray, key: KeyEnum, line_gap: int, note_center_h: int, note_center_v: int) -> Note:
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
        height, width = image.shape
        # no line => full note
        lines = cv2.HoughLinesP(image, 1, np.pi / 180, int(line_gap * 2.5))
        if lines is None:
            note_duration = 4
        else:
            # center is empty (i.e. average around center is black) => half note
            if np.average(image[
                          note_center_v - line_gap//4:
                          note_center_v + line_gap//4,
                          note_center_h - line_gap//4:
                          note_center_h + line_gap//4]) < 0.75 * 255:
                note_duration = 2
            else:
                # width is no bigger than 2 line gaps (implying the existence of the little flags)
                if width < 2 * line_gap:
                    note_duration = 1
                else:
                    note_duration = 0.5

        # count the increments of half line gap between the note and the third line
        note_pitch = DEFAULT_NOTE_PITCH + int(np.round((height - 2 * note_center_v) / line_gap))
        # adapt the note to the key
        if key == KeyEnum.FA:
            note_pitch -= 12
        if key == KeyEnum.DO:
            note_pitch -= 6
        return Note.from_pitch_duration(note_pitch, note_duration)
