import mido
import random
import time
import json

random_freq_cc0 = []
random_harm_cc1 = []
random_timbre_cc2 = []
random_morph_cc3 = []
random_tim_env_cc4 = []
random_FM_cc5 = []
random_morph_env_cc6 = []
random_8vert_cc7 = []
random_lfo_cc8 = []

dict_cc = {}

random.seed(8)

# green or red depending on the mode
mode_flag = 'green'
# 1 - 8 depending on the synthesis mode
button_flag = 1

'''
CONTROL CHANGE:

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
'''

for elem in range(10):
    random_freq_cc0.append(random.randrange(0, 127, 2))
    random_harm_cc1.append(random.randrange(0, 127, 2))
    random_timbre_cc2.append(random.randrange(0, 127, 2))
    random_morph_cc3.append(random.randrange(0, 127, 2))
    random_tim_env_cc4.append(random.randrange(0, 127, 2))
    random_FM_cc5.append(random.randrange(0, 127, 2))
    random_morph_env_cc6.append(random.randrange(0, 127, 2))
    random_8vert_cc7.append(random.randrange(0, 127, 2))
    random_lfo_cc8.append(random.randrange(0, 127, 2))

port = mido.open_output('IAC Driver WebMIDI')

#opens the master at 50
start_audio = mido.Message('control_change', channel=1, control=127, value=50)
start_recording = mido.Message('control_change', channel=1, control=126, value=127)
port.send(start_audio)
port.send(start_recording)

#loop between 16 synthesis modes:

internal_count = 0

for mode in range(16):

    internal_count += 1

    # randomizing 10 patches
    for elem in range(len(random_freq_cc0)):
        cc_freq = mido.Message('control_change', channel=1, control=0, value = random_freq_cc0[elem])
        cc_harm = mido.Message('control_change', channel=1, control=1, value = random_harm_cc1[elem])
        cc_timbre = mido.Message('control_change', channel=1, control=2, value=random_timbre_cc2[elem])
        cc_morph = mido.Message('control_change', channel=1, control=3, value=random_morph_cc3[elem])
        cc_tim_env = mido.Message('control_change', channel=1, control=4, value=random_tim_env_cc4[elem])
        cc_FM = mido.Message('control_change', channel=1, control=5, value=random_FM_cc5[elem])
        cc_morph_env = mido.Message('control_change', channel=1, control=6, value=random_morph_env_cc6[elem])
        cc_8vert = mido.Message('control_change', channel=1, control=7, value=random_8vert_cc7[elem])
        cc_freq_lfo = mido.Message('control_change', channel=1, control = 8, value = random_lfo_cc8[elem])
        port.send(cc_freq)
        port.send(cc_harm)
        port.send(cc_timbre)
        port.send(cc_morph)
        port.send(cc_tim_env)
        port.send(cc_FM)
        port.send(cc_morph_env)
        port.send(cc_8vert)
        port.send(cc_freq_lfo)

        # adding to dictionary
        cc_string = str(cc_freq)
        cc_list = cc_string.split(' ')
        cc_list.append('freq_cc=%d' % (random_freq_cc0[elem]))
        cc_list.append('harm_cc=%d' % (random_harm_cc1[elem]))
        cc_list.append('timbre_cc=%d' % (random_timbre_cc2[elem]))
        cc_list.append('morph_cc=%d' % (random_morph_cc3[elem]))
        cc_list.append('tim_env_cc=%d' % (random_tim_env_cc4[elem]))
        cc_list.append('FM_cc=%d' % (random_FM_cc5[elem]))
        cc_list.append('morph=%d' % (random_morph_env_cc6[elem]))
        cc_list.append('8vert_cc=%d' % (random_8vert_cc7[elem]))
        cc_list.append('lfo_cc8=%d' % (random_lfo_cc8[elem]))
        #the name of the files will be like: 6_green_7 = 6th synthesis method, green light, 7th randomization.
        name_dict = str(button_flag) + '_' + mode_flag + '_' + str(elem)
        dict_cc[name_dict] = cc_list


        time.sleep(1)

    #toggles btw the two modes
    if internal_count <= 2:
        mode_flag = 'red'
        #CC = 10 pushes the RIGHT (red) button
        toggle_green_red_1 = mido.Message('control_change', channel=1, control=10, value=0)
        port.send(toggle_green_red_1)
        toggle_green_red_0 = mido.Message('control_change', channel=1, control=10, value = 120)
        port.send(toggle_green_red_0)
        time.sleep(1)
        toggle_green_red_1 = mido.Message('control_change', channel=1, control=10, value=0)
        port.send(toggle_green_red_1)
        print('red!')
        if internal_count == 2:
            button_flag += 1
            print('now button flag ist', button_flag)
        else:
            print('button flag stayed ', button_flag)
    else:
        mode_flag = 'green'
        # CC = 10 pushes the LEFT (green) button
        toggle_red_green_1 = mido.Message('control_change', channel=1, control=100, value=0)
        port.send(toggle_red_green_1)
        toggle_red_green_0 = mido.Message('control_change', channel=1, control=100, value = 120)
        port.send(toggle_red_green_0)
        time.sleep(1)
        toggle_red_green_1 = mido.Message('control_change', channel=1, control=100, value=0)
        port.send(toggle_red_green_1)
        print('green!')
        if internal_count == 4:
            internal_count = 0
            button_flag += 1
            print('button flag is now ', button_flag)
            print('internal count is now ', internal_count)
            print('reset!')
        else:
            print('button flag stayed', button_flag)


# sets the master volume to zero
stop_audio = mido.Message('control_change', channel=1, control=127, value=0)
port.send(stop_audio)

stop_recording_0 = mido.Message('control_change', channel=1, control=126, value=0)
port.send(stop_recording_0)
stop_recording_1 = mido.Message('control_change', channel=1, control=126, value=120)
port.send(stop_recording_1)
stop_recording_2 = mido.Message('control_change', channel=1, control=126, value=0)
port.send(stop_recording_2)


'''
# all notes off
for i in range(127):
    msg = mido.Message('note_off', note=i)
    msg.copy(channel=1)
    port.send(msg)
'''

with open("sent_cc.json", "w") as write_file:
    json.dump(dict_cc, write_file)