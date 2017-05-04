import sys
import os


#Set root folder one level up, just for this example
mainPath=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
sys.path.insert(0, mainPath)

import unittest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from radiation import Location
from radiation import Window
import math

class TestRadiation(unittest.TestCase):



	def test_sunPosition(self):

		Zurich = Location(epwfile_path=os.path.join(mainPath,'auxillary','Zurich-Kloten_2013.epw'))


		Azimuth = []
		Altitude = []
		SunnyHOY=[]


		for HOY in range (8760):
			angles= Zurich.calcSunPosition(latitude_deg=47.480, longitude_deg=8.536, year=2015, HOY=HOY)

			Altitude.append(angles[0])
			Azimuth.append(angles[1])
			SunnyHOY.append(HOY+1)
			
		sunPosition=pd.read_csv(os.path.join(mainPath,'auxillary','SunPosition.csv'), skiprows=1)

		transSunPos=sunPosition.transpose()
		HOY_check=transSunPos.index.tolist()
		HOY_check =  [float(ii) for ii in HOY_check]
		Azimuth_check= (180-transSunPos[1]).tolist()

		Altitude_check= transSunPos[0].tolist()

		self.assertEqual(round(Altitude[9],1), round(Altitude_check[1],1))
		self.assertEqual(round(Azimuth[9],1), round(Azimuth_check[1],1))

		self.assertEqual(round(Altitude[3993],1), round(Altitude_check[2023],1))
		self.assertEqual(round(Azimuth[3993],1), round(Azimuth_check[2023],1))

		#Azimuth Angles go out of sync with data, however the sin and cosine must still match
		self.assertEqual(round(Altitude[4000],1), round(Altitude_check[2030],1))
		self.assertEqual(round(math.cos(math.radians(Azimuth[4000])),1), round(math.cos(math.radians(Azimuth_check[2030])),1))
		self.assertEqual(round(math.sin(math.radians(Azimuth[4000])),1), round(math.sin(math.radians(Azimuth_check[2030])),1))


	def test_windowSolarGains(self):

		HOY = 3993

		Zurich = Location(epwfile_path=os.path.join(mainPath,'auxillary','Zurich-Kloten_2013.epw'))
		Altitude, Azimuth = Zurich.calcSunPosition(latitude_deg=47.480, longitude_deg=8.536, year=2015, HOY=HOY)

		print Azimuth

		SouthWindow = Window(azimuth_tilt=0, alititude_tilt = 90) 

		SouthWindow.calcIncidentSolar(sun_altitude = Altitude, sun_azimuth = Azimuth, 
			normal_direct_radiation= Zurich.weather_data['dirnorrad_Whm2'][HOY], 
			horizontal_diffuse_radiation = Zurich.weather_data['difhorrad_Whm2'][HOY])

		print SouthWindow.incident_solar




if __name__  ==  '__main__':
	unittest.main()