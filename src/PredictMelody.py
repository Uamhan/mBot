from music21 import converter,instrument,note,chord,stream
import tensorflow as tf
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D,LSTM,Activation
from keras.models import Sequential
import keras.models
import numpy as np
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
import glob
import pickle

def Predict(model):
    
    with open('objs.pkl','rb') as f:  
        networkInput, pitchNames, numNotes, nVocab, normalNetworkInput = pickle.load(f)

    #randomly select a start point in our network inputs
    start = np.random.randint(0, len(networkInput)-1)
    #create a dictonary that allows us to convert back from the ltsm output to note names.
    intToNote = dict((number, note) for number, note in enumerate(pitchNames))
    #the prediction pattern at the randomly generated start point.
    pattern = networkInput[start]
    #array that will store the output predictions
    predictionOutput = []
    # generate numNotes notes
    for note_index in range(numNotes):
        #converts the prediction input to a format that can be used with the lstm predict function
        predictionInput = np.reshape(pattern, (1, len(pattern), 1))
        predictionInput = predictionInput / float(nVocab)
        #using this converted input we predict the next note in the sequence.
        prediction = model.predict(predictionInput, verbose=0)
        #this prediciton variable holds the probabilitys of each note to be played next
        #we use the argmax value to get the one with the bigest probability
        index = np.argmax(prediction)
        #we convert the most likely result to a note
        result = intToNote[index]
        #finanly we add this note to the predicition output list
        predictionOutput.append(result)
    
        #we add this note to the end of the list
        pattern.append(index)
        #we remove the first note in the list
        pattern = pattern[1:len(pattern)]
        #this allows us to now make our next prediciton bassed on the last 100 notes (witch now includes our predicted note at the end and our the first note being removed)

    #parseing this output to a midi file.
    #offset represents how far from the start of the midi file the note should be played.
    offset = 0
    offSetRepeat = 0
    #output notes will be the final string of notes with offset values to be converted to midi
    outputNotes=[]
    #sets note and chord objects based on models predicitions
    for pattern in predictionOutput:
        #if statement checking weather the next value in prediciton output is a chord.
        #if so we seperate the chord into an array of notes
        #create a new note object for these notes
        #assign default iinstrument as piano
        #then we create a chord object from these notes and assign the current offset.
        #finaly we appened the the outputnotes list.
        if('.' in pattern) or pattern.isdigit():
            notesInChord = pattern.split('.')
            cNotes = []
            for currentNote in notesInChord:
                newNote = note.Note(int(currentNote))
                newNote.storedInstrument = instrument.Piano()
                cNotes.append(newNote)
            newChord = chord.Chord(cNotes)
            newChord.offset=offset
            outputNotes.append(newChord)
        #if note a chord its simply a single note in this case we create a new note object assign the current offset assign default instrument and append to the output notes
        else:
                newNote = note.Note(pattern)
                newNote.offset = offset
                newNote.storedInstrument = instrument.Piano()
                outputNotes.append(newNote)
        #we increase the offset after each generated note has been added
        #if statement that generates 1 bar or four beat rythms
         
        #adds offset amount to total ofset of generated peice and reduces the offset repeat amount by 1
        offset += 0.5
   
        #create a stream from our output notes
        #write the output stream to the file OUTPUT.mid
    MIDIStream = stream.Stream(outputNotes)
    return MIDIStream