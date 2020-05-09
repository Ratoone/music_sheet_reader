import glob
import os

from music_detection.key_enum import KeyEnum
from music_detection.time_enum import TimeSignatureEnum
from music_detection.utils.template import Template


class TemplateManager:
    def __init__(self, path):
        self.path = path
        self.clef = []
        self.time_signature = []
        self.__build_clef_template()
        self.__build_time_template()

    def __build_clef_template(self):
        for clef in glob.glob(os.path.join(self.path, "clef/*")):
            if "bass" in clef:
                clef_type = KeyEnum.FA
            else:
                if "treble" in clef:
                    clef_type = KeyEnum.SOL
                else:
                    clef_type = KeyEnum.DO
            self.clef.append(Template(clef, clef_type))

    def __build_time_template(self):
        for time in glob.glob(os.path.join(self.path, "time/*")):
            name = os.path.splitext(os.path.basename(time))[0]
            if name == "common":
                time_type = TimeSignatureEnum.COMMON
            else:
                time_type = TimeSignatureEnum((int(name[0]), int(name[1])))
            self.time_signature.append(Template(time, time_type))