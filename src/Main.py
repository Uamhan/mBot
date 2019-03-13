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
import PredictMelody
import Transpose
import SetTempo
import TrainModel

#load model
#train model if none found
try:
    model = LoadModel.createModel()
    model.load_weights('ClassicalWeights.hdf5')
except:
    #train model
    model = TrainModel.Train()
    
#predict melody
MIDI = PredictMelody.Predict(model)
#transpose melody
desiredKey= 'F'
TMIDI = Transpose.TransposeMelody(MIDI,desiredKey)
#set melody tempo
FMIDI = SetTempo.SetTempo(TMIDI)
#output mellody as midi file
FMIDI.write('midi',fp='OUTPUT.mid')