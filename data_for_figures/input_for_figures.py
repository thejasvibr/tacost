# -*- coding: utf-8 -*-
""" Creates the array geometry and source position files 
for Figures 1 and 2 of the JOSS paper accompanying TACOST

General comments
----------------
1) Connect tristar points with lines to show the 'array'-ness of it all 

Created on Wed Jun 10 20:19:56 2020

@author: tbeleyur
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import numpy as np 
import pandas as pd

import tacost 
from tacost.calculate_toa import standard_tristar


def draw_mic_array(mic_xyz, draw_axis):
    for i, each in enumerate(mic_xyz):
        for j,every in enumerate(mic_xyz):
            mic_line = np.row_stack((each,every))
            draw_axis.plot(mic_line[:,0],mic_line[:,1],mic_line[:,2],'k', linewidth=0.5)
    return draw_axis

def make_position_mesh(x,y,z):
    return np.array(np.meshgrid(x, y, z)).T.reshape(-1,3)

########### Figure 1 - highlights the tristar accuarcy checking 

pos_x = np.linspace(0.5, 10, 5)
pos_y, pos_z = pos_x.copy(), pos_x.copy()

source_positions = make_position_mesh(pos_x, pos_y, pos_z)

fig = plt.figure()
ax = plt.subplot(111, projection='3d')
ax.scatter(source_positions[:,0],source_positions[:,1],source_positions[:,2], '*')
ax.scatter(standard_tristar[:,0],standard_tristar[:,1],standard_tristar[:,2],'.')
draw_mic_array(standard_tristar,ax)
plt.tight_layout()
plt.savefig('tristar_example.png')

# make the source positions file 
sourcepos = pd.DataFrame(data=source_positions, columns=['x','y','z'])
sourcepos.to_csv('tristar_source_positions.csv', index=False)


########### Figure 2 - highlights the custom microphone array checking 

# load the microphone positions surveyed with the TotalStation
cave_array = pd.read_csv('Cave.csv')
cave_array.columns = ['position_names','x','y','z']
mic_names = ['M1','M2','M3','M4','M5','M6','M7','S0','S1','S2','S3']
mic_data = cave_array[cave_array['position_names'].isin(mic_names)]
mic_data.index = mic_data['position_names']
mic_data = mic_data[['x','y','z']]

mic_data = mic_data.reindex(['S0','S1','S2','S3','M1','M2','M3','M4','M5','M6','M7'])
mic_data.to_csv('cave_survey_w_mic_index.csv')
mic_data.to_csv('cave_survey_without_mic_index.csv', index=False)

only_mics = np.array(mic_data[['x','y','z']])

cave_x = np.linspace(0, 2.8, 3)
cave_y = np.linspace(-0.5,1.3,3)
cave_z = np.linspace(0.1, 2, 3)

cave_xyz = make_position_mesh(cave_x, cave_y, cave_z)

cave_sourcepos = pd.DataFrame(data=cave_xyz, columns=['x','y','z'])
cave_sourcepos.to_csv('cave_source_positions.csv', index=False)
plt.figure()
ax2 = plt.subplot(111, projection='3d')
ax2.scatter(cave_xyz[:,0],cave_xyz[:,1],cave_xyz[:,2], '*')
ax2.scatter(only_mics[:,0],only_mics[:,1],only_mics[:,2],'*')
draw_mic_array(only_mics[:4,:],ax2)
draw_mic_array(only_mics[4:8,:],ax2)
draw_mic_array(only_mics[7:,:],ax2)

ax2.view_init(elev=41., azim=166)
plt.tight_layout()
plt.savefig('cave_example.png')
az = -140
el=-59