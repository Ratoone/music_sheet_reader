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
        return Note(NoteEnum(pitch % 7), pitch // 7, duration)

