# -*- coding: utf-8 -*-
"""
Make Default Positions
----------------------
This module handles the creation of some default sound source positions

"""
import numpy as np 

def generate_LMU_emitted_positions():
    '''Creates a hemisphere of positions matching those done in the LMU corridor
    
    Returns
    --------
    emitted_points : Npositions x 3 np.array with x,y,z co-ordinates
    '''

    radius = np.array([3, 4.5, 6, 8.5, 10])
    elevation = np.radians([-60,-30,0,30,60])
    azimuth = np.radians([0,30,60])

    all_r_theta_phis = np.array(np.meshgrid(radius,elevation,azimuth)).T.reshape(-1,3)
    emitted_points = np.zeros((radius.size*elevation.size*azimuth.size,3))

    for row, each_pos in enumerate(all_r_theta_phis):
        r, theta, phi = each_pos
        # converting spherical to cartesian coordinates
        x = r*np.cos(theta)*np.sin(phi)
        y = r*np.cos(theta)*np.cos(phi)
        z = r*np.sin(theta)
        xyz = [x,y,z]
        emitted_points[row,:] = xyz
    return emitted_points


