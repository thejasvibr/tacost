# -*- coding: utf-8 -*-
"""
Make Sim Audio
--------------
This module handles the actual creation and saving of the audio file itself. 

"""
import numpy as np 
import scipy.spatial as spl

# define mic positions  and calculate the radial distance to the mics
standard_tristar = np.array(([0, 0, 0],
                             [-0.52, 0.0, -0.3],
                             [0.52, 0.0, -0.3],
                             [0, 0.0, 0.6]))

def calculate_mic_arrival_times(emit_points, **kwargs):
    '''
    
    Parameters
    ------------
    emit_points:   np.array
        Npoints x 3 with x,y,z of the emitted positions.

    v_sound : float>0, optional
             Speed of sound, defaults to 338m/s

    array_geometry :  np.array, optional
        Nmicsx3 with x,y,z of each microphone 
        Defaults to the standard 60cm tristar array. 

    intersound_interval : float>0, optional
          Intersound interval between emissions. Defaults to 0.1 seconds            
    
    Returns
    -------
    t_calls_at_mics : np.array
        source_positions x Nmics array. 
        
    '''
    isi = kwargs.get('intersound_interval',0.1) # seconds
    v_sound = kwargs.get('v_sound', 338) # m/s
    
    if emit_points.ndim==1:
        t_emit = isi
    elif emit_points.ndim >1:
        t_emit = np.arange(isi, (emit_points.shape[0]+1)*isi, isi)

    array_geometry = kwargs.get('array_geometry', standard_tristar)

    if array_geometry.ndim==1:
        raise ValueError('Array geometry must have more than 2 mic positions!')

    t_calls_at_mics = np.apply_along_axis(calc_toa_mic_to_points, 1,
                                          array_geometry,
                                          t_emit, emit_points, 
                                          v_sound).T
    return t_calls_at_mics

def calc_toa_mic_to_points(mic_pos, t_emit, source_points, v_sound):
    '''
    Parameters
    ----------
    mic_pos : 1 x3 np.array
    t_emit : Npoints x 1 np.array
        Time of emission from each source point
    source_points : Npoints x 3 np.array
        xyz coordinates of source points
    v_sound : float>0
        velocity of sound in m/s

    Returns
    -------
    toa : np.array
        Npoints x 1 np.array with time 
        of arrival from each source point
        at 

    '''
    if source_points.ndim >1:
        travel_times = np.apply_along_axis(travel_time, 1, source_points,
                                       mic_pos, v_sound)    
    else:
        travel_times = travel_time(source_points, mic_pos, v_sound)

    toa = travel_times + t_emit
    return toa
  

def travel_time(point1, point2, v_sound):
    return distance(point1, point2)/v_sound


def distance(point1, point2):
    return spl.distance.euclidean(point1, point2)


