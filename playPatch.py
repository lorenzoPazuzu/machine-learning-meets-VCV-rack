from readPatch import *
import mido

port = mido.open_output('IAC Driver WebMIDI')

def play_Patch(name):
    newPatch = []
    patch = control_list[soundindex_patch_converter(name)]
    patch = patch[1]
    patch = patch[5:]
    #returns only the numbers
    for element in patch:
        number = element.split('=')
        element = int(number[1])
        newPatch.append(element)


    start_audio = mido.Message('control_change', channel=1, control=127, value=50)
    port.send(start_audio)
    cc_freq = mido.Message('control_change', channel=1, control=0, value=newPatch[0])
    cc_harm = mido.Message('control_change', channel=1, control=1, value=newPatch[1])
    cc_timbre = mido.Message('control_change', channel=1, control=2, value=newPatch[2])
    cc_morph = mido.Message('control_change', channel=1, control=3, value=newPatch[3])
    cc_tim_env = mido.Message('control_change', channel=1, control=4, value=newPatch[4])
    cc_FM = mido.Message('control_change', channel=1, control=5, value=newPatch[5])
    cc_morph_env = mido.Message('control_change', channel=1, control=6, value=newPatch[6])
    cc_8vert = mido.Message('control_change', channel=1, control=7, value=newPatch[7])
    cc_freq_lfo = mido.Message('control_change', channel=1, control=8, value=newPatch[8])

    port.send(cc_freq)
    port.send(cc_harm)
    port.send(cc_timbre)
    port.send(cc_morph)
    port.send(cc_tim_env)
    port.send(cc_FM)
    port.send(cc_morph_env)
    port.send(cc_8vert)
    port.send(cc_freq_lfo)


play_Patch('patch42.wav')



### STOP PATCH

stop_audio = mido.Message('control_change', channel=1, control=127, value=0)
port.send(stop_audio)