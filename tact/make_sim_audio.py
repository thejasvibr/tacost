# -*- coding: utf-8 -*-
"""
Make Sim Audio
--------------
This module handles the placement of source sounds into the 
audio and saving the file. 

"""

import os
import numpy as np 
import scipy.io.wavfile as wav
from tact.calculate_toa import calculate_mic_arrival_times
from tact.make_positions import generate_LMU_emitted_positions
from tact.make_source_sounds import make_bat_call

rms = lambda X: np.sqrt(np.mean(X**2.0))
dB = lambda X: 20*np.log10(abs(X))

def assign_call_to_mic(audio_channel, call, t_arrivals,**kwargs):
    '''
    

    '''
    for each_call in t_arrivals:
        start_sample = int(each_call * kwargs['sample_rate'])
        audio_channel[start_sample:start_sample + call.size] += call

    return audio_channel

def create_audio_for_mic_arrival_times(t_arrivals, **kwargs):
    '''
    
    Keyword Arguments
    -------------------
    sample_rate : float>0
        Sampling rate in Hz. 
        Defaults to 500kHz. 
    background_noise : float. 
                       db rms of white noise. Defaults to -90 dB rms re 1.
    call_SNR : tuple/list like. 
               If a single entry is given, all channels will have the same call SNR.
               Otherwise, Nchannel entries are expected. Defaults to 50dB SNR
    sound_snr : np.array, optional
		User's own sound which needs to be incorporated into the playback. 
		If not given, then the function uses make_bat_call

    Returns
    -------
    audio : np.array
    sample_rate : float>0
    '''
    
    # create the WAV files :
    
    if kwargs.get('sample_rate') is None:
        kwargs['sample_rate'] = 500000
    sample_rate = kwargs.get('sample_rate')
    n_channels = t_arrivals.shape[1]
    rec_durn = np.max(t_arrivals) + 0.05 # recording ends 50 milliseconds after start of last arriving call
    audio = np.zeros((int(rec_durn * sample_rate), n_channels))
    
    background_noise = kwargs.get('background_noise', -90)
    audio += np.random.normal(0, 10**(background_noise/20.0), 
                                      audio.size).reshape(-1, n_channels)
    audio = np.float32(audio)
    
    bat_call = kwargs.get('source_sound', make_bat_call(**kwargs))
    target_SNR = kwargs.get('sound_snr', [50])
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

    return audio, sample_rate

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

def make_tact_audio(**kwargs):
    '''
    The main interface function through which all parameters are passed


    '''
    
    points= kwargs.get('source_position', generate_LMU_emitted_positions())
    tcalls = calculate_mic_arrival_times(points, **kwargs)
    audio, fs = create_audio_for_mic_arrival_times(tcalls,**kwargs)
    
    sim_name = kwargs.get('sim_name', 'tact_simaudio')
    print('SIM NAME ####', sim_name)
    try:
        wav.write(sim_name+'.wav', fs, audio)
    except:
        print(kwargs.keys())
        raise IOError(f'Could not write {sim_name}.wav. Please check if input parameters are proper')



def simulate_audio_for_LMU_experiment(**kwargs):
    '''
    Keyword Arguments
    -------------------
    points : Npoints x 3 np.array 
             x,Y,Z coordinates of the emitted points
    '''
    
    points= kwargs.get('points', generate_LMU_emitted_positions())
    tcalls = calculate_mic_arrival_times(points, **kwargs)
    audio = create_audio_for_mic_arrival_times(tcalls,**kwargs)
    return audio 

