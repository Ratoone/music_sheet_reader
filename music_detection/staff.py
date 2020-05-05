from .key_enum import KeyEnum


class Staff:
    def __init__(self):
        self.key = KeyEnum.UNDEFINED
        self.time_signature = 0
        self.position_in_image = []
        self.measure_list = []

    def identify_measures(self):
        pass

