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
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import os

import LoadModel
import PredictMelody
import Transpose
import SetTempo
import TrainModel

import pygame.midi
import base64

#playbutton method
def play():

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

def getKey():
    
    #getts user values from combo boxes
    key = keycombo.get()
    mm = mmcombo.get()
    fs = fscombo.get()
    #sets the key value based on the user input.
    #major keys denoted by upercase and minor by lower case
    #sharp keys followed by #
    #flat keys followed by b
    if(mm == "Major"):
        key.upper()
    if(mm == "Minor"):
        key.lower()
    if(fs == "Flat"):
        key=key+"b"
    if(fs == "Sharp"):
        key=key+"#"

    return key

def generate():
    dislbl.configure(text="Generating new song this may take a minute.")
    window.update()
    #predict melody
    MIDI = PredictMelody.Predict(model)
    #transpose melody
    desiredKey= getKey()
    TMIDI = Transpose.TransposeMelody(MIDI,desiredKey)
    #set melody tempo
    newTempo = int(tempocombo.get())
    FMIDI = SetTempo.SetTempo(TMIDI,newTempo)
    #output mellody as midi file
    FMIDI.write('midi',fp='OUTPUT.mid')
    dislbl.configure(text="Generating complete hit play to listen or save to save midi file.")
    window.update()

def save():

    s = converter.parse('OUTPUT.mid')
    savelocation =  filedialog.asksaveasfilename(initialdir = "/",title = "Save file",filetypes = (("midi files","*.mid"),("all files","*.*")))
    dislbl.configure(text="File Saved.")
    s.write('midi', savelocation+".mid")
    
    

#plays song
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


#initilises gui window
window = Tk()
window.title("mBot NeuralNet Music Generator")

# gui labels
headerlbl = Label(window,text="Mbot Music Generator",font=("Arial Bold",32))
tempolbl = Label(window,text="Select song Tempo",font=("Arial",12))
keylbl = Label(window,text="Select song key",font=("Arial",12))
mmlbl = Label(window,text="Select song tonality",font=("Arial",12))
fslbl = Label(window,text="Select song's key Acidental",font=("Arial",12))
dislbl = Label(window,text="Select values above and click generate",font=("Arial Bold",12))


#combo boxes
#tempo combobox
tempocombo = Combobox(window)
tempocombo["values"]=(10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200)
tempocombo.current(11)
#key comboBox
keycombo = Combobox(window)
keycombo["values"]=("A","B","C","D","E","F","G")
keycombo.current(2)
#MajorMinor combobox
mmcombo = Combobox(window)
mmcombo["values"]=("Major","Minor")
mmcombo.current(0)
#flatsharp combobox
fscombo = Combobox(window)
fscombo["values"]=("Flat","Sharp","Neutral")
fscombo.current(2)

#buttons
generatebtn = Button(window, text="Generate", command=generate)
savebtn = Button(window, text="Save", command=save)
playbtn = Button(window, text="Play", command=play)


#placements of gui elements
#combobox placements
tempocombo.grid(column=1,row=1)
keycombo.grid(column=1,row=2)
mmcombo.grid(column=1,row=3)
fscombo.grid(column=1,row=4)
#lable placements.
headerlbl.grid(column=0,row=0,columnspan=3)
tempolbl.grid(column=0,row=1,sticky="w")
keylbl.grid(column=0,row=2,sticky="w")
mmlbl.grid(column=0,row=3,sticky="w")
fslbl.grid(column=0,row=4,sticky="w")
dislbl.grid(column=0,row=5,sticky="w",pady=15)
#button placements
generatebtn.grid(column=0, row=6)
savebtn.grid(column=1, row=6)
playbtn.grid(column=2, row=6)

#window settings
window.columnconfigure(0,minsize=200)
window.columnconfigure(1,minsize=200)
window.columnconfigure(2,minsize=200)
window.rowconfigure(0,pad = 10)
window.rowconfigure(1,pad = 10)
window.rowconfigure(2,pad = 10)
window.rowconfigure(3,pad = 10)
window.rowconfigure(4,pad = 10)
window.rowconfigure(5,pad = 10)
window.rowconfigure(6,pad = 10)
window.geometry("900x400")




#load model
#train model if none found
try:
    model = LoadModel.createModel()
    model.load_weights('ClassicalWeights.hdf5')
except:
    #train model
    model = TrainModel.Train()

#initilise window loop
window.mainloop()

