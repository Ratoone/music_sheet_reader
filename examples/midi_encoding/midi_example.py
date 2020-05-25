import numpy as np 
import midiutil as mu
import sys, os 

sys.path.insert(0,os.getcwd())

from music_detection.utils.midi_functions import *
from music_detection.measure import Measure
from music_detection.staff import Staff
from music_detection.note import Note
from music_detection.note_enum import NoteEnum
from music_detection.time_enum import TimeSignatureEnum

##Test Staff creation
twinkle_staff = Staff(None, None)
octave_number = 4
notes = [NoteEnum.DO, NoteEnum.DO, NoteEnum.SOL, NoteEnum.SOL, NoteEnum.LA, NoteEnum.LA, NoteEnum.SOL, NoteEnum.FA, NoteEnum.FA,
        NoteEnum.MI, NoteEnum.MI, NoteEnum.RE, NoteEnum.RE, NoteEnum.DO]
duration = [1,1,1,1,1,1,2,1,1,1,1,1,1,2]

twinkle_staff.time_signature = TimeSignatureEnum.COMMON
bar_length= 0
new_measure = Measure()
for i,note in enumerate(notes) : 
    new_note = Note(note, octave_number, duration[i])
    new_measure.note_list.append(new_note)
    bar_length += duration[i]
    if bar_length==4 :
        bar_length = 0
        twinkle_staff.measure_list.append(new_measure)
        new_measure = Measure()

#Converts twinkle_staff to MIDI format
write_MIDI_file(twinkle_staff, "examples\\midi_encoding\\result.mid")
