# -*- coding: utf-8 -*-
"""TODO: 
    > os.system doesn't allow feedback - figure out 
    ways to capture errors raised in the commandline
Created on Sat May 16 15:12:52 2020

@author: tbeleyur
"""
import glob
import tacost
import numpy as np 
import os 
import subprocess
import pandas as pd
import scipy.io.wavfile as wav
import unittest
import yaml
from tacost.__main__ import msg

class ParseParamfile(unittest.TestCase):
    
    def setUp(self):
        self.yamlfilename = 'params_setup.yaml'
        
    def tearDown(self):
        try:
            os.remove(self.yamlfilename)
        except FileNotFoundError:
            pass
        
        # remove any wav files if any
        wavfiles = glob.glob('*.wav')
        if len(wavfiles) >0:
            for each in wavfiles:
                os.remove(each)
        
    def make_yamlfile(self,setupdata):
        
        with open(self.yamlfilename,'w') as setupyaml:
            docs = yaml.dump(setupdata, setupyaml)
        
    def call_tacost_cli(self, test_name):
        tacost_output = subprocess.getoutput(f"python -m tacost -paramfile {self.yamlfilename}")
        if 'Error' in tacost_output:
            print(tacost_output)
            raise RuntimeError(f'Something has gone wrong in {test_name}')
    
    def make_yaml_and_runcli(self, data, test_name):
        self.make_yamlfile(data)
        self.call_tacost_cli(test_name)
    
    def test_check_simname_saved_properly(self):
        data={'sim_name':'MAIOW'}
        self.make_yaml_and_runcli(data, 'test_check_simname_saved_properly')
        # check simname is as expected:
        wavfile_name_matches = data['sim_name']+'.wav' in os.listdir()
        self.assertTrue(wavfile_name_matches)
    
    def get_wav_file(self):
        wavfiles = glob.glob('*.wav')
        if len(wavfiles)>1:
            raise ValueError(f'More than 1 wav file in the folder!{wavfiles}')
        elif len(wavfiles)==0:
            raise ValueError('No wav files in the folder!')
        else:
            return wavfiles
    
    def load_wav_file(self):
        wavfile_path = self.get_wav_file()
        fs, audio = wav.read(wavfile_path[0])
        return audio, fs
    
    def make_sure_one_wavfile(self):
        wf = self.get_wav_file()
        self.assertTrue(len(wf)==1)
    
    def test_samplerate_proper(self):
        data={'sim_name':'funny',
              'sample_rate':192000}
        self.make_yaml_and_runcli(data, 'test_samplerate_proper')
        audio, fs = self.load_wav_file()
        self.assertEqual(fs, data['sample_rate'])
    
    def test_source_sound_reading(self):
        '''
        Not a real test - just checks if the functionality works
        '''
        data = {'source_sound':'custom.wav',
                'sample_rate':250000,
                'sim_name':'custom_sim',
                }
        custom_sound = np.random.normal(0,1,2500)
        wav.write(data['source_sound'], 250000, custom_sound)
        
        self.make_yaml_and_runcli(data, 'test_source_sound_reading')
        # load the wav file and 
        fs, simaudio = wav.read(data['sim_name']+'.wav')
    
    def test_check_array_geom(self):
        random_array = np.random.normal(0,1,12).reshape(-1,3)
        arraygeom_df = pd.DataFrame(data=random_array,
                                    columns=['x','y','z'])
        customgeomfile = 'customarraygeom.csv'
        arraygeom_df.to_csv(customgeomfile)
        
        data = {'array_geometry':customgeomfile}
        self.make_yaml_and_runcli(data, 'test_check_array_geom')
        self.make_sure_one_wavfile()
    
    def test_check_array_geom_2mics(self):
        random_array = np.random.normal(0,1,6).reshape(-1,3)
        arraygeom_df = pd.DataFrame(data=random_array,
                                    columns=['x','y','z'])
        customgeomfile = 'customarraygeom.csv'
        arraygeom_df.to_csv(customgeomfile)
        
        data = {'array_geometry':customgeomfile}
        self.make_yaml_and_runcli(data, 'test_check_array_geom_2mics')
        self.make_sure_one_wavfile()
    
    def test_sourcepos(self):
        random_array = np.random.normal(0,1,6).reshape(-1,3)
        random_pos = pd.DataFrame(data=random_array,
                                    columns=['x','y','z'])
        
        sourcepos_filename = 'customsourcepos.csv'
        random_pos.to_csv(sourcepos_filename)
        
        data = {'source_position': sourcepos_filename}
        self.make_yaml_and_runcli(data, 'test_sourcepos')
        self.make_sure_one_wavfile()
    
    def test_check_isi(self):
        data = {'intersound_interval': 0.001}
        self.make_yaml_and_runcli(data, 'test_check_isi')
        self.make_sure_one_wavfile()

    def test_checkSNR(self):
        data = {'sound_snr': [40]}
        self.make_yaml_and_runcli(data, 'test_checkSNR')
        self.make_sure_one_wavfile()
    def test_check_multiSNRs(self):
        data = {'sound_snr': [40,30,20,10]}
        self.make_yaml_and_runcli(data, 'test_check_multiSNRs')
        self.make_sure_one_wavfile()
        
        
       
    def test_source_sound_loading(self):
        pass

class RunExampleTest(unittest.TestCase):
   
    def tearDown(self):
       
        # remove any wav files if any
        wavfiles = glob.glob('*.wav')
        if len(wavfiles) >0:
            for each in wavfiles:
                os.remove(each)
    
    def test_mimic_run_example(self):
        # mimic a user running 
        output = subprocess.getoutput('python -m tacost -run_example')
        self.assertEqual(output, msg)
        


if __name__ == '__main__':
    unittest.main()
        
    