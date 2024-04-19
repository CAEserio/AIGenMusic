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
    generatedMelody = []
    selectedMidiKey.append("REST")
    melody = stream.Stream()
   
    
    #isItFit = melodyRules(melody)
    #Returns True or False

    for i in range(32):
        noteChoice = random.choice(selectedMidiKey)
        if noteChoice != "REST":
            #mf.addNote(track, channel, noteChoice, i, 1, volume)
            generatedMelody.append(noteChoice)
        else:
            generatedMelody.append("REST")
    
    return generatedMelody

def mutate(generatedMelody,selectedMidiKey):
    mutationRate = 10
    for i in range(len(generatedMelody)):
        mutation = random.randint(0,10)
        if (mutation == mutationRate):
            generatedMelody[i] = random.choice(selectedMidiKey)
    
def printToScore(melody,selectedMidiKey,num):
    mf = MIDIFile(2)     # only 1 track
    track = 0   # the only track

    time = 0    # start at the beginning
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, 180)
    channel = 0
    volume = 100

    mf.addNote(1,channel,selectedMidiKey[0],0,4,volume)
    mf.addNote(1,channel,selectedMidiKey[0 + 3],0,4,volume)
    mf.addNote(1,channel,selectedMidiKey[0 + 3 + 3],0,4,volume)
    for i in range(len(melody)):
        if (melody[i] != "REST"):
            mf.addNote(track,channel,melody[i],i,1,volume)
    
    for i in range(4,34,4):
        chordChoice = random.randint(1,6)
        mf.addNote(1,channel,selectedMidiKey[chordChoice],i,4,volume)
        mf.addNote(1,channel,selectedMidiKey[(chordChoice+3) %8],i,4,volume)
        mf.addNote(1,channel,selectedMidiKey[(chordChoice+3 +3) %8],i,4,volume)

    with open("outputTEST"+str(num)+".mid", 'wb') as outf:
        mf.writeFile(outf)
            
def melodyRules(melody,notes):
    score = 0

    #Tonic - First and Last Notes of the Scale. Melody revolves around the proper use of the tonic
    #Correct Finish to the Tonic
    for i in range(1, len(melody)):
     if melody[i - 1] == notes[-2] and melody[i] == notes[0]:
        score += 1

    #Stepwise Motion- Interval Between two consecutive pitch should be no more than a step
    for i in range(1, len(melody)):
        interval = abs(get_note_index(melody[i]) - get_note_index(melody[i - 1]))
        if interval == 1:
            score += 1

    #Melodic Contour: Checks if there are large jumps betwen notes. Large Jumps are penalized
    for i in range(1, len(melody)):
        interval = abs(get_note_index(melody[i]) - get_note_index(melody[i - 1]))
        if interval > 4 and interval != 1:
            score -= 2  


    #Repeated Motifs: We check if the melody repeats short patterns of 3 notes. Repeating motifs are awarded
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

    if score > 10:
        return true
    else:
        return false



selec = selectKey()

melody = randomMelody(selec)
#print(melody)
#mutate(melody,selec)
#print(melody)
printToScore(melody,selec,1)
clock = pygame.time.Clock()
melody2 = randomMelody(selec)
printToScore(melody2,selec,2)

melody3 = randomMelody(selec)
printToScore(melody3,selec,3)

melody4 = randomMelody(selec)
printToScore(melody4,selec,4)

melody5 = randomMelody(selec)
printToScore(melody5,selec,5)

freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 1024    # number of samples

pygame.mixer.init(freq, bitsize, channels, buffer)
pygame.mixer.music.load("outputTEST1.mid")
pygame.mixer.music.play()
print("playing melody1")

while pygame.mixer.music.get_busy():
    clock.tick(30)

pygame.mixer.music.load("outputTEST2.mid")
pygame.mixer.music.play()
print("playing melody2")

while pygame.mixer.music.get_busy():
    clock.tick(30)

pygame.mixer.music.load("outputTEST3.mid")
pygame.mixer.music.play()
print("playing melody3")

while pygame.mixer.music.get_busy():
    clock.tick(30)

pygame.mixer.music.load("outputTEST4.mid")
pygame.mixer.music.play()
print("playing melody4")

while pygame.mixer.music.get_busy():
    clock.tick(30)

pygame.mixer.music.load("outputTEST5.mid")
pygame.mixer.music.play()
print("playing melody5")

while pygame.mixer.music.get_busy():
    clock.tick(30)
#Start on I/VII or V
#end on I/VII
#Stepwise is preffered
