# -*- coding: utf-8 -*-
"""Module to make some simulated data testing the TOADsuite
Created on Wed May 22 20:13:28 2019

@author: tbeleyur
"""

import numpy as np 
import pandas as pd
import scipy.signal as signal 
import scipy.spatial as spl
import soundfile as sf
import matplotlib.pyplot as plt
plt.rcParams['agg.path.chunksize'] = 100000


# the bat flies parallel to the array in the x axis from 
# mic 1 to mic 2
# the trajectory is sampled at 10 Hz, equivalent to a bat echolocating 
# at 0.1 s IPI

v_bat = 5.0 # m/s
v_sound = 338.0 # m/s
rec_durn = 4.0 # seconds
t_emit = np.arange(0.1,rec_durn,0.1)
radius = 3.0
traj_x = np.zeros(t_emit.size) # so that the bat makes a pass from the left to the right 
traj_y = 1.5 + t_emit*v_bat
traj_z = np.zeros(traj_x.size)
trajectory = np.column_stack((traj_x, traj_y, traj_z)).reshape(-1,3)

# define mic positions  and calculate the radial distance to the mics 
mic_posns = np.array(([0,   0     ,0],
                      [-0.52,-0.0,-0.3],
                      [0.52,-0.0,-0.3],
                      [0,-0.2,0.6]))

# calculate mic-bat distances for each call;
t_calls_at_mics = np.zeros((t_emit.size, mic_posns.shape[0]))
for mic_num, each_mic_pos in enumerate(mic_posns):
    row = 0
    print(mic_num)
    for t_call, each_pos in zip(t_emit, trajectory):
        t_calls_at_mics[row, mic_num] = spl.distance.euclidean(each_pos, each_mic_pos)/v_sound + t_call
        row += 1 

# create the WAV files :
fs = 500000
audio = np.zeros((int(rec_durn*fs), 4))
audio += np.random.normal(0,10**(-90/20.0),audio.size).reshape(-1,4)
audio = np.float32(audio)

# create bat call that will be put into the audio
start_f, end_f = 96000, 15000
call_durn = 0.003 # seconds
t = np.linspace(0,call_durn,int(fs*call_durn))
bat_call = signal.chirp(t, start_f, t[-1], end_f, 'logarithmic') * 0.5
bat_call *= signal.tukey(bat_call.size, 0.5)


def assign_call_to_mic(audio_channel, call, t_arrivals ):
    '''
    '''
    for each_call in t_arrivals:
        start_sample = int(each_call*fs)
        audio_channel[start_sample:start_sample+call.size] += call
    
    return(audio_channel)

for each_channel in range(mic_posns.shape[0]):
    assign_call_to_mic(audio[:,each_channel], bat_call,
                                                 t_calls_at_mics[:,each_channel])

audio_file_name = 'bat_flying_in_arc_from_2D_60cmtristar'
sf.write(audio_file_name+'.WAV', audio, fs)
pd.DataFrame(data=np.column_stack((trajectory,t_emit)),
             columns=['x','y','z','t_emit']).to_csv(audio_file_name+'_trajectory_path.csv')
