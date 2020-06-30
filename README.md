# machine-learning-meets-VCV-rack

## Introduction
The project is a small attemp to find a connection between the virtual modular synthesizers world and some machine learning techniques, going from simple MFCC analysis to Magenta's Wavenet.

The goal is: given a target sound, our program will return a sound extracted by a [VCV rack](https://vcvrack.com/) patch. This resulting sound will be as close as possible to the target one.


The idea behind is to set a comparative audio analysis between different samples:
- a single target sample: in my case it is a bird sound.
- a set of sounds extracted from a [VCV Rack](https://vcvrack.com/) patch. See the folder 'VCV patch'.
Check out [here](https://medium.com/@LeonFedden/comparative-audio-analysis-with-wavenet-mfccs-umap-t-sne-and-pca-cb8237bfce2f) how the algorithm works.

## Steps
The program is divided in different steps, each corresponding to different scripts:

1. sendMIDi.py
  - First open the VCV Rack patch in /VCV_patch/ML_vcv.
  - Then right click on the Recorder module and select a directory in which the file will be stored.

  - `sendMIDi.py` uses `mido` library in order to randomise the parameters of Plaits module (Macro Oscillator 2 from Audible Instruents) through CCs thanks to `mido` library. This is the mapping between MIDI CCs and the patch knobs:
    - CC0 : frequency;
    - CC1 : harmonics;
    - CC2 : timbre;
    - CC3 : morph;
    - CC4 : timbre env;
    - CC5 : FM env;
    - CC6 : morph env;
    - CC7 : 8Vert knob;
    - CC8 : LFO-1 Freq;
    - CC127: master volume;
    - CC126: recorder button;

    All the sent CCs will be stored in `sent_cc.json`
    

    PS: feel free to reassign these CCs to any other parameters or different module(s), just make sure to map them using the MIDI Map module!
    PS2 : this randomisation was tailored to work with the Macro Oscillator 2, so please make sure to change the labels for the CCs as well.


<img src="https://github.com/lorenzoPazuzu/machine-learning-meets-VCV-rack/blob/master/images/screenshot_patch.png" width="75%" height="60%">

2. `trimming.py`

This script uses `pydub` library in order to trim your long audio file into 1-second fragments, each corresponding to a different patch.
When the trimming is finished, create a new directory called `VCV patches` into your main folder and drag all the chunks there.

3. `audio_2_z.py`

This is the core of the algorithm. Check it [here](https://medium.com/@LeonFedden/comparative-audio-analysis-with-wavenet-mfccs-umap-t-sne-and-pca-cb8237bfce2f) for more infos. We'll use `sklearn`, `numpy`, and Magenta's `wavenet`.
In order to proceed, install [Magenta](https://magenta.tensorflow.org/) and download [this model's weights](http://download.magenta.tensorflow.org/models/nsynth/wavenet-ckpt.tar) to your working directory.

4. Add your target file!

Now drag your target file (try with a bird sound and call it "bird.wav") on the VCV_patches folder together with all the chunks.

4. `plotting.py`

By running this script you'll execute both `plotting.py` and `audio_2_z.py`. It will return a **blue** dot for each sound/patch, plus a **red** dot for your target sound.

The columns correspond to different numbers of T-SNE iterations (500, 1000, 2000, 5000) while the row correspond to different values of perplexity (5, 30, 50, 100), which relates to the number of nearest neighbours.

<img src="https://github.com/lorenzoPazuzu/machine-learning-meets-VCV-rack/blob/master/images/mfcc-wavenet_176samples.png" width="75%" height="75%">

5. `read_patch.py`

This script computes the Euclidean Distance between the target sound and the closest neighbor. It returns the name of the closest file (patch{number}.wav) to the target sound in the plots, for each of the encoding techniques used (MFCC vs Wavenet) and dimensionality reduction algorithms (t-SNE or PCA).

<img src="https://github.com/lorenzoPazuzu/machine-learning-meets-VCV-rack/blob/master/images/prints.png" width="50%" height="30%">
