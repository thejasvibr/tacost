# -*- coding: utf-8 -*-
"""
Created on Sat May 16 17:42:53 2020

@author: tbeleyur
"""

import scipy.signal as signal 
import numpy as np 


def make_bat_call(**kwargs):
    '''
    Makes a linear sweep from 0.4*sample rate to 0.1*sample rate
    
    Parameters
    ----------
    sample_rate : float>0
    
    call_durn : float>0, optional
        Defaults to 0.003 s
    
    '''
    sample_rate = kwargs['sample_rate']
    # create bat call that will be put into the audio
    start_f, end_f = sample_rate*0.4, sample_rate*0.1
    
    call_durn = kwargs.get('call_durn',0.003)
    t = np.linspace(0, call_durn, int(sample_rate * call_durn))
    bat_call = signal.chirp(t, start_f, t[-1], end_f) * 0.5
    bat_call *= signal.tukey(bat_call.size, 0.5)
    return bat_call
