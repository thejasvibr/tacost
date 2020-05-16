# -*- coding: utf-8 -*-
"""
Tests for make_positions module

@author: tbeleyur
"""
import unittest
from tact.make_positions import *

class LMUpositionSet(unittest.TestCase):
    
    def test_integration(self):
        '''
        Just check that it works
        '''
        generate_LMU_emitted_positions()
