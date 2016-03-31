
"""
===========================
Script for Handling Inputs (Weather files etc)
===========================
File history and credits:
Prageeth Jayathissa
Mario Frei
Jeremias Schmidli
Amr Elesawy 
"""


import numpy as np
import math
import csv
import pandas as pd




#x=pd.read_csv(epw_name)

#Extract DryBulb Temperature from the Weather File



def read_EWP(epw_name='Zurich-Kloten_2013.epw'):
	#Should be done later with Pandas, but for some reason I'ts not working

	
	To=[] #Open empty matrix for storing dry bulb temperature values
	glbRad=[] #Global radiation values
	with open(epw_name, 'rb') as csvfile:
		weatherfile = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in weatherfile:
			if row[0].isdigit():
				To.append(row[6])
				glbRad.append(row[15])
	return To,glbRad

def read_transmittedR(my_filename='radiation_combination2.csv'):
	incRad=[] #Incident radiation through the window
	with open(my_filename, 'rb') as csvfile:
		radvalues= csvfile.read().split(',')

		#Some stupid script to convert the monthly data into yearly data
		#Its  however incorrect as it adds a day to february and subtracts one from August for simplification
		for ii in range(12):
		
			newlist=radvalues[24*ii:24*(ii+1)]
			if ii%2==0:
				incRad+=newlist*31
			else:
				if ii==1:
					incRad += newlist*29
				else:
					incRad += newlist*30
		incRad=np.asarray(incRad)	
		incRad=incRad.astype(np.float)
		incRad=incRad/30 #Approximately convert it back from the monthly average to a daily average

		return incRad







	return radvalues


read_transmittedR()