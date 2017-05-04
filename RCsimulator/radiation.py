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

		self.weather_data = pd.read_csv(epwfile_path, skiprows=8, header=None, names=epw_labels).drop('datasource', axis=1)


	def calcSunPosition(self,latitude_deg, longitude_deg, utc_datetime):
		latitude_rad = math.radians(latitude_deg)
		longitude_rad = math.radians(longitude_deg)

		#Angular distance of the sun north or south of the earths equator
		day_of_year = utc_datetime.timetuple().tm_yday #Determine the day of the year.
		declination_rad = math.radians(23.45 * math.sin((2 * math.pi / 365.0) * (day_of_year-81))) #TODO: Change to 81

		angle_of_day = (day_of_year-81) * (2 * math.pi/364) #Adjusted Nomilisation to 2pi of the day. change to 81, 365.25

		equation_of_time = (9.87 * math.sin(2 *angle_of_day)) - (7.53 * math.cos(angle_of_day)) - (1.5 * math.sin(angle_of_day))

		solar_time = ((utc_datetime.hour * 60) + utc_datetime.minute + (4 * longitude_deg) + equation_of_time)/60.0

		#Angle between the local longitude and longitude where the sun is at highers altitude
		hour_angle_rad = math.radians(15 * (12 - solar_time))

		altitude_rad = math.asin(math.cos(latitude_rad) * math.cos(declination_rad) * math.cos(hour_angle_rad) + math.sin(latitude_rad) * math.sin(declination_rad))
		
		azimuth_rad = math.asin(math.cos(declination_rad) * math.sin(hour_angle_rad) / math.cos(altitude_rad))

		# print 'day', day_of_year
		# print 'declination_rad', declination_rad
		# print 'equation_of_time', equation_of_time
		# print 'angle_of_day', angle_of_day
		
		# print 'solar_time', solar_time
		# print 'hour_angle_rad', hour_angle_rad
		# print utc_datetime.minute

		return math.degrees(altitude_rad), 180-math.degrees(azimuth_rad)

		# if(math.cos(hour_angle_rad) >= (math.tan(declination_rad) / math.tan(latitude_rad))):
		# 	return math.degrees(altitude_rad), math.degrees(azimuth_rad)
		# else:
		# 	return math.degrees(altitude_rad), (180 - math.degrees(azimuth_rad))

if __name__  ==  '__main__':
    Zurich = Location(epwfile_path=os.path.join(os.path.dirname( __file__ ),'auxillary','Zurich-Kloten_2013.epw'))
    azimuth= Zurich.calcSunPosition(47.480,8.536,datetime.datetime(2015, 1, 1, 9, 0, 0, 0))
    print azimuth



