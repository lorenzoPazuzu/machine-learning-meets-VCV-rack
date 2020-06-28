# machine-learning-meets-VCV-rack


This projects performs a comparative audio analysis between different samples:
- a single target sample: in my case it was a bird sound.
- a big set of sounds extracted from a VCV Rack patch. (https://vcvrack.com/) See the folder 'VCV patch'.

Our goal is, given a target sound, to find a set of parameters for that patch whose output will be the most similar to the target.


The program is divided in different steps, each corresponding to different scripts:

1. `sendMIDi.py`
  - First open the VCV Rack patch in /VCV_patch/ML_vcv.
  - Then right click on the Recorder module and select a directory in which the file will be stored.

`sendMIDi.py` uses `mido` library in order to randomise the parameters of Plaits module (Macro Oscillator 2 from Audible Instruents) through CCs thanks to `mido` library.

This is the mapping between MIDI CCs and the patch knobs:
CC0 : frequency
CC1 : harmonics
CC2 : timbre
CC3 : morph

CC4 : timbre env
CC5 : FM env
CC6 : morph env

CC7 : 8Vert knob
CC8 : LFO-1 Freq

CC127: master volume
CC126: recorder button

All the sent CCs will be stored in `sent_cc.json`

PS: feel free to reassign these CCs to any other parameters or different module(s), just make sure to map them using the MIDI Map module!
PS2 : this randomisation was tailored to work with the Macro Oscillator 2, so please make sure to change the labels for the CCs as well.

![alt text](https://github.com/lorenzoPazuzu/machine-learning-meets-VCV-rack/blob/master/images/screenshot_patch.jpg?raw=true)

2. 
