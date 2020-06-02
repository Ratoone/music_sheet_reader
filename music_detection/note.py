from .note_enum import NoteEnum


class Note:
    def __init__(self, name = NoteEnum.UNDEFINED, octave=0, duration=0):
        self.name = name 
        self.octave = octave 
        self.duration = duration

