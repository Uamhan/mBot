from music21 import converter,instrument,note,chord,stream
import tensorflow as tf
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D,LSTM,Activation
from keras.models import Sequential
import keras.models
import numpy as np
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
import glob


#array storeing each note
notes = []
#number of notes to be generated
numNotes = 250

#Read in and covert midi files into useable format.
for file in glob.glob("Classical/*/*.mid"):
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

#creates out model
#each add fucntion adds a layer to our machine learning model.
#creates a sequential model
model = Sequential()
#adds LSTM layer with 256 nodes and a shame matching our normalised input
model.add(LSTM(256,input_shape=(normalNetworkInput.shape[1], normalNetworkInput.shape[2]),return_sequences=True))
#drop out randomly sets a draction rate of input units to 0 during training time with helps to prevent overfitting.
model.add(Dropout(0.3))
#adds another lstm layer with 512 nodes.
model.add(LSTM(512, return_sequences=True))
#dropout layer
model.add(Dropout(0.3))
#256 nodes lstm
model.add(LSTM(256))
#adds a standard densely connected NN layer with 256 nodes dense meaning each node recives input from all of the nodes in the previous layer.
model.add(Dense(256))
#dropout layer
model.add(Dropout(0.3))
#final dense layer with nVocab number of nodes so that we have 1 node per possible note value.
model.add(Dense(nVocab))
#adds a softmax activation to the previous dense layer.
model.add(Activation('softmax'))
#compiles out created model using the categorical_crossentropy loss function and the rmsprop optimiser.
model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

#creats checkpoints while training the model to prevent lost weights if training dose note complete in full.
filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"    
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=0,save_best_only=False,mode='min')    
callbacks_list = [checkpoint]     

#model.load_weights('blues1.hdf5')
#trains the network with 100 itterations
model.fit(normalNetworkInput, networkOutput, epochs=100, batch_size=64, callbacks=callbacks_list)



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
        isRestSelector = np.random.randint(0,8,1)
        if(isRestSelector==1):
            newNote = note.Rest()
            newNote.duration = offSetAmount
        else:
            newNote = note.Note(pattern)
            newNote.offset = offset
            newNote.storedInstrument = instrument.Piano()
            outputNotes.append(newNote)
    #we increase the offset after each generated note has been added
    #if statement that generates 1 bar or four beat rythms
    if(offSetRepeat == 0):
        offSetSelector = np.random.randint(0, 8, 1)
        if(offSetSelector == 0):
            offSetAmount = 1
            offSetRepeat = 4
        elif(offSetSelector == 1):
            offSetAmount = 0.25
            offSetRepeat = 16
        elif(offSetSelector == 2):
            offSetAmount = 2
            offSetRepeat = 2
        elif(offSetSelector == 3):
            offSetAmount = 4
            offSetRepeat = 1
        else : 
            offSetAmount = 0.5
            offSetRepeat = 8   
    #adds offset amount to total ofset of generated peice and reduces the offset repeat amount by 1
    offset += offSetAmount
    offSetRepeat -= 1
   
    #create a stream from our output notes
    #write the output stream to the file OUTPUT.mid
MIDIStream = stream.Stream(outputNotes)
MIDIStream.write('midi',fp='OUTPUT.mid')