''' Use this script to view the orientation of the measured and smoothed data 
    files with respect to the crystal axes.  
'''

import glob
import pandas
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from matplotlib import cm


# data file directories
cwd = os.getcwd()
measured_lo_path = cwd + '/measured_data/light_output/'
measured_psp_path = cwd + '/measured_data/pulse_shape_parameter/'
smoothed_lo_path = cwd + '/smoothed_data/light_output/'
smoothed_psp_path = cwd + '/smoothed_data/pulse_shape_parameter/' 

files = glob.glob(smoothed_psp_path + '*')

for fi in files:
    with open(fi, 'r') as f:
        df = pandas.read_csv(f, delimiter=r'\s+', names=['param', 'x', 'y', 'z', 'crystal'])

    if 'measured' in fi:
        # plot x, y, z for with crystal 1 and 2 labeled
        df_crys1 = df.loc[df['crystal'] == 'crystal_1']
        df_crys2 = df.loc[df['crystal'] == 'crystal_2']

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(df_crys1['x'].values, df_crys1['y'].values, df_crys1['z'].values, c='r', label='bvert')
        ax.scatter(df_crys2['x'].values, df_crys2['y'].values, df_crys2['z'].values, c='b', label='cpvert')
        ax.set_xlim([-1.1,1.1])
        ax.set_ylim([-1.1,1.1])
        ax.set_zlim([-1.1,1.1])
        ax.set_xlabel('a')
        ax.set_ylabel('b')
        ax.set_zlabel('c\'')
        ax.set_aspect('equal')
        title = fi.split('\\')
        ax.set_title(title[-1])
        plt.tight_layout()
        plt.legend()

    # plot param values - no interpolation
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    p = ax.scatter(df['x'].values, df['y'].values, df['z'].values, c=df['param'].values, cmap='viridis')
    ax.set_xlim([-1.1,1.1])
    ax.set_ylim([-1.1,1.1])
    ax.set_zlim([-1.1,1.1])
    ax.set_xlabel('a')
    ax.set_ylabel('b')
    ax.set_zlabel('c\'')
    ax.set_aspect('equal')
    title = fi.split('\\')
    ax.set_title(title[-1])
    plt.colorbar(p)
    plt.tight_layout()
    plt.show()

 


    

