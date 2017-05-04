"""
=========================================
Main file to calculate the building loads
EN-13970
=========================================
"""
__author__ = "Prageeth Jayathissa"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Gabriel Happle"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prageeth Jayathissa"
__email__ = "jayathissa@arch.ethz.ch"
__status__ = "Production"


import sys
import os

#Set root folder one level up, just for this example
mainPath=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
sys.path.insert(0, mainPath)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from buildingPhysics import Building #Importing Building Class
from auxillary import epwReader
from auxillary import sunPositionReader

matplotlib.style.use('ggplot')


ElectricityOut = []
HeatingDemand = []      #Energy required by the zone
HeatingEnergy = []       #Energy required by the supply system to provide HeatingDemand
CoolingDemand = []      #Energy surplus of the zone
CoolingEnergy = []       #Energy required by the supply system to get rid of CoolingDemand
IndoorAir = []
OutsideTemp = []
SolarGains=[]
COP=[]




gain_per_person = 100 #W per person
appliance_gains= 14 #W per sqm
max_occupancy=3.0

#Initialise an instance of the building. Empty brackets take on the default parameters. See buildingPhysics.py to see the default values
Office=Building()

#Read Weather Data
weatherData=epwReader.epwReader(os.path.join(mainPath,'auxillary','Zurich-Kloten_2013.epw'))

# print weatherData['drybulb_C']
# print weatherData['glohorrad_Whm2']

#Read Sunposition and Extract Azimuth and Alitutude Angles
sunPosition=pd.read_csv(os.path.join(mainPath,'auxillary','SunPosition.csv'), skiprows=1)

altitude=sunPosition.loc[0]
azimuth=180-sunPosition.loc[1]


#Read Occupancy Profile
occupancyProfile=pd.read_csv(os.path.join(mainPath,'auxillary','schedules_el_OFFICE.csv'))

T_m_prev=20

for hour in range(8760):
	#Occupancy for the time step
	occupancy = occupancyProfile.loc[hour,'People'] * max_occupancy
	#Gains from occupancy and appliances
	internal_gains = occupancy*gain_per_person + appliance_gains*Office.floor_area

	#Outdoor Temperature
	T_out = weatherData['drybulb_C'][hour]

	if str(float(hour)) in altitude.index:
		#if solar gains land in front of the south window. Assume that window is fully shaded from the back by the building
		if altitude[str(float(hour))]<90.0 and azimuth[str(float(hour))]>-90 and azimuth[str(float(hour))]<90:
			dir_solar_gains = weatherData['dirnorrad_Whm2'][hour] * np.cos(altitude[str(float(hour))]*np.pi/180.0) * np.cos(azimuth[str(float(hour))]*np.pi/180.0)
		else:
			dir_solar_gains = 0

		diffuse_solar_gains = weatherData['difhorrad_Whm2'][hour] / 2.0 

		if hour == 3994:
			print dir_solar_gains + diffuse_solar_gains

		solar_gains=(dir_solar_gains + diffuse_solar_gains) * Office.window_area


	else:
		#Sun is below the horizon (night time)
		solar_gains=0




	Office.solve_building_energy(internal_gains=internal_gains, solar_gains=solar_gains,T_out=T_out, T_m_prev=T_m_prev)

	T_m_prev=Office.T_m_next


	HeatingDemand.append(Office.heatingDemand)
	HeatingEnergy.append(Office.heatingEnergy)
	CoolingDemand.append(Office.coolingDemand)
	CoolingEnergy.append(Office.coolingEnergy)
	ElectricityOut.append(Office.electricityOut)
	IndoorAir.append(Office.T_air)
	OutsideTemp.append(T_out)
	SolarGains.append(solar_gains)
	COP.append(Office.COP)

annualResults=pd.DataFrame({
	'HeatingDemand' : HeatingDemand,
	'HeatingEnergy' : HeatingEnergy, 
	'CoolingDemand' : CoolingDemand, 
	'CoolingEnergy' : CoolingEnergy,
	'IndoorAir' : IndoorAir,
	'OutsideTemp' :  OutsideTemp,
	'SolarGains': SolarGains,
	'COP': COP
	})


annualResults[['HeatingEnergy','CoolingEnergy']].plot()
plt.show()
