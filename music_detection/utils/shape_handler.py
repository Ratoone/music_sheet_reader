import os
from enum import Enum
from typing import Tuple, Union, List, Optional

import cv2
import numpy as np

from music_detection.key_enum import KeyEnum
from music_detection.note import Note
from music_detection.note_enum import NoteEnum
from music_detection.utils.template_manager import TemplateManager
from music_detection.utils.template_matching import pick_template

# TODO: open it from the configuration file
path = os.path.dirname(os.path.abspath(__file__))
template_manager = TemplateManager(os.path.join(path, "../../resources/templates"))

# the default note will be the Si4 - third line, Sol clef - as it is in the center of the image
DEFAULT_NOTE_PITCH = 7 * 4 + 6
MAXIMUM_PITCH_DIFFERENCE = 4


def get_adjusted_line_gap(line_gap: int) -> int:
    return int(line_gap * 0.7)


class ShapeHandler:
    @staticmethod
    def identify_shape(image: np.ndarray, upper_limit: int, element_height: int, key: KeyEnum, line_gap: int) -> Tuple[str, Optional[Union[List[Note], Note, Enum]]]:
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
        element_image = image[upper_limit:upper_limit + element_height, :]

        time = pick_template(template_manager.time_signature, element_image)
        if time is not None:
            return "time", time

        clef = pick_template(template_manager.clef, element_image)
        if clef is not None:
            return "clef", clef

        accidental = pick_template(template_manager.accidentals, element_image)
        if accidental is not None:
            return "accidental", accidental

        rest = pick_template(template_manager.rests, element_image)
        if rest is not None:
            return "rest", Note(NoteEnum.REST, 0, rest.value)

        # filter out the non-template elements that are far from the staff
        height, width = image.shape
        theoretical_pitch_distance = (height - 2 * upper_limit - element_height) / line_gap
        if abs(theoretical_pitch_distance) > MAXIMUM_PITCH_DIFFERENCE:
            return "invalid", None

        # dot detection
        if width < line_gap * 3 / 4:
            return "dot", None

        line_empty_gap = get_adjusted_line_gap(line_gap)
        element_image = cv2.erode(element_image, np.ones((1, 5), np.uint8), iterations=1)
        note_heads = cv2.HoughCircles(element_image, cv2.HOUGH_GRADIENT, 1.2, 2 * line_empty_gap, minRadius=int(0.7*line_empty_gap), maxRadius=line_empty_gap, param1=50, param2=5)
        if note_heads is not None:
            if len(note_heads[0]) == 1:
                if width > 3 * line_gap:
                    note_height = upper_limit + note_heads[0][0][1]
                elif note_heads[0][0][1] < element_height / 2:
                    note_height = upper_limit + line_gap / 2
                else:
                    note_height = upper_limit + element_height - line_gap / 2
                return "note", ShapeHandler.handle_single_note(image, key, line_gap, int(note_heads[0][0][0]), int(note_height), element_height)
            else:
                # multiple notes, assuming 1/8 notes
                note_list = []
                note_position_list = []
                for note_head in note_heads[0]:
                    not_a_note = False
                    for note_position in note_position_list:
                        if abs(note_head[0] - note_position) < 2 * line_gap:
                            not_a_note = True
                    if not_a_note:
                        continue
                    pitch = DEFAULT_NOTE_PITCH + int(np.round((height - 2 * (note_head[1] + upper_limit)) / line_gap))
                    note_list.append(Note.from_pitch_duration(pitch, 0.5))
                    note_position_list.append(note_head[0])

                # found some false positives, treat the compound as a single note
                if len(note_list) == 1:
                    return "note", ShapeHandler.handle_single_note(image, key, line_gap, int(note_heads[0][0][0]),
                                                                   int(note_heads[0][0][1]) + upper_limit, element_height)
                return "notes", [note for _, note in sorted(zip(note_position_list, note_list), key=lambda pair: pair[0])]

        return "invalid", None

    @staticmethod
    def handle_single_note(image: np.ndarray, key: KeyEnum, line_gap: int, note_center_h: int, note_center_v: int, element_height: int) -> Note:
        """
        If the identified object is a note, find its pitch by checking the vertical position in the staff
        :param element_height: the height of the connected component element
        :param note_center_h: the horizontal position of the center of the note
        :param note_center_v: the vertical position of the center of the note
        :param image: the object's cropped image from the music score
        :param key: the key of the staff - used to map the height to the pitch
        :param line_gap: the line gap, in pixels
        :return: a note object corresponding to the identified note
        """
        # TODO: include the possibility of being in a different scale - assuming Do Major
        # TODO: consider the 1/16th note as well
        height, width = image.shape
        # small element => no line, full note
        if element_height < 3 * line_gap:
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
