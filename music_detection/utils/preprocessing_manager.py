import cv2
import numpy as np

from preprocessing_operations_enum import PreprocessingOperationEnum as PEnum

class PreprocessingManager :
    """Manages a whole preprocessing workflow, all operations are performed in-place,\n
    can be retrieved any time by accessing the processed_img attribute
     :img_to_be_processed: numpy ndarray, initial image, format does not matter
     :operations_list: list of preprocessing operations to perform, this list has to like that :
     [operation1:PEnum, [operation2:PEnum, arg1, arg2, ...], operation3:PEnum,...]. Refer to the __perform_operation method
     for more detailed explanations
    """
    def __init__(self,img_to_be_processed:np.ndarray, operations_list=[]):
        self.operations_list = operations_list
        self.processed_img= img_to_be_processed.copy()

    def __repr__(self) :
        repr_string = "operations queued :\n"
        for element in self.operations_list :
            repr_string += str(self.__read_operation(element).name)+"\n"
        return repr_string

    def add_operation(self, operation) -> None:
        """Appens an operation to PreprocessingManager.operations_list\n
        :operation: PEnum or a list of the following form : [operation:PEnum, arg1, arg2...]"""
        self.operations_list.append(operation)
    
    def remove_operation(self, index=-1) -> None:
        """Removes a preprocessing operation from the operations list \n
        :index: int, index of the operation in PreprocessingManager.operations_list
        to remove
        """
       self.operations_list.pop(index)
    
    def launch_preprocessing(self) -> None:
        """Launches the preprocessing. Operations are removed one-by-one\n
        from PreprocessingManager.operations_list and executed
        """
        for i in range(len(self.operations_list)) :
            element = self.operations_list.pop(i)
            self.__perform_operation(element)

    def __read_operation(self, element) :
        """Extracts the type of operation from an element of PreprocessingManager.operations_list
        :element: PEnum or a list of the following form : [operation:PEnum, arg1, arg2...]
        """
        if type(element)==list :
            operation = element[0]
        else :
            operation = element
        return operation

    def __perform_operation(self, element) :
        """Performs in-place the operation stored in element\n
        :element: PEnum or a list of the following form : [operation:PEnum, arg1, arg2...]

        The following operations can be performed :
            -convert image to grayscale
                Expected element : PEnum.CONVERT2GRAY
            -blurr image
                Expected element : [PEnum.BLURR, kernel_size:Tuple[int, int]]
            -adaptive thresholding :
                Expected element : [PEnum.ADAPTIVE_THRESHOLD, adaptive_method:cv2 constant, block_size:int]
                    See cv2.adaptiveThreshold function for more information
            -edge detection :
                Expected element : [PEnum.EDGE_DETECTION, threshold1:int, threshold2:int, apertureSize:int]
                    See cv2.Canny function for more information
            -morphological opening :
                Expected element : [PEnum.OPEN, kernel_size:Tuple[int, int]]
            -morphological closing :
                Expected element : [PEnum.CLOSE, kernel_size:Tuple[int, int]]
            -skeletonization : 
                Expected element  : PEnum.SKELETONIZE
        """
        operation = self.__read_operation(element)
        if operation == PEnum.CONVERT2GRAY :
            self.processed_img = cv2.cvtColor(self.processed_img, cv2.COLOR_RGB2GRAY)

        elif operation == PEnum.BLURR :
            kernel = element[1]
            self.processed_img = cv2.GaussianBlur(self.processed_img, kernel)
        elif operation == PEnum.ADAPTIVE_THRESHOLD :
            self.processed_img = cv2.adaptiveThreshold(self.processed_img, 255,element[1], element[2],
                                                        element[3],2) 

        elif operation == PEnum.EDGE_DETECTION :
            self.processed_img = cv2.Canny(self.processed_img, element[1], element[2], apertureSize=element[3])

        elif operation == PEnum.OPEN :
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, element[1])
            self.processed_img = cv2.morphologyEx(self.processed_img, cv2.MORPH_OPEN, kernel)

        elif operation==PEnum.CLOSE :
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, element[1])
            self.processed_img = cv2.morphologyEx(self.processed_img, cv2.MORPH_CLOSE, kernel)

        elif operation == PEnum.SKELETONIZE :
            im_skel = np.zeros(self.processed_img.shape, np.uint8)
            element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
            while cv2.countNonZero(self.processed_img) != 0:
                im_open = cv2.morphologyEx(self.processed_img, cv2.MORPH_OPEN, element)
                temp = cv2.subtract(self.processed_img, im_open)
                eroded = cv2.erode(self.processed_img, element)
                im_skel = cv2.bitwise_or(im_skel, temp)
                self.processed_img = eroded.copy()
            self.processed_img = im_skel
        