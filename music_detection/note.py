from .note_enum import NoteEnum


class Note:
    def __init__(self, pitch: int, duration: float):
        """
        Build a note according to the pitch and duration
        :param pitch: pitch measures in notes, e.h. La4 = 7*4+5
        :param duration: the length of the note - 1 is a full note, while 0.25 is a quarter note
        """
        self.name = NoteEnum(pitch % 7)
        self.octave = pitch // 7
        self.duration = duration

