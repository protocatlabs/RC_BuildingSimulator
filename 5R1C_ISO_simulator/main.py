"""
=========================================
Main file to calculate the building loads
EN-13970
=========================================
"""

import numpy as np
from buildingPhysics import Building #Importing Building Class

__author__ = "Prageeth Jayathissa"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Gabriel Happle"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prageeth Jayathissa"
__email__ = "jayathissa@arch.ethz.ch"
__status__ = "Production"



theta_e=10
theta_m_prev=22

#Internal heat gains, in Watts
phi_int=10

#Solar heat gains after transmitting through the winow, in Watts
phi_sol=2000

#Illuminance after transmitting through the window 
ill=44000 #Lumens

#Occupancy for the timestep [people/hour/square_meter]
occupancy = 0.1

#Set Building Parameters
Office=Building(Fenst_A=13.5 ,
		Room_Depth=7.0 ,
		Room_Width=4.9 ,
		Room_Height=3.1 ,
		glass_solar_transmitance=0.687 ,
		glass_light_transmitance=0.744 ,
		lighting_load=11.7 ,
		lighting_control = 300,
		Lighting_Utilisation_Factor=0.45,
		Lighting_MaintenanceFactor=0.9,
		U_em = 0.2 , 
		U_w = 1.1,
		ACH_vent=1.5,
		ACH_infl=0.5,
		ventilation_efficiency=.6,
		c_m_A_f = 165000,
		theta_int_h_set = 20.0,
		theta_int_c_set = 26.0,
		phi_c_max_A_f=-20.0,
		phi_h_max_A_f=20.0,
		heatingSystem=DirectHeater,
		coolingSystem=DirectCooler,
		heatingEfficiency=1,
		coolingEfficiency=1,

		)

Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
Office.solve_building_lighting(ill, occupancy)


print Office.theta_m

print Office.lighting_demand


# print 'phi_ia=', Office.phi_ia
# print 'phi_m=', Office.phi_m
# print 'phi_st=',Office.phi_st

print Office.phi_hc_nd_ac

Office.theta_int_h_set = 20.0

Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)

print Office.theta_m

#print Office.has_heating_demand

# print Office.phi_m_tot