from music_detection.staff import Staff
from music_detection.note import Note
from music_detection.time_enum import TimeSignatureEnum
from music_detection.note_enum import NoteEnum

import midiutil as mu

def get_time_signature_values(staff : Staff) -> int :
    """Extract necessary values for note encoding in MIDI format \n
    input:
        -staff : Staff object
    outputs:
        -numerator : first integer of the time signature
        -denominator : second integer of the time signature
        -clocks_amount : integer, corresponding clocks per tick value of the time signature
    """
    if staff.time_signature == TimeSignatureEnum.UNDEFINED :
        raise ValueError("Staff has no time signature")
    numerator = staff.time_signature.value[0]
    denominator = staff.time_signature.value[1]
    
    clocks_amount = int(24*numerator*4/denominator)
    return numerator, denominator, clocks_amount

def pitch_convert(note : Note) -> int :
    """Converts a note's name and octave into MIDI pitch value \n
    input :
        -note : Note object to extract the information from
    output :
        -MIDIValue : integer,corresponding pitch value for MIDI 
    """
    name = note.name
    octave = note.octave
    if name == NoteEnum.UNDEFINED :
        raise ValueError("Note name is undefined")
    elif name== NoteEnum.DO :
        note_offset = 0
    elif name==NoteEnum.RE :
        note_offset = 2
    elif name==NoteEnum.MI :
        note_offset = 4
    elif name==NoteEnum.FA :
        note_offset = 5
    elif name==NoteEnum.SOL :
        note_offset = 7
    elif name==NoteEnum.LA :
        note_offset = 9
    elif name==NoteEnum.SI :
        note_offset = 11
    
    MIDIValue = (octave+1)*12+note_offset
    return MIDIValue

#TODO : MAYBE change the following function so that instead of a unique Staff object it takes
#        a list of them as input
def write_MIDI_file(staff:Staff, path:str):
    """Converts Staff object into MIDI file and saves it \n
    inputs :
        -staff : Staff object to convert
        -path : path of the resulting MIDI file (e.g. examples\\result.mdi) 
    """
    #MIDI file creation and configuration
    songFile = mu.MIDIFile(1)

    songFile.addTempo(0,0,staff.tempo)
    numerator, denominator, clocks_amount = get_time_signature_values(staff)
    songFile.addTimeSignature(0,0,numerator,denominator, clocks_amount)

    #Note writing process
    time=0
    for measure in staff.measure_list :
        for note in measure.note_list :
            songFile.addNote(0,0,pitch_convert(note), time, note.duration, 127)
            time +=note.duration

    #File is then saved
    with open(path, "wb") as output_file:
        songFile.writeFile(output_file)