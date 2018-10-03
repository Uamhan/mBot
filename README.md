# mBot
## Relevent Links
### http://colah.github.io/posts/2015-08-Understanding-LSTMs/
### http://karpathy.github.io/2015/05/21/rnn-effectiveness/
## TODO
### - Find suitiable midi dataset.
#### https://colinraffel.com/projects/lmd/
### - Write Training code to create a model based on dataset.
### - Write Generate midi based of model.
### - Write Backing Track generator (select key,tonality,chord progession,timing and tempo) output midi file.
### - Transpose generated midi file to fit generated backing track.
#### Potentialy use music21 library to get key of generated midi (http://web.mit.edu/music21/doc/index.html)
#### Write python script to take in midi sample establish its key and make nescary transpositions to desired key.
#### Adjust bpm of midi track to fit backing track
### - Find suitable midi player library to play back the generated midi track over the backing track.
#### https://www.pygame.org/docs/ref/music.html has midi playback functionality
