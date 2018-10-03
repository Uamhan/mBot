# mBot
## Relevent Links
### 1. http://colah.github.io/posts/2015-08-Understanding-LSTMs/
### 2. http://karpathy.github.io/2015/05/21/rnn-effectiveness/
### 3. https://colinraffel.com/projects/lmd/
### 4. http://web.mit.edu/music21/doc/index.html
### 5. https://www.pygame.org/docs/ref/music.html

## TODO
###  Find suitiable midi dataset.
####   - Potentialy The Lakh MIDI Dataset found in 3 link above
### Write Training code to create a model based on dataset.
### Write Generate midi based of model.
### Write Backing Track generator (select key,tonality,chord progession,timing and tempo) output midi file values could be randomly selected for one click composition.
### Transpose generated midi file to fit generated backing track.
####   - Potentialy use music21 library to get key of generated midi (documentation link 4 above)
####   - Write python script to take in midi sample establish its key and make nescary transpositions to desired key.
####   - Adjust bpm of midi track to fit backing track
### Find suitable midi player library to play back the generated midi track over the backing track.
####    - pygame has midi playback functionality documentation found in link 5 abobr
