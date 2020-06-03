from enum import Enum

class PreprocessingOperationEnum (Enum) :
    CONVERT2GRAY=0
    BLURR = 1
    ADAPTIVE_THRESHOLD=2
    EDGE_DETECTION=3
    OPEN=4
    CLOSE=5
    SKELETONIZE=6
