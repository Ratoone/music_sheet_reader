
import numpy as np
import cv2

from .measure import Measure
from .key_enum import KeyEnum
from .time_enum import TimeSignatureEnum
from .utils.template_manager import TemplateManager
from .utils.template_matching import pick_template


class Staff:
    def __init__(self, image: np.ndarray):
        self.key = KeyEnum.UNDEFINED
        self.time_signature = TimeSignatureEnum.UNDEFINED
        self.measure_list = []
        self.image = image #Actual picture of the staff
        self.line_gap = 0 #Added it just to signify that i need it from a previous processing
        self.tempo = 120 #overall tempo of the music score in bpm, default MIDI value is 120 bpm  
    
    def identify_measures(self) -> None:
        """Split the staff into different Measure objects stored in measure_list"""
        vote_threshold = int(3.25*self.line_gap) #Determined experimentally

        #TODO : put the preprocessing part in another function, so that it is performed only once
        #for both bar and staff lines detection
        im_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        im_blur = cv2.GaussianBlur(im_gray, (3, 3), 0)
        im_adapt_thresh = cv2.adaptiveThreshold(im_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                            cv2.THRESH_BINARY_INV, 11, 2)
        #Closing operation
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        im_morph = cv2.morphologyEx(im_adapt_thresh, cv2.MORPH_CLOSE, kernel)

        #Skeletonization
        im_skel = np.zeros(im_morph.shape, np.uint8)
        element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        while cv2.countNonZero(im_morph) != 0:
            im_open = cv2.morphologyEx(im_morph, cv2.MORPH_OPEN, element)
            temp = cv2.subtract(im_morph, im_open)
            eroded = cv2.erode(im_morph, element)
            im_skel = cv2.bitwise_or(im_skel, temp)
            im_morph = eroded.copy()

        #Extraction of bar lines'x-coordinates
        lines = cv2.HoughLines(im_skel, 1, np.pi/180, vote_threshold)
        bar_lines_loc = list()
        for rho, theta in lines[:,0]:
            if theta< 3*np.pi/180: #only vertical (or almost vertical) lines are kept
                bar_lines_loc.append(int(round(rho)))
        
        bar_lines_loc.sort() #Necessary because bar lines are found in a random order
        prev_boundary = 0
        for next_boundary in bar_lines_loc :
            
            #If the 2 lines are far enough from each other, the measure in-between is simply
            #added to the list
            if next_boundary-prev_boundary > 2*self.line_gap: 
                measure = Measure(self.image[:, prev_boundary+1:next_boundary])#Measure is cropped
                self.measure_list.append(measure)
            else: 
                #Otherwise it means that the previous mesure has to be repeated
                #TODO : find an efficient way to differenciate repeating measures (: ||)
                #from the end of a music score (||) 
                self.measure_list.append(self.measure_list[-1])
            prev_boundary = next_boundary
