import librosa 


# read audio file 
x, sr = librosa.load('test.mp3') 


tempo, beat_times = librosa.beat.beat_track(x, sr=sr, start_bpm=60, units='time')

print(tempo)