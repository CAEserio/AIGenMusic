from midiutil.MidiFile import MIDIFile
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
    mf = MIDIFile(1)     # only 1 track
    track = 0   # the only track

    time = 0    # start at the beginning
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, 180)
    channel = 0
    volume = 100
    selectedMidiKey.append("REST")
   

    for i in range(32):
        noteChoice = random.choice(selectedMidiKey)
        if noteChoice != "REST":
            mf.addNote(track, channel, noteChoice, i, 1, volume)
    
    with open("outputTEST.mid", 'wb') as outf:
        mf.writeFile(outf)

selec = selectKey()
randomMelody(selec)

#Start on I/VII or V
#end on I/VII
#Stepwise is preffered
