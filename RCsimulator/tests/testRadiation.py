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
import math

class TestRadiation(unittest.TestCase):



    def test_sunPosition(self):

	Zurich = Location(epwfile_path=os.path.join(mainPath,'auxillary','Zurich-Kloten_2013.epw'))

	print Zurich.calcSunPosition(latitude_deg=47.480, longitude_deg=8.536, year=2015, HOY=3708)

	Azimuth = []
	Altitude = []
	SunnyHOY=[]


	for HOY in range (8760):
		sun= Zurich.calcSunPosition(latitude_deg=47.480, longitude_deg=8.536, year=2015, HOY=HOY)

		Altitude.append(sun[0])
		Azimuth.append(sun[1])
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


if __name__  ==  '__main__':
    unittest.main()