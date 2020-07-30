import numpy as np 
import midiutil as mu
import sys, os 

sys.path.insert(0,os.getcwd())

from music_detection.utils.midi_writer import *
from music_detection.measure import Measure
from music_detection.staff import Staff
from music_detection.note import Note
from music_detection.note_enum import NoteEnum
from music_detection.time_enum import TimeSignatureEnum

##testset creation
twinkle_staffs = [Staff(None, 0) for i in range(3)]
octave_number = 4
notes_twinkle = [[NoteEnum.DO, NoteEnum.DO, NoteEnum.SOL, NoteEnum.SOL, NoteEnum.LA, NoteEnum.LA, NoteEnum.SOL, NoteEnum.FA, NoteEnum.FA,
        NoteEnum.MI, NoteEnum.MI, NoteEnum.RE, NoteEnum.RE, NoteEnum.DO],[ NoteEnum.SOL, NoteEnum.SOL, NoteEnum.FA, NoteEnum.FA,
        NoteEnum.MI, NoteEnum.MI, NoteEnum.RE,NoteEnum.SOL, NoteEnum.SOL, NoteEnum.FA, NoteEnum.FA,NoteEnum.MI, NoteEnum.MI, NoteEnum.RE],
        [NoteEnum.DO, NoteEnum.DO, NoteEnum.SOL, NoteEnum.SOL, NoteEnum.LA, NoteEnum.LA, NoteEnum.SOL, NoteEnum.FA, NoteEnum.FA,
        NoteEnum.MI, NoteEnum.MI, NoteEnum.RE, NoteEnum.RE, NoteEnum.DO]]
durations_twinkle = [[1,1,1,1,1,1,2,1,1,1,1,1,1,2],[1,1,1,1,1,1,2,1,1,1,1,1,1,2],[1,1,1,1,1,1,2,1,1,1,1,1,1,2]]

for k,staff in enumerate(twinkle_staffs) :
    staff.time_signature = TimeSignatureEnum.COMMON
    bar_length= 0
    new_measure = Measure()
    notes =notes_twinkle[k]
    duration = durations_twinkle[k]
    for i,note in enumerate(notes) : 
        new_note = Note(note, octave_number, duration[i])
        new_measure.note_list.append(new_note)
        bar_length += duration[i]
        if bar_length==4 :
            bar_length = 0
            staff.measure_list.append(new_measure)
            new_measure = Measure()

#MidiWriter Object creation end initialization
mw = MIDIWriter(1)
for staff in twinkle_staffs :
    mw.addStaff(0,staff)

#Writing to file
mw.writeToFile("result_twinkle.mid")



