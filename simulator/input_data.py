
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
import matplotlib.pyplot as plt


#Constants
human_heat_emission=0.12 #[kWh] heat emitted by a human body per hour. Source: HVAC Engineers Handbook, F. Porges
floor_area=30 #[m^2] floor area



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
		Q_fenstRad=pd.DataFrame(incRad)


	return Q_fenstRad

def read_occupancy(myfilename='Occupancy_COM.csv'):
	#People: Average number of people per hour per m2
	#tintH_set: Temperature set point of the heating season, if negative then heating is disabled
	#tintC_set: Temperature set point for cooling season. Error: When does this turn on and off
	occupancy=pd.read_csv(myfilename, nrows=8760)
	#print occupancy['tintH_set'].iat[100]
	Q_human=occupancy['People']*human_heat_emission*floor_area
	return occupancy, Q_human.transpose()


Kloten_T,Kloten_R=read_EWP(epw_name='Zurich-Kloten_2013.epw')
Geneva_T,Geneva_R=read_EWP(epw_name='CHE_Geneva.067000_IWEC.epw')


plt.plot(range(0, int(8760)),Kloten_R, 'b', range(0, int(8760)),Geneva_R,'g')
plt.show()


