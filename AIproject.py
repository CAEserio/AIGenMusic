from midiutil.MidiFile import MIDIFile
import pygame
from music21 import *

import random
midiNotes = {
    'C':61,'C#':62,'D':63,'D#':64,
    'E':65,'F':66,'F#':67,'G':68,
    'G#':69, 'A':70,'A#':71,'B':72
}

notes = ['C','C#','D','D#',
         'E','F','F#','G',
         'G#','A','A#','B',]

keyPattern = [2,2,1,2,2,2,1]



def selectKey():
    selectedKeySig = []
    midiKeySig = []
    print("Please select the key you want the melody to be in:")
    selectedKey = input()
    selectedIndex = notes.index(selectedKey)
    selectedKeySig.append(notes[selectedIndex])

    for i in keyPattern:
        indexToAppend = (selectedIndex + i) % 12
        selectedKeySig.append(notes[indexToAppend])
        selectedIndex = indexToAppend
    
    for note in selectedKeySig:
        midiKeySig.append(midiNotes[note])

    return midiKeySig


def randomMelody(selectedMidiKey):
    mf = MIDIFile(2)     # only 1 track
    track = 0   # the only track

    time = 0    # start at the beginning
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, 180)
    channel = 0
    volume = 100
    selectedMidiKey.append("REST")
    melody = stream.Stream()
   
    mf.addNote(1,channel,selectedMidiKey[0],0,4,volume)
    mf.addNote(1,channel,selectedMidiKey[0 + 3],0,4,volume)
    mf.addNote(1,channel,selectedMidiKey[0 + 3 + 3],0,4,volume)
    for i in range(32):
        noteChoice = random.choice(selectedMidiKey)
        if noteChoice != "REST":
            mf.addNote(track, channel, noteChoice, i, 1, volume)

    for i in range(4,34,4):
        chordChoice = random.randint(1,6)
        mf.addNote(1,channel,selectedMidiKey[chordChoice],i,4,volume)
        mf.addNote(1,channel,selectedMidiKey[(chordChoice+3) %8],i,4,volume)
        mf.addNote(1,channel,selectedMidiKey[(chordChoice+3 +3) %8],i,4,volume)

    with open("outputTEST.mid", 'wb') as outf:
        mf.writeFile(outf)

def melodyRules():
    score = 0

    #Stepwise Motion- Interval Between two consecutive pitch should be no more than a step, limit skips 
    stepwise_count = 0
    for i in range(1, len(melody_stream)):
        if melody_stream[i - 1].isNote and melody_stream[i].isNote:
            interval_between_notes = interval.Interval(melody_stream[i - 1], melody_stream[i])
            if interval_between_notes.generic.undirected == 2:
                stepwise_count += 1
    if stepwise_count > len(melody_stream) / 2:  # Reward for stepwise motion
        score += 1
    #Reference: https://www.youtube.com/watch?v=Z8uYdzU_ZR8&list=PLhiuDs71BWGGBbzE_MlcYHlbUWpgeEZey


    #Repeated Motifs: We check if the melody repeats short patterns of 3 notes. Repeating motifs are given extra points.
    motif_counts = {}
    for i in range(1, len(melody_stream) - 2):
        motif = melody_stream[i:i + 3]
        motif_str = str(motif)
        if motif_str in motif_counts:
            motif_counts[motif_str] += 1
        else:
            motif_counts[motif_str] = 1

    repeated_motif_count = sum(count for count in motif_counts.values() if count > 1)
    score += repeated_motif_count

    


selec = selectKey()
randomMelody(selec)

freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 1024    # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)
pygame.mixer.music.load("outputTEST.mid")
pygame.mixer.music.play()


#Start on I/VII or V
#end on I/VII
#Stepwise is preffered
