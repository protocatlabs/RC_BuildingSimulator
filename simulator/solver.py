

"""
===========================
RC Model of a single zone building
===========================
File history and credits:
Prageeth Jayathissa
Mario Frei
Jeremias Schmidli
Amr Elesawy 
"""

import numpy as np
import math
import var_input as f
import matplotlib.pyplot as plt

#Import Data
To,glbRad= f.read_EWP(epw_name='Zurich-Kloten_2013.epw')
incRad=f.read_transmittedR(my_filename='radiation_combination2.csv')

#Single Capacitance Model Parameters
Cm=2.07 #[kWh/C] based of Madsen2011
Ri=5.29 #[C/kWh] based on Madsen2011
Q=incRad #only solar gains for now
Ti=20 #Starting internal temperature
Data_Ti=[] 

#Differential Equation Parameters
dt=.25 #hours

for ii in range(0, int(8760)):
	for jj in range(0,int(1/dt)):
		h_step=ii #delete
	

		dTi=(float(Q[ii])/(Cm) + (1/(Cm*Ri))*(float(To[ii])-Ti))*dt
		Ti=Ti+dTi
	Data_Ti.append(Ti)



plt.plot(range(0, int(8760)),To, range(0, int(8760)),Data_Ti)
plt.show()