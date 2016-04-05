

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
import input_data as f
import matplotlib.pyplot as plt
import PID_controller

#Import Data
To,glbRad= f.read_EWP(epw_name='Zurich-Kloten_2013.epw')
Q_fenstRad=f.read_transmittedR(my_filename='radiation_combination2.csv')
occupancy, Q_human=f.read_occupancy(myfilename='Occupancy_COM.csv')
tintC_set=26 #Because data in occupancy is a bit wierd and will causes control issues


#Single Capacitance Model Parameters
Cm=2.07 #[kWh/K] Room Capacitance based of Madsen2011
Ri=42 #[K/kWh] Resistance to outside air. Based off glass having a Uvalue of 1.978W/m2K, 12m2 facade glass
glass_transmitance=0.687 #Dbl LoE (e=0.2) Clr 3mm/13mm Air

#Calculate uncontrollable Q data series
Q_fenstRad=Q_fenstRad*glass_transmitance #Solar Gains
Q=Q_fenstRad.add(Q_human, axis=0) #only solar gains and human gains for now

Q_heat=0
Q_cool=0
Total_Heat=0
Total_Cooling=0
Ti=20 #Starting internal temperature
Data_Ti=[] 

#PID setup
heatingControl=PID_controller.PID(P=2.0, I=4.0, D=0.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500)
coolingControl=PID_controller.PID(P=2.0, I=4.0, D=0.0, Derivator=0, Integrator=0, Integrator_max=500, Integrator_min=-500)

#Differential Equation Parameters
dt=.25 #hours

for ii in range(0, int(8760)):
	for jj in range(0,int(1/dt)):
	

		dTi=((Q.iat[ii,0]+Q_heat+Q_cool)/(Cm) + (1/(Cm*Ri))*(float(To[ii])-Ti))*dt
		Ti=Ti+dTi
		if occupancy['tintH_set'].iat[ii]>=0 and occupancy['tintH_set'].iat[ii]>Ti:
			heatingControl.setPoint(occupancy['tintH_set'].iat[ii])

			Q_heat= heatingControl.update(Ti)/10
		else:
			Q_heat=0
		Total_Heat+=Q_heat

		if Ti>tintC_set:
			coolingControl.setPoint(tintC_set)
			Q_cool = coolingControl.update(Ti)/2
		else:
			Q_cool=0
		Total_Cooling+=Q_cool

	Data_Ti.append(Ti)

print 'Total Heating Load is:', Total_Heat, 'kWh'
print 'Total Cooling Load is:', Total_Cooling*-1, 'kWh'
#These values are still a little high, but in the right magnitude at least


plt.plot(range(0, int(8760)),To, range(0, int(8760)),Data_Ti)
plt.show()