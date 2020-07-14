#!/usr/local/bin/python3.8

import csv
from collections import OrderedDict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# deepee is a pretty crude hack - it is how many columns to ignore
deepee = 4
# another crude hack - how many days to use for calculating the rate at which the doubling rate is changing
howmany = 21
# the peack of the covid pandemic in the US - when the doubling rate was highest
peak = '3/17/20'
# the data set is global - but here we are just interested in the US
nashun = 'US'

def rethaf(dethz, whereami):
# This is the function that calculates the retroactive doubling time in days.
# That is, it calculates how many days it has been since the number of deaths
# was half of what it is now.
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

#def sloper(eenies):
	

with open('covid_deaths.csv') as covid_csv:
	# from first line of data slice off first deepee columns - assign the rest to daytz
	daytz = covid_csv.readline().rstrip("\n").split(',')[deepee:]
#	print(daytz)
	# now read the rest of the file one line at a time - 
	for layn in covid_csv.readlines():
		thingz = layn.rstrip('\n').split(',')
		if thingz[1] == nashun:
			# once we get to the line for US, slice off first deepee columns - assign the rest to dethz
			dethz = thingz[deepee:]
			break
# assign number of deaths at peak of pandemic to peaky
peaky = daytz.index(peak)
# create ordered dictionary with dates and deaths 
death_table = OrderedDict(zip(daytz, dethz))
#for dayt in death_table:
#	print(dayt, death_table[dayt])
slopzDict = OrderedDict()
halfzDict = OrderedDict()
dethzDict = OrderedDict()
intrzDict = OrderedDict()
eeepzDict = OrderedDict()
for eye in range (len(dethz)):
	dethzDict[daytz[eye]] = int(dethz[eye])
	
dayz = list(range(1,len(daytz)+1))
i_dethz = [ int(deth) for deth in dethz ]
f_dayz = [ float(dae) for dae in dayz ]
hookle = rethaf(i_dethz, -1)
#print(hookle)
whereizit = 0
f_halvzies = []
for eye in range(len(i_dethz)-1, peaky-1, -1):
	whereizit -= 1
	dees_one = rethaf(i_dethz, whereizit)
	print(eye, daytz[eye], dees_one) 
	f_halvzies.append(dees_one)
	halfzDict[daytz[eye]] = dees_one
###for eech in halfzDict:
###	print(eech, dethzDict[eech], halfzDict[eech])

#print(i_dethz)
#print(f_dayz)
###   https://realpython.com/linear-regression-in-python/
print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
backup = -1
for backup in range(0,70):
	exx = []
	why = []
	dz = []
#	print("backup = ", backup, "%%%%%%%%%%%%%%%%%%%%%%%%%%%")
#	backup += 1  
	for eye, daet in enumerate(daytz[-howmany-backup:len(daytz)-backup]):
		print("!!!!!!!!!!!!!!!!!!!!!!!", eye, daet, dethzDict[daet], halfzDict[daet])
		why.append(halfzDict[daet])
		exx.append(eye)
		dz.append(daet)
#x = np.array(f_dayz[-howmany:]).reshape((-1,1))
#y = np.array(i_dethz[-howmany:])
	x = np.array(exx).reshape((-1,1))
	y = np.array(why)
#print("Here is x:")
#print(x)
#print("And here is y:")
#print(y)
	model = LinearRegression()
	model.fit(x,y)
	r_sq = model.score(x, y)
#	print('coefficient of determination:', r_sq)
#	print(backup, dz[0], dz[-1], 'slope:', model.coef_)
	slopzDict[dz[-1]] = model.coef_
	intrzDict[dz[-1]] = model.intercept_
	eeepzDict[dz[-1]] = daytz.index(dz[-1])

for eech in slopzDict:
        print(eeepzDict[eech], eech, dethzDict[eech], halfzDict[eech], slopzDict[eech], intrzDict[eech])
