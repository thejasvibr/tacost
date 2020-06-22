# -*- coding: utf-8 -*-
""" Just checking if the audio actuall has 125 calls in it or not!
Created on Fri Jun 12 14:42:22 2020

@author: tbeleyur
"""
import numpy as np 
import scipy.signal as signal
import scipy.ndimage as ndimage
import soundfile as sf
import matplotlib.pyplot as plt 
import tacost
import  tacost.make_source_sounds as source_sound
# load audio
audio, fs = sf.read('../fig1_tristar_audio.wav')
one_channel = audio[:,0]

# smooth 
smoothed = signal.convolve(np.abs(one_channel), np.ones(int(0.003*fs))/int(0.003*fs),'same')

plt.figure()
plt.plot(one_channel)
plt.plot(smoothed)

# all regions above noise
labelled, num = ndimage.label(smoothed>0.001)

print(f"Number of calls in the audio : {num}")
# There are actually 125 points in the 