from .note_enum import NoteEnum


class Note:
    def __init__(self, *args):
        if (len(args)> 0) :
            self.name = args[0]
            self.octave= args[1]
            self.duration = args[2]
        else :
            self.name = NoteEnum.UNDEFINED
            self.octave = 0
            self.duration = 0

