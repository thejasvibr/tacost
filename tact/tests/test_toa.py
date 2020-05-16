# -*- coding: utf-8 -*-
"""
Created on Sat May 16 15:12:52 2020

@author: tbeleyur
"""
import numpy as np 
import pandas as pd
import unittest
from tact.calculate_toa import *

class TestMic2Points(unittest.TestCase):
    
    def setUp(self):
        self.mic_pos = np.array([0,0,0])
        self.temit = np.array(([0.1, 0.2, 0.3]))
        self.sources = np.array(([0,1,0],
                                 [1,0,0],
                                 [0,0,1]))
    
        self.v_sound = 330.0 
        
    def test_simple(self):
        toa = calc_toa_mic_to_points(self.mic_pos, self.temit, 
                                     self.sources,
                                     self.v_sound)
        
        expected = self.temit + travel_time(self.mic_pos, self.sources[0,:], 
                               self.v_sound)
        match = np.allclose(toa, expected)
        self.assertTrue(match)
    
    def test_single_sourcepoint(self):
        self.sources = np.array([0,1,0])
        self.temit = np.array([0.1])
        
        toa = calc_toa_mic_to_points(self.mic_pos, self.temit, 
                                     self.sources,
                                     self.v_sound)
        
        expected = self.temit + travel_time(self.mic_pos, self.sources, 
                               self.v_sound)
        match = np.allclose(toa, expected)
        self.assertTrue(match) 
    
class TestCalcMicArrivalTimes(unittest.TestCase):
    '''
    '''
    
    def setUp(self):
        self.source = np.array(([0,1,0],
                                 [1,0,0],
                                 [0,0,1]))

        self.mic_pos = np.array(([0,0,0],
                                 [0,0,0]))
        self.vsound = 330.0
        
    def test_simple(self):
        toa = calculate_mic_arrival_times(self.source,
                                    array_geometry=self.mic_pos,
                                        v_sound = self.vsound)
        
        both_toas_same = np.array_equal(toa[:,0], toa[:,1])
        self.assertTrue(both_toas_same)
        
    
    def test_single_mic(self):
        self.mic_pos = np.array([0,0,0])
        
        with self.assertRaises(ValueError):
            toa = calculate_mic_arrival_times(self.source,
                                    array_geometry=self.mic_pos,
                                        v_sound = self.vsound)
        
    def test_singlepoint(self):
        self.source = np.array([0,1,0])
        toa = calculate_mic_arrival_times(self.source,
                                    array_geometry=self.mic_pos,
                                        v_sound = self.vsound)
        
        exp_toa = calc_toa_mic_to_points(self.source, 0.1,
                                         self.mic_pos[0,:],
                                         self.vsound)
        
        match = np.array_equal(np.tile(exp_toa, 2), toa)
        self.assertTrue(match)
    


if __name__ == '__main__':
    unittest.main()