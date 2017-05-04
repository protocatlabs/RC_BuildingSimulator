"""
=========================================
Tool to Evaluate Radiation incident on a surface of a set angle
=========================================
"""

import numpy as np
import pandas as pd
import os
import sys
import math
import datetime
import matplotlib.pyplot as plt



__authors__ = "Prageeth Jayathissa"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["pysolar"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prageeth Jayathissa"
__email__ = "jayathissa@arch.ethz.ch"
__status__ = "BETA"


"""
Workflow

initialise a location with weatherfile
	calculate sun positions based on location for the whole year

initialise a window class for people to create windows

initalise a PV panel class to create PV modules

	

"""


class Location(object):
	"""docstring for Location"""
	def __init__(self, epwfile_path):
		super(Location, self).__init__()

		#Set EPW Labels and import epw file
		epw_labels = ['year', 'month', 'day', 'hour', 'minute', 'datasource', 'drybulb_C', 'dewpoint_C', 'relhum_percent',
					   'atmos_Pa', 'exthorrad_Whm2', 'extdirrad_Whm2', 'horirsky_Whm2', 'glohorrad_Whm2',
					   'dirnorrad_Whm2', 'difhorrad_Whm2', 'glohorillum_lux', 'dirnorillum_lux','difhorillum_lux',
					   'zenlum_lux', 'winddir_deg', 'windspd_ms', 'totskycvr_tenths', 'opaqskycvr_tenths', 'visibility_km',
					   'ceiling_hgt_m', 'presweathobs', 'presweathcodes', 'precip_wtr_mm', 'aerosol_opt_thousandths',
					   'snowdepth_cm', 'days_last_snow', 'Albedo', 'liq_precip_depth_mm', 'liq_precip_rate_Hour']

		#Import EPW file
		self.weather_data = pd.read_csv(epwfile_path, skiprows=8, header=None, names=epw_labels).drop('datasource', axis=1)



	def calcSunPosition(self,latitude_deg, longitude_deg, year, HOY):
		latitude_rad = math.radians(latitude_deg)
		longitude_rad = math.radians(longitude_deg)

		#Set the date in UTC based off the hour of year and the year itself
		start_of_year = datetime.datetime(year, 1, 1, 0, 0, 0, 0)
		utc_datetime = start_of_year + datetime.timedelta(hours=HOY)

		#Angular distance of the sun north or south of the earths equator
		day_of_year = utc_datetime.timetuple().tm_yday #Determine the day of the year.
		declination_rad = math.radians(23.45 * math.sin((2 * math.pi / 365.0) * (day_of_year-81))) #TODO: Change to 81

		angle_of_day = (day_of_year-81) * (2 * math.pi/364) #Adjusted Nomilisation to 2pi of the day. change to 81, 365.25

		equation_of_time = (9.87 * math.sin(2 *angle_of_day)) - (7.53 * math.cos(angle_of_day)) - (1.5 * math.sin(angle_of_day))

		solar_time = ((utc_datetime.hour * 60) + utc_datetime.minute + (4 * longitude_deg) + equation_of_time)/60.0

		#Angle between the local longitude and longitude where the sun is at highers altitude
		hour_angle_rad = math.radians(15 * (12 - solar_time))

		#Alititude Position of the Sun in Radians
		altitude_rad = math.asin(math.cos(latitude_rad) * math.cos(declination_rad) * math.cos(hour_angle_rad) + \
			math.sin(latitude_rad) * math.sin(declination_rad))
	
		#Azimuth Position fo the sun in radians	
		azimuth_rad = math.asin(math.cos(declination_rad) * math.sin(hour_angle_rad) / math.cos(altitude_rad))

		#I don't really know what this code does, it has been copied from PySolar
		if(math.cos(hour_angle_rad) >= (math.tan(declination_rad) / math.tan(latitude_rad))):
			return math.degrees(altitude_rad), math.degrees(azimuth_rad)
		else:
			return math.degrees(altitude_rad), (180 - math.degrees(azimuth_rad))


class Window(object):
	"""docstring for Window"""
	def __init__(self, azimuth_tilt, alititude_tilt = 90):
		super(Window, self).__init__()
		self.alititude_tilt_rad = math.radians(alititude_tilt)
		self.azimuth_tilt_rad = math.radians(azimuth_tilt)

	def calcIncidentSolar(self, sun_altitude, sun_azimuth, normal_direct_radiation, horizontal_diffuse_radiation):
		sun_altitude_rad = math.radians(sun_altitude)
		sun_azimuth_rad = math.radians(sun_azimuth)

		#If the sun is infront of the window surface 
		if math.cos(sun_azimuth_rad - self.azimuth_tilt_rad) > 0:
			#Proportion of the radiation incident on the window (inverse cos of the incident ray)
			acos_i = math.cos(sun_altitude_rad) * math.cos(sun_azimuth_rad - self.azimuth_tilt_rad) + \
		 	math.sin(sun_altitude_rad) * math.cos(self.alititude_tilt_rad)

			direct_solar = acos_i * normal_direct_radiation

		else:
			direct_solar = 0

		diffuse_solar = horizontal_diffuse_radiation * (1 + math.cos(self.alititude_tilt_rad))/2

		self.incident_solar = direct_solar + diffuse_solar

			
		


if __name__  ==  '__main__':
	Zurich = Location(epwfile_path=os.path.join(os.path.dirname( __file__ ),'auxillary','Zurich-Kloten_2013.epw'))

	print Zurich.calcSunPosition(latitude_deg=47.480, longitude_deg=8.536, year=2015, HOY=3708)

	Azimuth = []
	Altitude = []
	SunnyHOY=[]


	for HOY in range (8760):
		sun= Zurich.calcSunPosition(latitude_deg=47.480, longitude_deg=8.536, year=2015, HOY=HOY)
		Altitude.append(sun[0])
		Azimuth.append(sun[1])
		SunnyHOY.append(HOY+1)
		
		

	sunPosition=pd.read_csv(os.path.join(os.path.dirname( __file__ ),'auxillary','SunPosition.csv'), skiprows=1)

	transSunPos=sunPosition.transpose()
	HOY_check=transSunPos.index.tolist()
	HOY_check =  [float(ii) for ii in HOY_check]
	Azimuth_check= (180-transSunPos[1]).tolist()

	Altitude_check= transSunPos[0].tolist()

	plt.style.use('ggplot')

	plt.plot(SunnyHOY, Azimuth, HOY_check, Azimuth_check, SunnyHOY, Altitude, HOY_check, Altitude_check )
	plt.legend(['Azimuth','Azimuth Check','Altitude','Altitude_check'])

	plt.show()
