#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 13:16:36 2023

@author: elliehojeily
"""
import pandas as pd
import os
import matplotlib.pyplot as plt
from statistics import mean, median, stdev


path_2_proto2='/Volumes/data-polar/aq/nyserda/proto2/corrected/csv/'
proto2_filepaths=[]
for file in sorted(os.listdir(path_2_proto2)):
    proto2_filepaths.append(path_2_proto2+file)

proto2_read = (pd.read_csv(f) for f in proto2_filepaths)
proto2_raw_dat = pd.concat(proto2_read)
proto2_raw_dat = proto2_raw_dat.drop(['Unnamed: 0', 'datetimestamp','unix_time'],1)

#proto2_raw_dat.to_csv('/Volumes/data-polar/home/ehojeily/proto2_data/raw_proto2_csv')

times=pd.to_datetime(proto2_raw_dat['datefield'],format='%Y-%m-%d %H:%M:%S')

proto2_raw_dat=proto2_raw_dat.set_index(times)
proto2_raw_dat.index.names=['date']

''' DESPIKING '''
variables_to_despike = proto2_raw_dat.columns.values.tolist() 
variables_to_despike.remove('datefield')
variables_to_despike = ['pm25_std_ugm3']


#Static variables here
thresholdHigh = 100 #Enter threshold for high here
thresholdLow = 0 #Enter low threshold here
nstds = 1 #Enter deviance from std -- a default value of 1 equals 100% of std
#columnToAnalyze = 'pm25_env_ugm3' #Enter variable to analyze
    
for variable in variables_to_despike:
    
    proto2_raw_dat.reset_index(drop=True, inplace=True)

    proto2_raw_dat[variable] = pd.to_numeric(proto2_raw_dat[variable]) #<---
    
    
    minPrior = min(proto2_raw_dat[variable])
    maxPrior = max(proto2_raw_dat[variable])
    medianPrior = median(proto2_raw_dat[variable])
    meanPrior = mean(proto2_raw_dat[variable])
    stdPrior = stdev(proto2_raw_dat[variable])
    stdevRange = 2

    dataFrameConcatPrior = proto2_raw_dat


    nullVals = proto2_raw_dat[variable].isnull() #Get logical columns if NaN values are present
    isLowerThanThreshold = proto2_raw_dat[variable] < thresholdLow
    isGreaterThanThreshold = proto2_raw_dat[variable] > thresholdHigh

    spikedVals = nullVals | isLowerThanThreshold | isGreaterThanThreshold

    markers_on = [i for i, x in enumerate(spikedVals) if x]
    
    runningTotal=len(proto2_raw_dat)

    dataPostSpiked = proto2_raw_dat.drop(labels=markers_on, axis=0,inplace=False) #Delete rows of spiked data
    stdPost = stdev(dataPostSpiked[variable])
    minPost = min(dataPostSpiked[variable])
    maxPost = max(dataPostSpiked[variable])
    medianPost = median(dataPostSpiked[variable])
    meanPost = mean(dataPostSpiked[variable])

    outsideOfStdev1 = dataPostSpiked[variable] > stdPost 
    outsideOfStdev2 = dataPostSpiked[variable] < -stdPost
    outsideOfStdev = outsideOfStdev1 | outsideOfStdev2

    #markers_on = [i for i, x in enumerate(outsideOfStdev) if x]
    stdPost = stdev(dataPostSpiked[variable])

    data = [['Min',minPrior,minPost],['Max',maxPrior,maxPost],['Median',medianPrior,medianPost],['Mean',meanPrior,meanPost],['Std',stdPrior,stdPost]] #For stats dataframe
    
plt.figure()
plt.plot(proto2_raw_dat[variable], label='Pre-spiked', color='black')
plt.plot(dataPostSpiked[variable], label='Post-spiked', color='red')

#plt.plot(proto2_raw_dat[variable]-dataPostSpiked[variable], label='Change')
plt.legend()

    
    
    
despiked_dat = dataPostSpiked.to_csv('/Volumes/data-polar/home/ehojeily/proto2_data/despiked_proto2_ext.csv')
    
    
    