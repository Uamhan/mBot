from music21 import converter,instrument,note,chord,stream,pitch,interval
import tensorflow as tf
from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D,LSTM,Activation
from keras.models import Sequential
import keras.models
import numpy as np
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
import glob
import pickle

def TransposeMelody(MIDIStream,desiredKey):
    #gets key of generated peice (krumhansl method)
    key = MIDIStream.analyze('Krumhansl')
    keyInterval = interval.Interval(key.tonic,pitch.Pitch(desiredKey)) 
    MIDIStream = MIDIStream.transpose(keyInterval)

    return MIDIStream