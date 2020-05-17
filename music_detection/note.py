from .note_enum import NoteEnum


class Note:
    def __init__(self):
        self.name = NoteEnum.UNDEFINED
        self.octave = 0
        self.duration = 0

