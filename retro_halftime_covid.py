#!/usr/local/bin/python3.8

import csv
from collections import OrderedDict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# explanation of variables
# deepee is how many columns to ignore
# howmany is how many days to use for calculating rate at which doubling rate is changing (linear regression-wise)
# peak is the date of the peak of the pandemic - March 17, 2020
# nashun is the country to focus on - in this case the US
deepee = 4
howmany = 21
peak = '3/17/20'
nashun = 'US'

def rethaf(dethz, whereami):
# This is the function that calculates the retroactive doubling time in days.
# That is, it calculates how many days it has been since the number of deaths
# was half of what it is now. Linear interpolation is used to estimate the fractional
# portion between whole days.
	halfzy = dethz[whereami]/2.0
	justAfter = -1
	while(True):
		justAfter += 1
		whereami -= 1
		if dethz[whereami] > halfzy:
			continue
		hd = (justAfter) + (dethz[whereami+1]-halfzy)/(dethz[whereami+1]-dethz[whereami])
		break
	return hd

# here is where we read in the data and fill the lists daytz and dethz
with open('covid_deaths.csv') as covid_csv:
	# from first line of data slice off first deepee columns - assign the rest to daytz
	daytz = covid_csv.readline().rstrip("\n").split(',')[deepee:]
	# now read the rest of the file one line at a time - until we get the one we want - then break out
	for layn in covid_csv.readlines():
		thingz = layn.rstrip('\n').split(',')
		if thingz[1] == nashun:
			# once we get to the line for US, slice off first deepee columns - assign the rest to dethz
			dethz = thingz[deepee:]
			break

# assign number of deaths at peak of pandemic to peaky
peaky = daytz.index(peak)
# create ordered dictionary death_table with dates and deaths 
# and then also create some blank ordered dictionaries for linear regression
# death_table = OrderedDict(zip(daytz, dethz))
slopzDict = OrderedDict()
halfzDict = OrderedDict()
dethzDict = OrderedDict()
intrzDict = OrderedDict()
eeepzDict = OrderedDict()
for eye in range (len(dethz)):
	dethzDict[daytz[eye]] = int(dethz[eye])
	
dayz = list(range(1,len(daytz)+1))
i_dethz = [ int(deth) for deth in dethz ]
hookle = rethaf(i_dethz, -1)
whereizit = 0
f_halvzies = []
for eye in range(len(i_dethz)-1, peaky-1, -1):
	whereizit -= 1
	dees_one = rethaf(i_dethz, whereizit)
#	print(eye, daytz[eye], dees_one) 
	f_halvzies.append(dees_one)
	halfzDict[daytz[eye]] = dees_one

###   https://realpython.com/linear-regression-in-python/
for backup in range(0,70):
	# each time through this loop we create one dataset for linear regression
	# each dataset contains howmany points
	# the first dataset ends at the last date that we have
	# each subsequent dataset moves back one day
	exx = []
	why = []
	dz = []
	for eye, daet in enumerate(daytz[-howmany-backup:len(daytz)-backup]):
		# eye ranges from 0 to howmany-1
		# daet ranges over the dates for this particular dataset
		# why - the y variable - will be the retroactive doubling time in days
		# exx - the x variable - is just the current value of eye
		# dz is just the current value of daet
		why.append(halfzDict[daet])
		exx.append(eye)
		dz.append(daet)
	# now we have our dataset - so lets do some linear regressio
	x = np.array(exx).reshape((-1,1))
	y = np.array(why)
	model = LinearRegression()
	model.fit(x,y)
	r_sq = model.score(x, y)
	# now store the slope, intercept, and ending date for this dataset (the date where it ends)
	slopzDict[dz[-1]] = model.coef_
	intrzDict[dz[-1]] = model.intercept_
	eeepzDict[dz[-1]] = daytz.index(dz[-1])

for eech in slopzDict:
        print(eeepzDict[eech], eech, dethzDict[eech], halfzDict[eech], slopzDict[eech], intrzDict[eech])
