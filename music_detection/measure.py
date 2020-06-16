import numpy as np

class Measure:
    def __init__(self, image:np.ndarray=None,elements_info:np.ndarray=np.empty(0)):
        self.position_in_image = []
        self.note_list = []
        self.time_signature = 0
        self.image = image #Actual picture of the staff

        #array containing information about the different elements in the measure
        #these information are stored in the following order :
        #[x_upper_left_corner, y_upper_left_corner, width, height,_]
        self.elements_info=elements_info 

    def identify_notes(self):
        pass

    def reconstruct_notes(self):
        pass
