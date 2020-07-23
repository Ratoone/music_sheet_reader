
import numpy as np
import cv2

from .measure import Measure
from .key_enum import KeyEnum
from .time_enum import TimeSignatureEnum
from .utils.template_manager import TemplateManager
from .utils.template_matching import pick_template


class Staff:
    def __init__(self, image: np.ndarray, line_gap):
        """
        Initialize the staff with a binary image and the line gap of the staff
        :param image:
        :param line_gap:
        """
        self.key = KeyEnum.UNDEFINED
        self.time_signature = TimeSignatureEnum.UNDEFINED
        self.measure_list = []
        self.line_gap = line_gap
        self.image = image #Actual picture of the staff
        self.tempo = 120 #overall tempo of the music score in bpm, default MIDI value is 120 bpm

    def segment_and_divide_staff(self, staff_img:np.ndarray) -> None:
        """
        Extracts the different elements in the staff image, and splits it into several measures
         :param staff_img: binary image of the staff, where staff lines have been removed.
        The notes, accidentals, etc... are expected to be in white.
        """
        res_array=cv2.connectedComponentsWithStats(self.image, connectivity=8)
        stats = res_array[2]
        stats=stats[stats[:,0].argsort()]
        bar_lines_index=self.__extract_bar_lines_info(stats)

        xmid_prec=0
        prec_index = 1
        for index in bar_lines_index :
            bar_line_info = stats[index]
            xmid = int(bar_line_info[0]+bar_line_info[2]/2)
            elements_info = stats[prec_index:index,:]
            elements_info[:,0] -= xmid_prec
            measure = Measure(staff_img[:, xmid_prec:xmid+1], elements_info, self.line_gap)
            self.measure_list.append(measure)
            xmid_prec = xmid
            prec_index=index+1

            if self.key == KeyEnum.UNDEFINED:
                self.key = measure.key
            if self.time_signature == TimeSignatureEnum.UNDEFINED:
                self.time_signature = measure.time_signature

    def __extract_bar_lines_info(self, stats:np.ndarray) -> np.ndarray :
        """
        Finds the bar lines in a list of element information
         :param stats: np.ndarray, list containing the element information, in the following order :
        [x_upper_left_corner, y_upper_left_corner, width, height,_]
         :return: np.ndarray, contains the indexes of the bar lines information in stats
        """
        ratio = stats[:,3]/stats[:,2]
        bar_lines_index = np.where(ratio >8.0)[0]
        return bar_lines_index
