# -*- coding: utf-8 -*-
"""Module to make some simulated data testing the TOADsuite
Created on Wed May 22 20:13:28 2019

@author: tbeleyur
"""

import numpy as np 
import pandas as pd
import scipy.signal as signal 


rms = lambda X: np.sqrt(np.mean(X**2.0))
dB = lambda X: 20*np.log10(abs(X))

def assign_call_to_mic(audio_channel, call, t_arrivals,**kwargs):
    '''
    

    '''
    for each_call in t_arrivals:
        start_sample = int(each_call * kwargs['fs'])
        audio_channel[start_sample:start_sample + call.size] += call

    return audio_channel

def create_audio_for_mic_arrival_times(t_arrivals, **kwargs):
    '''
    
    Keyword Arguments
    -------------------
    fs : float>0
        Sampling rate in Hz. 
        Defaults to 500kHz. 

    background_noise : float. 
                       db rms of white noise. Defaults to -90 dB rms re 1.

    call_SNR : tuple/list like. 
               If a single entry is given, all channels will have the same call SNR.
               Otherwise, Nchannel entries are expected. 
    playback_sound : np.array, optional
		User's own sound which needs to be incorporated into the playback. 
		If not given, then the function uses make_bat_call
		
    '''
    
    # create the WAV files :
    fs = kwargs.get('fs',500000)
    n_channels = t_arrivals.shape[1]
    rec_durn = np.max(t_arrivals) + 0.05 # recording ends 50 milliseconds after start of last arriving call
    audio = np.zeros((int(rec_durn * fs), n_channels))
    
    background_noise = kwargs.get('background_noise', -60)
    audio += np.random.normal(0, 10 ** (background_noise/20.0), audio.size).reshape(-1, 4)
    audio = np.float32(audio)
    
    bat_call = kwargs.get('playback_sound', make_bat_call(**kwargs))
    target_SNR = kwargs.get('call_SNR', [50])
    adjusted_rms_batcalls = adjust_rms_to_reach_SNR(bat_call, target_SNR, audio)
    
    if len(adjusted_rms_batcalls)==n_channels:
        for each_channel in range(t_arrivals.shape[1]):
            assign_call_to_mic(audio[:, each_channel], adjusted_rms_batcalls[each_channel],
                               t_arrivals[:, each_channel],**kwargs)

        
        
    elif len(adjusted_rms_batcalls) ==1:
        for each_channel in range(t_arrivals.shape[1]):
            assign_call_to_mic(audio[:, each_channel], adjusted_rms_batcalls[0],
                               t_arrivals[:, each_channel],**kwargs)

    audio *= 0.9

    return audio, fs

def adjust_rms_to_reach_SNR(bat_call, SNR, empty_audio):
    '''
    Parameters
    ----------
    bat_call : Nsamples np.array
    
    SNR : float or array/list like. 
          If a single entry is given, then only the 
          
    empty_audio : Msamples np.array
            Single channel audio without the bat calls in them - the 'noise'

    Returns
    -------
    adjusted_bat_calls : array/list like. 
                        Contains the rms adjusted versions fo the input bat call
                        for each channel. 

    '''
    rms_empty = rms(empty_audio)
    current_SNR = dB(rms(bat_call)) - dB(rms(empty_audio))

    adjusted_bat_calls = []
    for each in SNR:
        required_gain = each - current_SNR
        adjusted_rms_call = bat_call*10**(required_gain/20.0)
        adjusted_bat_calls.append(adjusted_rms_call)

    return adjusted_bat_calls

def simulate_audio_for_LMU_experiment(**kwargs):
    '''
    Keyword Arguments
    -------------------
    points : Npoints x 3 np.array 
             x,Y,Z coordinates of the emitted points
    '''
    
    points= kwargs.get('points',generate_LMU_emitted_positions())
    tcalls = calculate_mic_arrival_times(points, **kwargs)
    audio = create_audio_for_mic_arrival_times(tcalls,**kwargs)
    return audio 
    