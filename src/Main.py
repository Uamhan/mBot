from Imports import *

import LoadModel
import PredictMelody
import Transpose
import SetTempo
import TrainModel

#load model
model = LoadModel.createModel()
#train model if none found
try:
    model.load_weights('Clasical.hdf5')
except:
    #train model
    model = TrainModel.Train()
    
#predict melody
MIDI = PredictMelody.Predict(model)
#transpose melody
TMIDI = Transpose.TransposeMelody(MIDI)
#set melody tempo
FMIDI = SetTempo.SetTempo(TMIDI)
#output mellody as midi file
FMIDI.write('midi',fp='OUTPUT.mid')