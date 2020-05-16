import argparse
import tact
import os
import pandas as pd 
import scipy.io.wavfile as wav
import yaml 

#import measure_hor
parser = argparse.ArgumentParser(description='Tactically test your Acoustica Tracking')

parser.add_argument('-paramfile', action="store",
                                 dest="param_file", 
                                help='path to the parameter file. For more\
                                help on the format of the parameter itself see\
                                the documentation')

parser.add_argument('-run_example', 
                    action="store", dest="run_example", 
                    default=True,
                    help='Runs and example source position set on the default array geometry and outputs\
                    1) the wav file, 2) the source positions and 3) the array geometry')


def main(arg_parser):
    '''
    '''
    args = arg_parser.parse_args()
    if args.run_example:
        tact.make_tact_audio()

    if args.param_file:
        parameters = parse_paramfile(args.param_file)

        tact.make_tact_audio(**parameters)


def parse_paramfile(paramfile_path):
    '''
    Function which parses the yaml parameter file path into a 
    keyword dictionary for input into make_tact_audio
    
    '''

    with open(paramfile_path, 'r') as f:
        keywords = yaml.load(f, Loader=yaml.FullLoader)
    
    for key, value in keywords.items():
        if key in list(load_files_to_data.keys()):
            keywords[key] = load_files_to_data[key](value)
    
    return keywords


to_str = lambda X: str(X)
to_float = lambda X: float(X)
to_path = lambda X: os.path(X)

def load_audio(filepath):
    fs, audio = wav.read(filepath)
    return audio

def convert_to_np_array(filepath):
    '''
    loads csv file and converts to np.array
    '''
    df = pd.read_csv(filepath)
    return df.to_numpy()

load_files_to_data = {
        'source_sound': load_audio,
        'array_geometry': convert_to_np_array,
        'source_position': convert_to_np_array,
        }

if __name__ == '__main__':
	main(parser)