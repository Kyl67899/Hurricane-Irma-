#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 23:13:53 2020

@author: parsotak
"""
#Data retrieved from: European Centre for Medium-Range Weather Forecasts, 2009: 
#ERA-Interim Project. Research Data Archive at the National Center for Atmospheric Research, 
#Computational and Information Systems Laboratory, Boulder, CO. 
#[Available online at https://doi.org/10.5065/D6CR5RD9.] Accessed 03 25 20.
#Creating Hurricane Irma (2017-08-30 00:00 - 2017-09-16 18:00) life cycle

# import datasets

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap

#To display data file variables

#f.variables

#read in the netCDF files:

#read in the surface analysis times netCDF files

sfcTimes = ['2017083000', '2017083006', '2017083012','2017083018',
              '2017083100','2017083106','2017083112','2017083118',
              '2017090100','2017090106','2017090112','2017090118',
              '2017090200','2017090206','2017090212','2017090218',
              '2017090300','2017090306','2017090312','2017090318',
              '2017090400','2017090406','2017090412','2017090418',
              '2017090500','2017090506','2017090512','2017090518',
              '2017090600','2017090606','2017090612','2017090618',
              '2017090700','2017090706','2017090712','2017090718',
              '2017090800','2017090806','2017090812','2017090818',
              '2017090900','2017090906','2017090912','2017090918',
              '2017091000','2017091006','2017091012','2017091018',
              '2017091100','2017091106','2017091112','2017091118',
              '2017091200','2017091206','2017091212','2017091218',
              '2017091300','2017091306','2017091312','2017091318',
              '2017091400','2017091406','2017091412','2017091418',
              '2017091500','2017091506','2017091512','2017091518',
              '2017091600','2017091606','2017091612','2017091618']


#for loop for time reading in each files in sfc SST and MSL

for i in sfcTimes:
    
    #print(infiles)
    
    #Define input file
    
    #sfc analysis netCDF files

    infile = '/home/students/parsotak/project-data/data_with_uv/ei.oper.an.sfc.regn128sc.'+ i + '.parsotan416050.nc'

    #Read in the file

    f = Dataset(infile, 'r')
    
    #Read in Mean sea level (surface) convert from Pa to mb

    sfc_Heights = f['MSL_GDS4_SFC'][0, :, :] / 100.
    
    #Read in Temperature (K)

    sfc_Temps = f['SSTK_GDS4_SFC'][0, :, :]
    
    #Convert Kelvins to Celsius

    sfcTemps_C = sfc_Temps - 273.15 
    
    #Read in cloud cover

    cloud_cv = f['TCC_GDS4_SFC'][0, :, :]

    #Read in U velocity (m/s)

    wind_u1 = f['10U_GDS4_SFC'][:]

    #Read in V velocity (m/s)

    wind_v1 = f['10U_GDS4_SFC'][:]

    #Read in wind u (x) and v (y) (m/s) to knots

    wind_u = f['10U_GDS4_SFC'][0, :, :] * 1.94384

    wind_v = f['10V_GDS4_SFC'][0, :, :] * 1.94384 
    
    #define U and v for wind barbs
    #and increase the data space read in

    Unew = wind_u[0::10, 0::10]

    Vnew = wind_v[0::10, 0::10]

    #Read in lat and long

    lats = f['g4_lat_1'][:]

    lons = f['g4_lon_2'][:]

    print(lats.shape)

    print(lons.shape)
    
    #from 1D to 2D to plot to a map

    lon2d, lat2d = np.meshgrid(lons, lats)

    #Define a figure

    fig = plt.figure(figsize = (12,10))

    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    
    #Define basemap

    m = Basemap(llcrnrlon = 240., llcrnrlat = 0., urcrnrlon = 360., urcrnrlat = 50., resolution = 'l', projection = 'merc', ax = ax)

    xi, yi = m(lon2d, lat2d)

    m.drawparallels(np.arange(-80., 81, 10.), labels = [1, 0, 0, 0], fontsize = 12)

    m.drawmeridians(np.arange(0., 359., 30.), labels = [0, 0 ,0, 1], fontsize = 14)

    m.drawcoastlines()

    m.drawstates()

    m.drawcountries()
    
    #Define coordinates for wind barbs

    Xnew = xi[0::10, 0::10]

    Ynew = yi[0::10, 0::10]

    #MSL height range

    range_mslHgts = np.arange(950, 1050, 3)

    #Sfc temps range

    range_sfcTemps = np.arange(-10, 50, 5)
    
    #Add contour fills MSL values

    contour_MSLh = m.contour(xi, yi, sfc_Heights, range_mslHgts, colors = 'Black')

    clab = plt.clabel(contour_MSLh, inline = True, fontsize = 14, fmt='%1.0f')

    #Add contour fills for geo heights values 500 mb

    contour_sfcTemps = m.contourf(xi, yi, sfcTemps_C, cmap = 'RdBu')
    
    #Add colorbar for SST temps 

    cbar = plt.colorbar(contour_sfcTemps, orientation = 'horizontal', pad = 0.05, shrink = 0.75, ax = ax)

    #wind barbs and time for each plot to show up in the title and the animation of each plot into one.
    # plot wind barbs over map

    ax.barbs(Xnew, Ynew, Unew, Vnew)
    
    #increase size of labels 

    cbar.ax.tick_params(labelsize = 14)

    cbar.set_label('Sea Surface temperature ($^{o}$C)', fontsize = 14)

    #add a title 

    ax.set_title("Hurricane Irma's Mean Sea Level Pressure (mb), Sea Surface Temperature $^{o}$C and wind barbs at the surface (kts) from: " + i , fontsize = 12)

    #save png

    plt.savefig('parsotak_Hurricane_Irma_MSL_SST' + i + '.png')
    
    #show each plot at each time
    
    plt.show()
   
#for loop for time reading in each files in upperlevel 400 500 700 mb and relative humidity
    
for i in sfcTimes:

    #Define input file
    
    #read in the 400 500 700 upperlevel analysis netCDF files

    infile1 = '/home/students/parsotak/project-data/data_with_400_500_700mb/ei.oper.an.pl.regn128sc.'+ i +'.parsotan416040.nc'
    
    f1 = Dataset(infile1, 'r')
    
    #read in the 400 500 700 upperlevel analysis netCDF files
    
    infile2 = '/home/students/parsotak/project-data/data_with_400_500_700mb/ei.oper.an.pl.regn128uv.'+ i +'.parsotan416040.nc'
    
    upperlvl1 = Dataset(infile2, 'r')
    
    #Read in 400 mbar upper lvl from m^2 / s^2 to m
    
    upper_lvl1400mb = f1['Z_GDS4_ISBL'][0, 0, :, :] / 9.8
    
    #Read in 500mb upper lvl from m^2 / s^2 to m
    
    upper_lvl1500mb = f1['Z_GDS4_ISBL'][0, 1, :, :] / 9.8
    
    #Read in 700 mbar upper lvl from m^2 / s^2 to m
    
    upper_lvl1700mb = f1['Z_GDS4_ISBL'][0, 2, :, :] / 9.8

    #Read in Relative Humidity upper level

    relHum_upper = f1['R_GDS4_ISBL'][0, :, :, :]
    
    #find the mean value of the relative Humidity
    
    relHum_upperavg = np.mean(relHum_upper, axis = 0)
    
    #Read in U velocity (m/s)

    wind_u1 = upperlvl1['U_GDS4_ISBL'][:]

    #Read in V velocity (m/s)

    wind_v1 = upperlvl1['V_GDS4_ISBL'][:]

    #Read in wind u (x) and v (y) (m/s) to knots

    wind_ulvl = upperlvl1['U_GDS4_ISBL'][0, 1, :, :] * 1.94384

    wind_vlvl = upperlvl1['V_GDS4_ISBL'][0, 1, :, :] * 1.94384
    
    #define U and v for wind barbs
    #and increase the data space read in

    Unew1 = wind_ulvl[0::5, 0::5]

    Vnew1 = wind_vlvl[0::5, 0::5]
    
    #Read in lat and long

    lats = f1['g4_lat_2'][:]

    lons = f1['g4_lon_3'][:]

    print(lats.shape)

    print(lons.shape)
    
    #from 1D to 2D to plot to a map

    lon2d, lat2d = np.meshgrid(lons, lats)

    #Define a figure

    fig = plt.figure(figsize = (12,10))

    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    
    #Define basemap

    m = Basemap(llcrnrlon = 240., llcrnrlat = 0., urcrnrlon = 360., urcrnrlat = 50., resolution = 'l', projection = 'merc', ax = ax)

    xi, yi = m(lon2d, lat2d)

    m.drawparallels(np.arange(-80., 81, 10.), labels = [1, 0, 0, 0], fontsize = 12)

    m.drawmeridians(np.arange(0., 359., 30.), labels = [0, 0 ,0, 1], fontsize = 14)

    m.drawcoastlines()

    m.drawstates()

    m.drawcountries()
    
    #Define coordinates for wind barbs

    Xnew1 = xi[0::5, 0::5]

    Ynew1 = yi[0::5, 0::5]

    #MSL height range

    range_isolvl = np.arange(4770, 5150, 5)

    #Sfc Rel. Humidity range

    range_RelHum = np.arange(0, 105, 5)
    
    #Add contour fills for geo heights values 400, 500, 700 mb

    contour_RelHum = m.contourf(xi, yi, relHum_upperavg, range_RelHum, cmap = 'RdBu')

    #Add contour fills MSL values

    contour_isolvl = m.contour(xi, yi, upper_lvl1500mb, colors = 'Black')

    clab = plt.clabel(contour_isolvl, inline = True, fontsize = 14, fmt='%1.0f')

    #Add colorbar for Rel Hum. temps 

    cbar = plt.colorbar(contour_RelHum, orientation = 'horizontal', pad = 0.05, shrink = 0.75, ax = ax)

    # plot wind barbs over map

    ax.barbs(Xnew1, Ynew1, Unew1, Vnew1)
    
    #increase size of labels 

    cbar.ax.tick_params(labelsize = 14)

    cbar.set_label('400-700 mb height Relative Humidity average (%)', fontsize = 14)
    
    #add a title 

    ax.set_title("Hurricane Irma's Relative Humidity (%), 500 (mb) upper level pressure and upper level wind barbs (kts) from: " + i , fontsize = 12)

    #save png of each plot to create gif animations

    plt.savefig('parsotak_Hurricane_Irma_Rel_hum' + i + '.png')
   
    plt.show()
 
    
    
   
##for loop for time reading in each files in sfc cloud cover
#
#for i in sfcTimes:
#    
#    #print(infiles)
#    
#    #Define input file
#    
#    #sfc analysis netCDF files
#
#    infile = '/home/students/parsotak/project-data/data_with_uv/ei.oper.an.sfc.regn128sc.'+ i + '.parsotan416050.nc'
#
#    #Read in the file
#
#    f3 = Dataset(infile, 'r')
#    
#    #Read in Mean sea level (surface) convert from Pa to mb
#
#    sfc_Heights = f3['MSL_GDS4_SFC'][0, :, :] / 100.
#    
#    #Read in Temperature (K)
#
#    sfc_Temps = f3['SSTK_GDS4_SFC'][0, :, :]
#    
#    #Convert Kelvins to Celsius
#
#    sfcTemps_C = 273.15 - sfc_Temps
#    
#    #Read in cloud cover
#
#    cloud_cv = f3['TCC_GDS4_SFC'][0, :, :]
#
#    #Read in U velocity (m/s)
#
#    wind_u1 = f3['10U_GDS4_SFC'][:]
#
#    #Read in V velocity (m/s)
#
#    wind_v1 = f3['10U_GDS4_SFC'][:]
#
#    #Read in wind u (x) and v (y) (m/s) to knots
#
#    wind_u = f3['10U_GDS4_SFC'][0, :, :] * 1.94384
#
#    wind_v = f3['10V_GDS4_SFC'][0, :, :] * 1.94384 
#    
#    #define U and v for wind barbs
#    #and increase the data space read in
#
#    Unew = wind_u[0::10, 0::10]
#
#    Vnew = wind_v[0::10, 0::10]
#
#    #Read in lat and long
#
#    lats = f3['g4_lat_1'][:]
#
#    lons = f3['g4_lon_2'][:]
#
#    print(lats.shape)
#
#    print(lons.shape)
#    
#    #from 1D to 2D to plot to a map
#
#    lon2d, lat2d = np.meshgrid(lons, lats)
#
#    #Define a figure
#
#    fig = plt.figure(figsize = (12,10))
#
#    ax = fig.add_axes([0.1,0.1,0.8,0.8])
#    
#    #Define basemap
#
#    m = Basemap(llcrnrlon = 240., llcrnrlat = 0., urcrnrlon = 360., urcrnrlat = 50., resolution = 'l', projection = 'merc', ax = ax)
#
#    xi, yi = m(lon2d, lat2d)
#
#    m.drawparallels(np.arange(-80., 81, 10.), labels = [1, 0, 0, 0], fontsize = 12)
#
#    m.drawmeridians(np.arange(0., 359., 30.), labels = [0, 0 ,0, 1], fontsize = 14)
#
#    m.drawcoastlines()
#
#    m.drawstates()
#
#    m.drawcountries()
#    
#    #Define coordinates for wind barbs
#
#    Xnew = xi[0::10, 0::10]
#
#    Ynew = yi[0::10, 0::10]
#
#    #MSL height range
#
#    range_mslHgts = np.arange(950, 1050, 3)
#
#    #Sfc temps range
#
#    range_sfccldcv = np.arange(0, 10, 2)
#    
#    #Add contour fills MSL values
#
#    contour_MSLh = m.contour(xi, yi, sfc_Heights, range_mslHgts, colors = 'Black')
#
#    clab = plt.clabel(contour_MSLh, inline = True, fontsize = 14, fmt='%1.0f')
#
#    #Add contour fills for cloud cover
#
#    contour_sfccldcv = m.contourf(xi, yi, cloud_cv, cmaps = 'rainbows')
#    
#    #Add colorbar for SST temps 
#
#    cbar = plt.colorbar(contour_sfccldcv, orientation = 'horizontal', pad = 0.05, shrink = 0.75, ax = ax)
#
#    #wind barbs and time for each plot to show up in the title and the animation of each plot into one.
# 
#    ## plot wind barbs over map
#
#    ax.barbs(Xnew, Ynew, Unew, Vnew)
#    
#    #increase size of labels 
#
#    cbar.ax.tick_params(labelsize = 14)
#
#    cbar.set_label('Cloud Cover for Hurricane Irma', fontsize = 14)
#
#    #add a title 
#
#    ax.set_title("Hurricane Irma's Mean Sea Level Pressure (mb), Cloud Cover and wind barbs at the surface (kts) from: " + i , fontsize = 12)
#    
#    #save png
#
#    plt.savefig("parsotak_Hurricane_Irma_MSL_SST.png")
#
#    plt.show()
