from enum import Enum


class TimeSignatureEnum(Enum):
    UNDEFINED = (0, 1)
    COMMON = (4, 4)
    TWO_QUARTERS = (2, 4)
    THREE_QUARTERS = (3, 4)
    SIX_EIGHTHS = (6, 8)

    @staticmethod
    def get_length(time: Enum) -> float:
        return time.value[0] / time.value[1]
