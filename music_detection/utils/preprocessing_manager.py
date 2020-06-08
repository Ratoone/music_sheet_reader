import cv2
import numpy as np

class PreprocessingManager :
    def __init__(self, img:np.ndarray=None):
        self.image=img 

    def generate_edge_map(self, binary_inv:bool=True) -> np.ndarray :
        """
        Perform an edge detection using Canny algorithm on PreprocessingManager.image \n
         :param binary_inv: bool, if true the edges are in white on the resulting edge map. They are black otherwise.
         :return : np.ndarray, binary image containing the edges found  
        """
        kernel = np.ones((3, 3), np.float32) / 9
        dst = cv2.filter2D(self.image, -1, kernel)
        # canny_edge detection
        edges = cv2.Canny(dst, 50, 150, apertureSize=3)

        if binary_inv ==False :
            edges = 255-edges
        
        return edges

    def generate_thresholded_image(self, binary_inv:bool=True) -> np.ndarray :
        """
        Thresholds PreprocessingManager.image \n
         :param binary_inv: bool, if true the black regions of the original image are in white on the resulting edge map. Otherwise they remain black
         :return: np.ndarray, thresholded image
        """
        im_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        im_blur = cv2.GaussianBlur(im_gray, (3, 3), 0)
        im_adapt_thresh = cv2.adaptiveThreshold(im_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                            cv2.THRESH_BINARY_INV, 11, 2)
        #Closing operation
        #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        #im_morph = cv2.morphologyEx(im_adapt_thresh, cv2.MORPH_CLOSE, kernel)

        im_morph=im_adapt_thresh.copy()
        
        if binary_inv ==False :
            im_morph=255-im_morph
        
        return im_morph




        
