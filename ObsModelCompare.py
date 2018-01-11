
# coding: utf-8

# In[8]:


# importing packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.signal as sp
import seaborn as sns
pd.set_option('display.max_colwidth', -1)

# user friendly for selecting launch
launch = input('Enter launch you are interested in (1-8): ')
file = pd.ExcelFile('C:/Users/Michael/Documents/EclipseBalloons/LAUNCH' + str(launch) + '.xlsx',
                   sheetname='LAUNCH' + str(launch))
file.sheet_names
data = file.parse('LAUNCH' + str(launch))
data = data.drop([0,1])
data = data.convert_objects(convert_numeric=True)

# derive wind direction

data['u'] = -1 * np.absolute(data['WSpeed']) * np.sin(np.pi/180 * data['WDirn'])
data['v'] = -1 * np.absolute(data['WSpeed']) * np.cos(np.pi/180 * data['WDirn'])
data['ascent'] = data['Alt_AGL'].shift() / data['Time'].shift()

# filter data to remove sway of balloon and to make less noisy overall
#data['Alt_AGL'] = sp.medfilt(data['Alt_AGL'], 141)
data['Temp'] = sp.medfilt(data['Temp'],9)
data['DP'] = sp.medfilt(data['DP'],9)

# extract WRF coords

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns
import xarray as xr
from matplotlib.cm import get_cmap
from wrf import to_np, getvar, latlon_coords, CoordPair, xy_to_ll, ll_to_xy, interp1d, to_np
# Get Model Sims NetCDF files
os.chdir("X:/WRF/AUG2022/")
file1 = "wrfout_d01_2017-08-21_18%3A45%3A00"
ncfile1 = Dataset(file1)

lat = 34.07
lon = -81.59
# Convert from lat/lon to x and y
x_y = ll_to_xy(ncfile1, lat, lon)
x = int(x_y[0])
y = int(x_y[1])

# Get variables from control sim
z = to_np(getvar(ncfile1, "z", units="m"))[:,y,x]
T1 = to_np(getvar(ncfile1, "tc"))[:,y,x]
Td1 = to_np(getvar(ncfile1, "td")[:,y,x])
pressure = to_np(getvar(ncfile1, "pressure")[:,y,x])
#print(len(pressure))
#print(len(z))
#print(len(T1))
#print(len(Td1))

# create the dataframes

d = {'temp_observations' : pd.Series(data['Temp']),
     'dew_observations' : pd.Series(data['DP']),
     'altitude' : pd.Series(data['Alt_AGL']),
     'press' : pd.Series(data['Press'])}
df1 = pd.DataFrame(d)

df1 = df1[df1['press'] >= 100]
df1 = df1.astype(int)
results = df1.groupby(df1['press']).mean().temp_observations

e = {'temp_model' : pd.Series(T1),
      'dew_model' : pd.Series(Td1),
      'altitude' : pd.Series(z),
      'press' : pd.Series(pressure)}
df2 = pd.DataFrame(e)
df2 = df2.astype(int)
result =  pd.merge(df1, df2, on='press', indicator=True)
result.set_index('press', inplace=True)
result = result[result['_merge'] == 'both']
result = result.groupby('press').mean()

result = result.reset_index()

plt.figure(figsize=(10,10))
sns.set_style("whitegrid", {"axes.facecolor": "1"})
sns.set_context("talk")
plt.plot(result['temp_model'], result['press'], label='WRF-Temperature', color='red', linestyle=':', linewidth=5)
plt.plot(result['dew_model'], result['press'], label='WRF-Dewpoint', color='green', linestyle=':', linewidth=5)
plt.plot(result['temp_observations'], result['press'],  label='Temperature', color='red')
plt.plot(result['dew_observations'], result['press'],  label='Dewpoint', color='green')

# just a normal plot of temperature/dewpoint with height

plt.xlabel('Degrees (C)', fontsize=25)
plt.ylabel('Pressure (mb)', fontsize=25)
plt.title('Launch ' + str(launch) + ' - ' + file1[22:24] + ':' + file1[27:29] + 'Z - 21 August 2017', fontsize=20)
plt.legend(loc='best',prop={'size':17})
plt.gca().invert_yaxis()
plt.show()

