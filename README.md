# stilbene_scintillation_anisotropy_data
Measured and smoothed light output and pulse shape parameter anisotropy for recoil proton energies between 0.56 and 10 MeV.

## Text files    
The measured and smoothed data are listed in ascii files. 

The text files are composed of 6 or 8 columns:
- Column 1 lists the light ouptput (MeVee) or pulse shape parameter (unitless)
- Column 2 lists the light ouput or pulse shape parameter uncertainty
- Columns 3 - 5 list the x, y, and z coordinates, respectively
- Column 6 lists the recoil proton energy
- Column 7 (measured data only) lists the recoil proton energy uncertainty
- Column 8 (measured data only) lists the crystal used for the measurement

## Viewing data
view_data.py is provided to plot the data w.r.t. the crystal axes. 
It contains a function to plot the data in 3D and a function to plot the data using Lambert azimuthal equation area projection (including the light output uncertainties).

### Requirments
view_data.py was tested on Python 3.7
Required packages:
- glob
- pandas
- numpy
- scipy
- matplotlib
- mpl_toolkits
- os

