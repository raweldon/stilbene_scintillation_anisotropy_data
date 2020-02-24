''' Plots the measured and smoothed light output and pulse shape parameter data
    Selection of plots and plotted data can be made in the main block
'''

import glob
import pandas
import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
from matplotlib import cm

def plot_3D(files):

    for f in files:
        with open(f, 'r') as fin:
            df = pandas.read_csv(fin, delimiter=r'\s+', names=['param', 'param_unc', 'x', 'y', 'z', 'Ep', 'Ep_unc', 'crystal'])
        if 'measured' in f:
            # plot trajectories measured with crystal 1 and 2
            df_crys1 = df.loc[df['crystal'] == 'crystal_1']
            df_crys2 = df.loc[df['crystal'] == 'crystal_2']

            fig = plt.figure(figsize=(6.5,6))
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(df_crys1['x'].values, df_crys1['y'].values, df_crys1['z'].values, c='r', label='bvert')
            ax.scatter(df_crys2['x'].values, df_crys2['y'].values, df_crys2['z'].values, c='b', label='cpvert')
            ax.set_xlim([-1.1,1.1])
            ax.set_ylim([-1.1,1.1])
            ax.set_zlim([-1.1,1.1])
            ax.set_xlabel('a')
            ax.set_ylabel('b')
            ax.set_zlabel('c\'')
            title = f.split('\\')
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
        title = f.split('\\')
        ax.set_title(title[-1])
        plt.colorbar(p)
        plt.tight_layout()

def lambert_projection_plots(files):

    # ignore divide by zero warning
    np.seterr(divide='ignore', invalid='ignore')

    for f in files:
        with open(f, 'r') as fin:
            df = pandas.read_csv(fin, delimiter=r'\s+', names=['param', 'param_unc', 'x', 'y', 'z', 'Ep', 'Ep_unc', 'crystal'])

        # convert to lambertian projection (from https://en.wikipedia.org/wiki/Lambert_azimuthal_equal-area_projection)
        X, Y = [], []
        for xi, yi, zi in zip(df.x.values, df.y.values, df.z.values):
            Xi = np.sqrt(2/(1-zi))*xi
            Yi = np.sqrt(2/(1-zi))*yi
            if np.isnan(Xi) or np.isnan(Yi):
                zi -= 0.000001
                Xi = np.sqrt(2/(1-zi))*xi
                Yi = np.sqrt(2/(1-zi))*yi    
            if np.isinf(Xi) or np.isinf(Yi):
                zi -= 0.000001
                Xi = np.sqrt(2/(1-zi))*xi
                Yi = np.sqrt(2/(1-zi))*yi  
            X.append(Xi)
            Y.append(Yi)
        X = np.array(X)/max(X)
        Y = np.array(Y)/max(Y)

        # make mesh grid
        grid_x, grid_y = np.mgrid[-1:1:1000j, -1:1:1000j]
        interp = scipy.interpolate.griddata((X, Y), df.param.values, (grid_x, grid_y), method='linear')

        # plot
        plt.figure()
        plt.rcParams['axes.facecolor'] = 'grey'
        plt.imshow(interp.T, extent=(-1,1,-1,1), origin='lower', cmap='viridis', interpolation='none')
        #plt.scatter(X, Y, c=df.param.values, cmap='viridis')
        ## put avg uncert on colorbar
        avg_uncert = df.param_unc.mean()/(df.param.max() - df.param.min()) # scale y from (0, 1) to (min(ql), max(ql))

        if 'psp_' in f:
            cbar = plt.colorbar(format='%1.3f')
            cbar.set_label('Pulse shape parameter', rotation=270, labelpad=22, fontsize=18)
        else:
            cbar = plt.colorbar(format='%1.2f')
            cbar.set_label('Light output (MeVee)', rotation=270, labelpad=22, fontsize=18)

        cbar.ax.errorbar((df.param.max() + df.param.min())/2., (df.param.max() + df.param.min())/2., 
                        yerr=df.param_unc.mean(), ecolor='w', elinewidth=2, capsize=4, capthick=2)
        cbar.ax.tick_params(labelsize=14)

        # print( '{:>6.1f} {:>8.3f} {:>8.4f} {:>8.4f}'.format(df.Ep.values[0], df.param.mean(),
        #                                                     df.param_unc.mean(), df.param_unc.mean()/df.param.mean()*100))
        plt.text(-0.71, 0.0, 'a', color='r', fontsize=16)
        plt.text(0.71, 0., 'a', color='r', fontsize=16)
        plt.text(0, 0.0, 'c\'', color='r', fontsize=16)
        plt.text(0, 0.713, 'b', color='r', fontsize=16)
        plt.text(0, -0.713, 'b', color='r', fontsize=16)
        if 'low_gain' in f:
            plt.title(str(df.Ep.values[0]) + ' MeV recoil protons, low gain', fontsize=20)
        else:
            plt.title(str(df.Ep.values[0]) + ' MeV recoil protons, high gain', fontsize=20)
        plt.xticks([])
        plt.yticks([])
        plt.tight_layout()


if __name__ == '__main__':

    # select plots to show
    plot_3d = True
    plot_lambert_projection = True

    # select data file directory
    cwd = os.getcwd()
    measured_lo_path = cwd + '/measured_data/light_output/'
    measured_psp_path = cwd + '/measured_data/pulse_shape_parameter/'
    smoothed_lo_path = cwd + '/smoothed_data/light_output/'
    smoothed_psp_path = cwd + '/smoothed_data/pulse_shape_parameter/' 
    files = glob.glob(smoothed_lo_path + '*')

    # plot
    if plot_3d:
        print('\nPlotting with mplot3d')
        plot_3D(files)
        plt.show()

    if plot_lambert_projection:
        print('\nPlotting Lambert azimuthal equal area projection')
        lambert_projection_plots(files)
        plt.show()  

 


    

