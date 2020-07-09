import glob
import os

from music_detection.key_enum import KeyEnum
from music_detection.time_enum import TimeSignatureEnum
from music_detection.utils.template import Template


class TemplateManager:
    """
    Holds the image templates for all the templates used in template matching.
    """
    def __init__(self, path):
        self.path = path
        self.clef = []
        self.time_signature = []
        self.__build_clef_template()
        self.__build_time_template()
        self.rests = []
        self.accidentals = []
        self.__rests_template()
        self.__accidentals_template()


    def __build_clef_template(self):
        """
        Create the template vector for the keys / clefs. It is expected that the template
        names start with bass, treble, or alto.
        """
        for clef in glob.glob(os.path.join(self.path, "clef/*")):
            if "bass" in clef:
                clef_type = KeyEnum.FA
            else:
                if "treble" in clef:
                    clef_type = KeyEnum.SOL
                else:
                    clef_type = KeyEnum.DO
            self.clef.append(Template(clef, clef_type))

    def __build_time_template(self) -> None:
        """
        Create the template vector for time signatures. The enum is built by forming a tuple
        with the first 2 characters in the template name.
        """
        for time in glob.glob(os.path.join(self.path, "time/*")):
            name = os.path.splitext(os.path.basename(time))[0]
            if name == "common":
                time_type = TimeSignatureEnum.COMMON
            else:
                time_type = TimeSignatureEnum((int(name[0]), int(name[1])))
            self.time_signature.append(Template(time, time_type))

    def __build_rests_template(self):
        for rests in glob.glob(os.path.join(self.path, "rests/*")):
            if "half_rest_1" in rests:
                rests_type = RestsEnum.HF
            else:
                if "whole_rest" in rests:
                    rests_type = RestsEnum.WR
                else:
                    if "quarter_rest" in rests:
                        rests_type = RestsEnum.QR
                    else:
                        rests_type = RestsEnum.ER
            self.clef.append(Template(rests, rests_type))

    def __build_accidentals_template(self):
        for accidentals in glob.glob(os.path.join(self.path, "accidentals/*")):
            if "flat-line" in accidentals:
                accidentals_type = AccidentalsEnum.FL
            else:
                if "flat-space" in accidentals:
                    accidentals_type = AccidentalsEn.FS
                else:
                    if "sharp-line" in accidentals:
                        accidentals_type = AccidentalsEnum.SL
                    else:
                        accidentals_type = AccidentalsEnum.SS
            self.clef.append(Template(rests, rests_type))