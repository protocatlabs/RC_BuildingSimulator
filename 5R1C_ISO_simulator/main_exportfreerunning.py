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


import numpy as np
import pandas as pd
from buildingPhysics import Building #Importing Building Class
import input_data as f


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
		heatingEfficiency=1,
		coolingEfficiency=1,

		)

Office.theta_m_prev=20.0

#Import Data
T_out,glbRad, glbIll= f.read_EWP(epw_name='data/Zurich-Kloten_2013.epw') #C, W, lx
Q_fenstRad=f.read_transmittedR(myfilename='data/radiation_Building_Zh.csv') #kWh/h
occupancy, Q_human=f.read_occupancy(myfilename='data/Occupancy_COM.csv') #people/m2/h, kWh/h
Ill_Eq= f.Equate_Ill(epw_name='data/Zurich-Kloten_2013.epw') #Equation coefficients for linear polynomial

occupancy = occupancy.People


#Calculate Illuminance in the room. 
fenstIll=Q_fenstRad*1000*Ill_Eq[0] #Lumens.  Note that the constant has been ignored because it should be 0
TransIll=fenstIll*Office.glass_light_transmitance
Lux=TransIll/(Office.Room_Depth*Office.Room_Width)

#Other Set Points
tintH_set=20.0
tintC_set=26.0 #Because data in occupancy is a bit wierd and will causes control issues FIX THIS


#Calculate external heat gains
Q_fenstRad=Q_fenstRad*Office.glass_solar_transmitance #Solar Gains

Q=Q_fenstRad.add(Q_human, axis=0) #only solar gains and human gains for now

	# Office.solve_building_energy(phi_int, phi_sol, theta_e, office.theta_m_prev)
	# Office.solve_building_lighting(ill, occupancy)
Q_fenstRad = Q_fenstRad[0]

Tm_h_rad =[]
Tm_rad =[]
Tm =[]

for ii in range(0, int(8760)):

	print 'qhuman is', Q_human[ii]
	print 'fenst rad is', Q_fenstRad[ii]
	print 'Tout',T_out[ii]
	print Office.theta_m_prev

	Office.solve_building_energy(phi_int=Q_human[ii], phi_sol=Q_fenstRad[ii], theta_e= T_out[ii], theta_m_prev=Office.theta_m_prev)
	Tm_h_rad.append(Office.theta_m)

	# Office.solve_building_energy(0.0001, Q_fenstRad[ii], T_out[ii], Office.theta_m_prev)
	# Tm_rad.append(Office.theta_m)

	# Office.solve_building_energy(0.00001, 0, T_out[ii], Office.theta_m_prev)
	# Tm.append(Office.theta_m)

	# print Office.lighting_demand
	#Office.solve_building_lighting(fenstIll[ii], occupancy[ii])

	# print 'phi_ia=', Office.phi_ia
	# print 'phi_m=', Office.phi_m
	# print 'phi_st=',Office.phi_st
	# print Office.phi_hc_nd_ac
	# Office.theta_int_h_set = 20.0
	# Office.solve_building_energy(phi_int, phi_sol, theta_e, theta_m_prev)
	# print Office.theta_m_prev
	#print Office.has_heating_demand
	# print Office.phi_m_tot
Tm_h_rad.to_csv('Tm_h_rad.csv')
Tm_rad.to_csv('Tm_rad.csv')
Tm.to_csv('Tm.csv')