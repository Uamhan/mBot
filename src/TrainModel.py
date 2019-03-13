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
import LoadModel

def Train():
    #array storeing each note
    notes = []
    #number of notes to be generated
    numNotes = 250

    #Read in and covert midi files into useable format.
    for file in glob.glob("../Classical/*/*.mid"):
        #using music21 coverter we parse midi files into the variable midi
        midi = converter.parse(file)
        print("Parsing %s" % file)
        notesToParse = None
        parts = instrument.partitionByInstrument(midi)
        if parts: # file has more than one instrument we seperate them and add to notes to parse
            notesToParse = parts.parts[0].recurse()
        else: # single instrument adds notes to notes to parse
            notesToParse = midi.flat.notes
        #we convert each note to its given pitch value and add it to our list of notes.
        #for chords we join the the notes to gether with a . before adding to the notes list.
        for e in notesToParse:
            if isinstance(e, note.Note):
                notes.append(str(e.pitch))
            elif isinstance(e, chord.Chord):
                notes.append('.'.join(str(n) for n in e.normalOrder))
    
    #sequence length ie the amount of previous notes the lstm checks to predict the next note
    sLength = 100
    #gets a difinitive list of the difrent pitches present in our training data.
    pitchNames = sorted(set(item for item in notes))
    #number of difrent notes.
    nVocab= len(set(notes))

    #we use a dictonary to map the difrent notes to ints. as the lstm needs to process the data as numbers rather than string representations of notes.
    #we will convert back when creating the midi file.
    noteToInt = dict((note,number)for number,note in enumerate(pitchNames))
    #input for our lstm network.
    networkInput = []
    #output for our lstm network.
    networkOutput = []

    #fills out network input from notes with our sequence length number of notes from notes.
    for i in range(0,len(notes)-sLength,1):
        sIn = notes[i:i + sLength]
        sOut = notes[i +sLength]
        networkInput.append([noteToInt[char] for char in sIn])
        networkOutput.append(noteToInt[sOut])

    #length of our networkInput
    nPatterns = len(networkInput)

    #reshape the input into a format compatibal for lstm training.
    normalNetworkInput = np.reshape(networkInput,(nPatterns,sLength,1))
    normalNetworkInput = normalNetworkInput / float(nVocab)
    #converts our output so that it can accept out compile loss function categorical_crossentropy
    networkOutput = np_utils.to_categorical(networkOutput)

    #saves varibles needed for prediction to file
    with open('objs.pkl', 'wb') as f:
        pickle.dump([networkInput, pitchNames, numNotes, nVocab, normalNetworkInput], f)

    model = LoadModel.createModel()

    #creats checkpoints while training the model to prevent lost weights if training dose note complete in full.
    filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"    
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=0,save_best_only=False,mode='min')    
    callbacks_list = [checkpoint]
    model.fit(normalNetworkInput, networkOutput, epochs=100, batch_size=64, callbacks=callbacks_list)
    return model