from enum import Enum


class RestsEnum(Enum):
    """
    Enum containing the possible rests. The values represent the duration
    """
    UNDEFINED = 0
    HALF = 2
    WHOLE = 4
    QUARTER = 1
    EIGHTH = 0.5
