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

import pygame.midi
import base64

#playws
def play_song(music_file):
    
    timer = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
    except pygame.error:
        print ("File not found")
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        timer.tick(30)


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
desiredKey= 'a'
TMIDI = Transpose.TransposeMelody(MIDI,desiredKey)
#set melody tempo
#
newTempo = 120
FMIDI = SetTempo.SetTempo(TMIDI,newTempo)
#output mellody as midi file
FMIDI.write('midi',fp='OUTPUT.mid')

#songfile to be played.
Song_file = "OUTPUT.mid"
#midi mixer settings.

buffer = 1024    # number of samples
bitsize = -16   # unsigned 16 bit
freq = 44100    # CD quality audio
mono_stereo = 2    # 1 is mono, 2 is stereo
#initilises midi mixer using the arguments above.
pygame.mixer.init(freq, bitsize, mono_stereo, buffer)

play_song(Song_file)
