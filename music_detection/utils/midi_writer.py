from music_detection.staff import Staff
from music_detection.note import Note
from music_detection.time_enum import TimeSignatureEnum
from music_detection.note_enum import NoteEnum

import midiutil as mu
import math


class MIDIWriter :
    def __init__(self, num_tracks=0) :
        self.num_tracks = 0
        self.track_list = list()
        for i in range(num_tracks) :
            self.addTrack()

    def addStaff(self, track_id:int, staff:Staff) :
        """add Staff object to a specific track. \n
        inputs :
            -track_id : int, index of the track in MIDIWriter.track_list
            -staff : Staff object to be added
        """
        self.track_list[track_id].staff_list.append(staff)

    def writeToFile(self, file_name:str) :
        """Writes the tracks in a MIDIFile and saves it. \n
        input : 
            -file_name : string, name of the generated MIDI file (with .mdi extension).
                        Can be a path as well.
        """

        file = mu.MIDIFile(self.num_tracks)
        for track_id,track in enumerate(self.track_list) :
            time = track.start_time
            for staff in track.staff_list :
                file.addTempo(track_id,time,staff.tempo)
                numerator, denominator, clocks_amount = self.__get_time_signature_values(staff.time_signature)
                file.addTimeSignature(track_id, time,numerator,int(math.log(denominator, 2)),clocks_amount)
                for measure in staff.measure_list :
                    for note in measure.note_list :
                        if note.name != NoteEnum.REST:
                            file.addNote(track_id, 0, self.__pitch_convert(note), time, note.duration, 127)
                        time+= note.duration

        with open(file_name,"wb") as output_file :
            file.writeFile(output_file)
        output_file.close()
    
    def addTrack(self,start_time=0, staff_list = []):
        """Creates and adds a new Track object to MIDIWriter.track_list. \n
        inputs :
            -start-time : time of the first note on of the track
            -staff_list : list, contains Staff objects to be added in the track
        """
        self.track_list.append(Track(start_time,staff_list))
        self.num_tracks +=1
        
    
    
    def __pitch_convert(self, note : Note) -> int :
        """Converts a note's name and octave into MIDI pitch value \n
        input :
            -note : Note object to extract the information from
        output :
            -MIDIValue : integer,corresponding pitch value for MIDI 
        """
        name = note.name
        octave = note.octave
        note_offset = 0
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

        if note.accidental is not None:
            note_offset += note.accidental.value
        
        MIDIValue = (octave+1)*12+note_offset
        return MIDIValue

    def __get_time_signature_values(self, time_signature : TimeSignatureEnum) -> int :
        """Extract necessary values for note encoding in MIDI format \n
        input:
            -time_signature : TimeSignatureEnum object
        outputs:
            -numerator : first integer of the time signature
            -denominator : second integer of the time signature
            -clocks_amount : integer, corresponding clocks per tick value of the time signature
        """
        if time_signature == TimeSignatureEnum.UNDEFINED :
            raise ValueError("Staff has no time signature")
        numerator = time_signature.value[0]
        denominator = time_signature.value[1]
        
        clocks_amount = int(24*numerator*4/denominator)
        return numerator, denominator, clocks_amount


class Track :
    def __init__(self, start_time=0, staff_list=[]) :
        self.start_time = 0
        self.staff_list = staff_list