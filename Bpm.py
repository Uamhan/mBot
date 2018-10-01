#!/usr/bin/python
import librosa 

#takes path of audio file and returns Bpm of audio
def getBpm(path):
    x, sr = librosa.load(path) 
    tempo, _ = librosa.beat.beat_track(x, sr=sr, start_bpm=60, units='time')
    return tempo
