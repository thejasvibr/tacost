# -*- coding: utf-8 -*-
"""
Created on Sat May 16 15:12:52 2020

@author: tbeleyur
"""

import pandas as pd
import unittest

class ParseParamfile(unittest.TestCase):
    
    def setUp(self):
        df = pd.DataFrame(data={'sample_rate':44100,
                                'sim_name':'MAIOW'})
        df.to_csv('params.csv')
    
    def test_simple(self):
        
    