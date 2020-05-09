import numpy as np

from .key_enum import KeyEnum
from .time_enum import TimeSignatureEnum
from .utils.template_manager import TemplateManager
from .utils.template_matching import pick_template


class Staff:
    def __init__(self, image: np.ndarray, template_manager: TemplateManager):
        self.key = KeyEnum.UNDEFINED
        self.time_signature = TimeSignatureEnum.UNDEFINED
        self.image = image
        self.template_manager = template_manager
        self.measure_list = []

    def identify_measures(self):
        pass

    def identify_clef_time(self):
        if self.key == KeyEnum.UNDEFINED:
            clef = pick_template(self.template_manager.clef, self.image)
            if clef is not None:
                self.key = clef

        if self.time_signature == TimeSignatureEnum.UNDEFINED:
            time = pick_template(self.template_manager.time_signature, self.image)
            if time is not None:
                self.time_signature = time
