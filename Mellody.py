from music21 import converter,instrument,note,chord
import tensorflow as tf
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D,LSTM,Activation
from keras.models import Sequential
import keras.models
import numpy as np
from keras.utils import np_utils
from MellodyTrain import getModelDetails

nVocab,modelS1,modelS2,pitchNames=getModelDetails()
model = Sequential()
model.add(LSTM(
    512,
    input_shape=(modelS1, modelS2),
    return_sequences=True
))
model.add(Dropout(0.3))
model.add(LSTM(512, return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(512))
model.add(Dense(256))
model.add(Dropout(0.3))
model.add(Dense(nVocab))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
# Load the weights to each node
model.load_weights('weights.hdf5')



