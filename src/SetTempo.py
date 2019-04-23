from music21 import converter,instrument,note,chord,stream,tempo
import tensorflow as tf
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D,LSTM,Activation
from keras.models import Sequential
import keras.models
import numpy as np
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
import glob
import pickle

def SetTempo(MIDI,newTempo) :
    #change tempo here
    streamFlat = MIDI.flat
    t = tempo.MetronomeMark('slow', newTempo/2, note.Note(type='half'))
    streamFlat.insert(0,t)

    return streamFlat