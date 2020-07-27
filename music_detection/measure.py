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
        self.scale = 0
        self.image = image #Actual picture of the staff

        #array containing information about the different elements in the measure
        #these information are stored in the following order :
        #[x_upper_left_corner, y_upper_left_corner, width, height,_]
        self.elements_info=elements_info
        self.identify_elements()

    def identify_elements(self):
        previous_element_type = ""
        previous_element_value = None
        previous_element_h = 0
        for element in self.elements_info:
            element_type, element_value = ShapeHandler.identify_shape(self.image[:, element[0]:element[0]+element[2]], element[1], element[3], self.key, self.line_gap)
            if element_type == "clef":
                self.key = element_value
            if element_type == "time":
                self.time_signature = element_value
            if element_type == "rest":
                self.note_list.append(element_value)
            if element_type == "accidental":
                if previous_element_type in ["clef", "accidental"]:
                    self.scale += element_value.value

            if element_type == "note":
                if previous_element_type == "accidental" and element[0] - previous_element_h < self.line_gap:
                    element_value.accidental = previous_element_value
                element_value.update_scale(self.scale)
                self.note_list.append(element_value)

            if element_type == "dot" and previous_element_type == "note":
                # filter false positives
                if element[0] > previous_element_h and element[0] - previous_element_h < 2 * self.line_gap:
                    import cv2
                    image = cv2.rectangle(self.image, (element[0],element[1]), (element[0]+element[2], element[1]+element[3]), 125, 2)
                    cv2.imshow("", image)
                    cv2.waitKey()
                    self.note_list[-1].duration *= 1.5
                else:
                    element_type = "invalid"

            if element_type != "invalid":
                previous_element_type = element_type
                previous_element_value = element_value
                previous_element_h = element[0]+element[2]
