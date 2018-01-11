
# coding: utf-8

# In[1]:


# SOME STUPID DEPENDENCIES
import matplotlib
#matplotlib.use("macosx")
matplotlib.rcParams['figure.dpi'] = 240
#matplotlib.use('TkAgg')
# the essentials that should allow this to work but don't
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
from mpl_toolkits.basemap import Basemap
from wrf import to_np, getvar, smooth2d, get_basemap, latlon_coords
import os

# this is all path stuff
infile = 'wrfout_d01_2017-08-21_19%3A00%3A00'
#path = "X:/WRF/AUG2022/"
path = 'X:/WRF/test/'
#listing = os.listdir(path)
#print(infile)
wrf = str(infile)
filepath = path + wrf
ncfile = Dataset(filepath)
date = (wrf[11:21])
timestamp = (str(wrf[22:24]) + ':' + str(wrf[27:29]) + 'Z')

# this is the actual scrape from the wrfout file and application to plot
temp = getvar(ncfile, "temp", units='degF')
dbz = getvar(ncfile, "dbz")
dp = getvar(ncfile, "td", units='degF')
swdown = getvar(ncfile, "SWDOWN")
lowest_temp = temp[0,:,:]
lowest_td = dp[0,:,:]
lowest_swdown = swdown
#dbz = dbz[0,:,:]
#smooth_temp = smooth2d(temp, 3)
lats, lons = latlon_coords(lowest_swdown)
bm = get_basemap(lowest_swdown)
plt.figure(figsize=(15,15))
bm.drawcoastlines(linewidth=0.25)
bm.drawstates(linewidth=0.25)
bm.drawcountries(linewidth=0.25)
x, y = bm(to_np(lons), to_np(lats))
#bm.contour(x, y, to_np(lowest_td), 8, colors="black")
#a = np.linspace(50,99,100)

bm.contourf(x, y, to_np(lowest_swdown), cmap=get_cmap("gist_ncar"))
plt.title("WRF-Eclipse - Incoming Shortwave Radiation - " + timestamp + ' ' + date, size=15)
plt.colorbar(shrink=.62,)
#plt.clim(60,100)

# save figure
testfilename = timestamp + '_' + date + '.png'
#os.chdir('X:/WRF/AUG2022Figures/EclipseParameterization/')
#plt.savefig('{}.png'.format(testfilename))
#plt.savefig(str(testfilename), dpi=240)
plt.show()


