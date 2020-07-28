from .accidentals_enum import AccidentalsEnum
from .note_enum import NoteEnum


class Note:
    def __init__(self, name=NoteEnum.UNDEFINED, octave: int = 0, duration: float = 0):
        self.name = name
        self.octave = octave
        self.duration = duration
        self.accidental = None

    @staticmethod
    def from_pitch_duration(pitch: int, duration: float):
        """
        Build a note according to the pitch and duration
        :param pitch: pitch measures in notes, e.h. La4 = 7*4+5
        :param duration: the length of the note in number of beats - 1 is a quarter note
        """
        if pitch % 7 == 0:
            name = NoteEnum.DO
        elif pitch % 7 == 1:
            name = NoteEnum.RE
        elif pitch % 7 == 2:
            name = NoteEnum.MI
        elif pitch % 7 == 3:
            name = NoteEnum.FA
        elif pitch % 7 == 4:
            name = NoteEnum.SOL
        elif pitch % 7 == 5:
            name = NoteEnum.LA
        else:
            name = NoteEnum.SI

        return Note(name, pitch // 7, duration)

    def update_scale(self, scale: int) -> None:
        """
        Updates the accidental wrt the scale
        :param scale: integer representing the scale, equal to the number of sharps (positive) or flats (negative)
        """
        if self.accidental == AccidentalsEnum.NATURAL or scale == 0:
            return

        if scale > 0:
            if self.name.value < scale:
                self.accidental = AccidentalsEnum.SHARP
        if scale < 0:
            if self.name.value > 6 + scale:
                self.accidental = AccidentalsEnum.FLAT
