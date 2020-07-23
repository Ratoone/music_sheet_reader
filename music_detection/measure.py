import numpy as np

from music_detection.key_enum import KeyEnum
from music_detection.time_enum import TimeSignatureEnum
from music_detection.utils.shape_handler import ShapeHandler


class Measure:
    def __init__(self, image:np.ndarray=None,elements_info:np.ndarray=np.empty(0), line_gap : int = 0):
        self.position_in_image = []
        self.note_list = []
        self.time_signature = TimeSignatureEnum.UNDEFINED
        self.line_gap = line_gap
        self.key = KeyEnum.UNDEFINED
        self.image = image #Actual picture of the staff

        #array containing information about the different elements in the measure
        #these information are stored in the following order :
        #[x_upper_left_corner, y_upper_left_corner, width, height,_]
        self.elements_info=elements_info
        self.identify_elements()

    def identify_elements(self):
        for element in self.elements_info:
            element_type, element_value = ShapeHandler.identify_shape(self.image[:, element[0]:element[0]+element[2]], element[1], element[3], self.key, self.line_gap)
            if element_type == "clef":
                self.key = element_value
            if element_type == "time":
                self.time_signature = element_value
            if element_type == "rest":
                self.note_list.append(element_value)
            if element_type == "accidental":
                # TODO: handle accidentals
                pass
            if element_type == "note":
                self.note_list.append(element_value)
