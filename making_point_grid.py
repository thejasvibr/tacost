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
from mpl_toolkits.mplot3d import Axes3D

plt.rcParams['agg.path.chunksize'] = 100000

# the bat flies parallel to the array in the x axis from
# mic 1 to mic 2
# the trajectory is sampled at 10 Hz, equivalent to a bat echolocating
# at 0.1 s IPI

v_bat = 5.0  # m/s
v_sound = 338.0  # m/s

radius = np.array([3, 4.5, 6, 8.5, 10])
elevation = np.radians([-60,-30,0,30,60])
azimuth = np.radians([0,30,60])

all_r_theta_phis = np.array(np.meshgrid(radius,elevation,azimuth)).T.reshape(-1,3)
trajectory = np.zeros((radius.size*elevation.size*azimuth.size,3))

for row, each_pos in enumerate(all_r_theta_phis):
    r, theta, phi = each_pos
    # converting spherical to cartesian coordinates
    x = r*np.cos(theta)*np.sin(phi)
    y = r*np.cos(theta)*np.cos(phi)
    z = r*np.sin(theta)
    xyz = [x,y,z]
    trajectory[row,:] = xyz



t_emit = np.arange(0.1, (trajectory.shape[0]+1)*0.1, 0.1)
rec_durn = t_emit[-1] + 0.1

# theta_dot = v_bat / radius  # since r * thetadot = v_bat
# traj_x = radius * np.cos(theta_dot * v_bat * t_emit)
# traj_y = 5 + radius * np.sin(theta_dot * v_bat * t_emit)
# traj_z = np.zeros(traj_x.size)
# trajectory = np.column_stack((traj_x, traj_y, traj_z)).reshape(-1, 3)


# define mic positions  and calculate the radial distance to the mics
mic_posns = np.array(([0, 0, 0],
                      [-0.52, 0.0, -0.3],
                      [0.52, 0.0, -0.3],
                      [0, 0.0, 0.6]))


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(trajectory[:,0],trajectory[:,1],trajectory[:,2], '*')
ax.plot(mic_posns[:,0],mic_posns[:,1],mic_posns[:,2],'r*')
#

# calculate mic-bat distances for each call;
t_calls_at_mics = np.zeros((t_emit.size, mic_posns.shape[0]))
for mic_num, each_mic_pos in enumerate(mic_posns):
    row = 0
    print(mic_num)
    for t_call, each_pos in zip(t_emit, trajectory):
        t_calls_at_mics[row, mic_num] = spl.distance.euclidean(each_pos, each_mic_pos) / v_sound + t_call
        row += 1

    # create the WAV files :
fs = 500000
audio = np.zeros((int(rec_durn * fs), 4))
audio += np.random.normal(0, 10 ** (-90 / 20.0), audio.size).reshape(-1, 4)
audio = np.float32(audio)

# create bat call that will be put into the audio
start_f, end_f = 96000, 15000
call_durn = 0.003  # seconds
t = np.linspace(0, call_durn, int(fs * call_durn))
bat_call = signal.chirp(t, start_f, t[-1], end_f, 'logarithmic') * 0.5
bat_call *= signal.tukey(bat_call.size, 0.5)


def assign_call_to_mic(audio_channel, call, t_arrivals):
    '''
    '''
    for each_call in t_arrivals:
        start_sample = int(each_call * fs)
        audio_channel[start_sample:start_sample + call.size] += call

    return (audio_channel)


for each_channel in range(mic_posns.shape[0]):
    assign_call_to_mic(audio[:, each_channel], bat_call,
                       t_calls_at_mics[:, each_channel])

audio_file_name = 'point_grid_simulating_LMU_experiment'
sf.write(audio_file_name + '.WAV', audio, fs)
pd.DataFrame(data=np.column_stack((trajectory, t_emit)),
             columns=['x', 'y', 'z', 't_emit']).to_csv(audio_file_name + '_trajectory_path.csv')
