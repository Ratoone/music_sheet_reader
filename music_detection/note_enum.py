from enum import Enum


class NoteEnum(Enum):
    """
    The types of notes. For the positive ones, the number signifies the order of scale
    - FA, DO, SOL, RE, LA, Mi, Si
    """
    REST = -2
    UNDEFINED = -1
    DO = 1
    RE = 3
    MI = 5
    FA = 0
    SOL = 2
    LA = 4
    SI = 6

